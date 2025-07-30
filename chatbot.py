import re
from pyswip import Prolog

# Initialize Prolog and consult the knowledge base
prolog = Prolog()
prolog.consult("family_kb.pl")

def check_consistency(new_facts):
    """Check if adding new facts would create logical inconsistencies."""
    
    for fact in new_facts:
        # Extract person and relationship info from the fact
        if fact.startswith("parent_of("):
            # Extract parent and child from parent_of(parent, child)
            parent = fact.split("(")[1].split(",")[0].strip()
            child = fact.split(",")[1].split(")")[0].strip()
            
            # Check for self-parenthood
            if parent == child:
                return False, f"{parent.capitalize()} cannot be their own parent!"
            
            # Check for circular parent relationships (ancestry loops)
            try:
                # Would this create a cycle? Check if child is already an ancestor of parent
                if list(prolog.query(f"ancestor_of({child}, {parent})")):
                    return False, f"This would create a circular family relationship - {child.capitalize()} cannot be both ancestor and descendant of {parent.capitalize()}!"
                
                # Also check direct parent relationship in reverse
                if list(prolog.query(f"parent_of({child}, {parent})")):
                    return False, f"This would create a circular relationship - {child.capitalize()} and {parent.capitalize()} cannot both be parents of each other!"
                    
            except:
                pass
            
        elif fact.startswith("is_male(") or fact.startswith("is_female("):
            # Extract person from gender fact
            person = fact.split("(")[1].split(")")[0].strip()
            
            # Check for gender conflicts
            try:
                if fact.startswith("is_male("):
                    if list(prolog.query(f"is_female({person})")):
                        return False, f"{person.capitalize()} cannot be both male and female!"
                else:  # is_female
                    if list(prolog.query(f"is_male({person})")):
                        return False, f"{person.capitalize()} cannot be both male and female!"
            except:
                pass
    
    # Check for gender-role conflicts across multiple facts
    parent_facts = [f for f in new_facts if f.startswith("parent_of(")]
    gender_facts = [f for f in new_facts if f.startswith("is_male(") or f.startswith("is_female(")]
    
    for parent_fact in parent_facts:
        parent = parent_fact.split("(")[1].split(",")[0].strip()
        child = parent_fact.split(",")[1].split(")")[0].strip()
        
        # Check if we're asserting conflicting gender roles
        parent_gender = None
        child_gender = None
        
        # Check new gender facts
        for gender_fact in gender_facts:
            person = gender_fact.split("(")[1].split(")")[0].strip()
            if person == parent:
                parent_gender = "male" if gender_fact.startswith("is_male(") else "female"
            elif person == child:
                child_gender = "male" if gender_fact.startswith("is_male(") else "female"
        
        # Check existing gender facts
        try:
            if parent_gender is None:
                if list(prolog.query(f"is_male({parent})")):
                    parent_gender = "male"
                elif list(prolog.query(f"is_female({parent})")):
                    parent_gender = "female"
                    
            if child_gender is None:
                if list(prolog.query(f"is_male({child})")):
                    child_gender = "male"
                elif list(prolog.query(f"is_female({child})")):
                    child_gender = "female"
        except:
            pass
        
        # Check for role-gender conflicts in the current statement context
        # This is checked by looking at the original statement patterns, but we'll do basic checks here
        
    return True, ""

def apply_facts(facts):
    """Apply a list of facts to the Prolog knowledge base."""
    for fact in facts:
        try:
            prolog.assertz(fact)
        except Exception as e:
            print(f"Error adding fact {fact}: {e}")

def detect_statement_contradictions(prompt, match_groups):
    """Detect contradictions within the statement itself or with existing knowledge."""
    prompt_lower = prompt.lower()
    
    # Check for gender-role contradictions in the statement
    if "father" in prompt_lower or "son" in prompt_lower or "grandfather" in prompt_lower or "uncle" in prompt_lower or "brother" in prompt_lower:
        expected_gender = "male"
        person = match_groups[0].lower()  # Usually the first captured group is the person
        
        # Check if this person is already known to be female
        try:
            if list(prolog.query(f"is_female({person})")):
                role = "father" if "father" in prompt_lower else "son" if "son" in prompt_lower else "grandfather" if "grandfather" in prompt_lower else "uncle" if "uncle" in prompt_lower else "brother"
                return False, f"{person.capitalize()} cannot be a {role} because they are female!"
        except:
            pass
    
    elif "mother" in prompt_lower or "daughter" in prompt_lower or "grandmother" in prompt_lower or "aunt" in prompt_lower or "sister" in prompt_lower:
        expected_gender = "female"
        person = match_groups[0].lower()  # Usually the first captured group is the person
        
        # Check if this person is already known to be male
        try:
            if list(prolog.query(f"is_male({person})")):
                role = "mother" if "mother" in prompt_lower else "daughter" if "daughter" in prompt_lower else "grandmother" if "grandmother" in prompt_lower else "aunt" if "aunt" in prompt_lower else "sister"
                return False, f"{person.capitalize()} cannot be a {role} because they are male!"
        except:
            pass
    
    return True, ""

def handle_statement(prompt):
    """Process and learn from family relationship statements."""
    original_prompt = prompt
    prompt = prompt.strip()

    patterns = [
        # "X is the father of Y."
        (r"(\w+) is the father of (\w+)\.", lambda m: [
            f"parent_of({m[0].lower()}, {m[1].lower()})",
            f"is_male({m[0].lower()})"
        ]),

        # "X is the mother of Y."
        (r"(\w+) is the mother of (\w+)\.", lambda m: [
            f"parent_of({m[0].lower()}, {m[1].lower()})",
            f"is_female({m[0].lower()})"
        ]),

        # "X, Y, and Z are children of W."
        (r"(\w+), (\w+), and (\w+) are children of (\w+)\.", lambda m: [
            f"parent_of({m[3].lower()}, {child.lower()})" for child in m[:3]
        ]),

        # "X is the son of Y."
        (r"(\w+) is the son of (\w+)\.", lambda m: [
            f"parent_of({m[1].lower()}, {m[0].lower()})",
            f"is_male({m[0].lower()})"
        ]),

        # "X is the daughter of Y."
        (r"(\w+) is the daughter of (\w+)\.", lambda m: [
            f"parent_of({m[1].lower()}, {m[0].lower()})",
            f"is_female({m[0].lower()})"
        ]),

        # "X is male." or "X is female."
        (r"(\w+) is (male|female)\.", lambda m: [
            f"is_{m[1].lower()}({m[0].lower()})"
        ]),

        # "X is a sister of Y."
        (r"(\w+) is a sister of (\w+)\.", lambda m: [
            f"is_female({m[0].lower()})"
            # Note: sibling relationship will be derived if they share parents
        ]),

        # "X and Y are siblings."
        (r"(\w+) and (\w+) are siblings\.", lambda m: [
            # This is tricky - we need a common parent. For now, we'll create a placeholder parent.
            # In a real system, you might want to ask for clarification.
            print("Note: I need to know who their common parent is to properly record this relationship.")
        ]),

        # "X is a grandmother of Y."
        (r"(\w+) is a grandmother of (\w+)\.", lambda m: [
            f"is_female({m[0].lower()})"
            # Grandparent relationship will be derived from parent chains
        ]),

        # "X is a grandfather of Y."
        (r"(\w+) is a grandfather of (\w+)\.", lambda m: [
            f"is_male({m[0].lower()})"
            # Grandparent relationship will be derived from parent chains
        ]),

        # "X is a child of Y."
        (r"(\w+) is a child of (\w+)\.", lambda m: [
            f"parent_of({m[1].lower()}, {m[0].lower()})"
        ]),

        # "X is an uncle of Y."
        (r"(\w+) is an uncle of (\w+)\.", lambda m: [
            f"is_male({m[0].lower()})"
            # Uncle relationship will be derived from sibling and parent relationships
        ]),

        # "X is an aunt of Y."
        (r"(\w+) is an aunt of (\w+)\.", lambda m: [
            f"is_female({m[0].lower()})"
            # Aunt relationship will be derived from sibling and parent relationships
        ]),

        # "X and Y are the parents of Z."
        (r"(\w+) and (\w+) are the parents of (\w+)\.", lambda m: [
            f"parent_of({m[0].lower()}, {m[2].lower()})",
            f"parent_of({m[1].lower()}, {m[2].lower()})"
        ]),
    ]

    for pattern, action in patterns:
        match = re.match(pattern, prompt, re.IGNORECASE)
        if match:
            try:
                # Check for statement-level contradictions first
                is_valid, error_msg = detect_statement_contradictions(original_prompt, match.groups())
                if not is_valid:
                    print(f"That's impossible! {error_msg}")
                    return
                
                new_facts = action(match.groups())
                
                # Handle special cases that return None or print messages
                if new_facts is None:
                    return
                
                # Flatten the list in case some actions return nested lists
                flattened_facts = []
                for fact in new_facts:
                    if isinstance(fact, list):
                        flattened_facts.extend(fact)
                    else:
                        flattened_facts.append(fact)
                
                # Check consistency before applying facts
                is_consistent, error_msg = check_consistency(flattened_facts)
                
                if not is_consistent:
                    print(f"That's impossible! {error_msg}")
                    return
                
                # Apply the facts if they're consistent
                apply_facts(flattened_facts)
                print("Okay, I learned something new.")
                
            except Exception as e:
                print(f"Error processing statement: {e}")
            return

    print("Sorry, I couldn't understand that statement.")

def handle_question(prompt):
    """Process and answer family relationship questions."""
    prompt = prompt.strip()
    if not prompt.endswith('?'):
        return "That's not a question."

    # Yes/No questions
    yes_no_patterns = [
        (r"Is (\w+) the father of (\w+)\?", lambda m: f"father_of({m[0].lower()}, {m[1].lower()})"),
        (r"Is (\w+) the mother of (\w+)\?", lambda m: f"mother_of({m[0].lower()}, {m[1].lower()})"),
        (r"Are (\w+) and (\w+) siblings\?", lambda m: f"sibling_of({m[0].lower()}, {m[1].lower()})"),
        (r"Is (\w+) a brother of (\w+)\?", lambda m: f"brother_of({m[0].lower()}, {m[1].lower()})"),
        (r"Is (\w+) a sister of (\w+)\?", lambda m: f"sister_of({m[0].lower()}, {m[1].lower()})"),
        (r"Is (\w+) a daughter of (\w+)\?", lambda m: f"parent_of({m[1].lower()}, {m[0].lower()}), is_female({m[0].lower()})"),
        (r"Is (\w+) a son of (\w+)\?", lambda m: f"parent_of({m[1].lower()}, {m[0].lower()}), is_male({m[0].lower()})"),
        (r"Is (\w+) a child of (\w+)\?", lambda m: f"parent_of({m[1].lower()}, {m[0].lower()})"),
        (r"Is (\w+) an uncle of (\w+)\?", lambda m: f"uncle_of({m[0].lower()}, {m[1].lower()})"),
        (r"Is (\w+) an aunt of (\w+)\?", lambda m: f"aunt_of({m[0].lower()}, {m[1].lower()})"),
        (r"Is (\w+) a grandmother of (\w+)\?", lambda m: f"grandmother_of({m[0].lower()}, {m[1].lower()})"),
        (r"Is (\w+) a grandfather of (\w+)\?", lambda m: f"grandfather_of({m[0].lower()}, {m[1].lower()})"),
        (r"Is (\w+) male\?", lambda m: f"is_male({m[0].lower()})"),
        (r"Is (\w+) female\?", lambda m: f"is_female({m[0].lower()})"),
    ]

    # Wh- questions
    wh_patterns = [
        (r"Who is the father of (\w+)\?", lambda m: f"father_of(X, {m[0].lower()})"),
        (r"Who is the mother of (\w+)\?", lambda m: f"mother_of(X, {m[0].lower()})"),
        (r"Who are the parents of (\w+)\?", lambda m: f"parent_of(X, {m[0].lower()})"),
        (r"Who are the siblings of (\w+)\?", lambda m: f"sibling_of(X, {m[0].lower()})"),
        (r"Who are the brothers of (\w+)\?", lambda m: f"brother_of(X, {m[0].lower()})"),
        (r"Who are the sisters of (\w+)\?", lambda m: f"sister_of(X, {m[0].lower()})"),
        (r"Who are the daughters of (\w+)\?", lambda m: f"parent_of({m[0].lower()}, X), is_female(X)"),
        (r"Who are the sons of (\w+)\?", lambda m: f"parent_of({m[0].lower()}, X), is_male(X)"),
        (r"Who are the children of (\w+)\?", lambda m: f"parent_of({m[0].lower()}, X)"),
        (r"Who is the grandmother of (\w+)\?", lambda m: f"grandmother_of(X, {m[0].lower()})"),
        (r"Who is the grandfather of (\w+)\?", lambda m: f"grandfather_of(X, {m[0].lower()})"),
        (r"Who are the grandparents of (\w+)\?", lambda m: f"grandparent_of(X, {m[0].lower()})"),
        (r"Who are the aunts of (\w+)\?", lambda m: f"aunt_of(X, {m[0].lower()})"),
        (r"Who are the uncles of (\w+)\?", lambda m: f"uncle_of(X, {m[0].lower()})"),
    ]

    # Try yes/no questions
    for pattern, query_fn in yes_no_patterns:
        match = re.fullmatch(pattern, prompt, re.IGNORECASE)
        if match:
            query = query_fn(match.groups())
            try:
                result = list(prolog.query(query, maxresult=1))
                return "Yes." if result else "No."
            except Exception as e:
                return f"Error querying: {e}"

    # Try wh- questions
    for pattern, query_fn in wh_patterns:
        match = re.fullmatch(pattern, prompt, re.IGNORECASE)
        if match:
            query = query_fn(match.groups())
            try:
                results = list(prolog.query(query))
                if results:
                    names = {r['X'].capitalize() for r in results if 'X' in r}
                    if len(names) == 1:
                        return list(names)[0] + "."
                    else:
                        return ", ".join(sorted(names)) + "."
                else:
                    return "I don't know."
            except Exception as e:
                return f"Error querying: {e}"

    return "Sorry, I don't understand the question."

def show_help():
    """Display available commands and examples."""
    print("\n=== Family Chatbot Help ===")
    print("You can teach me about family relationships or ask questions!")
    print("\nExample statements (end with '.'):")
    print("- John is the father of Mary.")
    print("- Sarah is the mother of Tom.")
    print("- Mike is the son of Sarah.")
    print("- Lisa is the daughter of John.")
    print("- John and Sarah are the parents of Tom.")
    print("- Bob is male.")
    print("\nExample questions (end with '?'):")
    print("- Who is the father of Mary?")
    print("- Is John the father of Tom?")
    print("- Who are the children of Sarah?")
    print("- Are Mike and Tom siblings?")
    print("- Who are the grandparents of Lisa?")
    print("\nOther commands:")
    print("- 'help' - Show this help message")
    print("- 'facts' - Show all known facts")
    print("- 'exit' - Quit the program")

def show_facts():
    """Display all known facts in the knowledge base."""
    print("\n=== Known Facts ===")
    
    try:
        # Show parent relationships
        parents = list(prolog.query("parent_of(X, Y)"))
        if parents:
            print("Parent relationships:")
            for p in parents:
                print(f"  {p['X'].capitalize()} is a parent of {p['Y'].capitalize()}")
        
        # Show gender information
        males = list(prolog.query("is_male(X)"))
        if males:
            print("Males:")
            for m in males:
                print(f"  {m['X'].capitalize()}")
                
        females = list(prolog.query("is_female(X)"))
        if females:
            print("Females:")
            for f in females:
                print(f"  {f['X'].capitalize()}")
                
    except Exception as e:
        print(f"Error retrieving facts: {e}")

def chatbot():
    """Main chatbot loop."""
    print("Welcome to the Family Chatbot!")
    print("I can learn about family relationships and answer questions about them.")
    print("Type 'help' for examples, or 'exit' to quit.")
    print()

    while True:
        try:
            prompt = input("> ").strip()
            
            if prompt.lower() == "exit":
                print("Goodbye!")
                break
            elif prompt.lower() == "help":
                show_help()
            elif prompt.lower() == "facts":
                show_facts()
            elif prompt.endswith('.'):
                handle_statement(prompt)
            elif prompt.endswith('?'):
                response = handle_question(prompt)
                print(response)
            else:
                print("Please end statements with '.' and questions with '?', or type 'help' for examples.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    chatbot()