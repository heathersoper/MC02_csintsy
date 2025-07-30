from pyswip import Prolog

# Initialize Prolog instance
prolog = Prolog()

prolog.consult("Family_Tree.pl")
prolog.consult("Social_Roles.pl") 

# Dynamically add facts to the knowledge base
def add_fact(predicate, *args):
    fact = f"{predicate}({', '.join(args)})"
    prolog.assertz(fact)

# Dynamically query the knowledge base
def query_fact(predicate, *args):
    query = f"{predicate}({', '.join(args)})"
    results = list(prolog.query(query))
    return results

def parsing_fact(words):
    # Parse the input (basic example, assumes correct format)
    if "is" in words and "of" in words and "and" not in words:
        # Extract names from the input
        X = words[0]
        Y = words[-1]
        relation = words[words.index("of") -1] + "_of"
            
        # Add the fact to the Prolog knowledge base
        add_fact(relation, X, Y)
        if relation == "brother_of" or relation == "sister_of":
            add_fact("are_siblings", X, Y)
        elif relation == "child_of" or relation == "parent_of":
            if relation == "child_of":
                add_fact("parent_of", Y, X)
            else:
                add_fact("child_of", Y, X)
        print("\tI've learned Something !")
        return
    # case with multiple inputs
    elif "and" in words:
        if "parents" in words:
            X = words[0]
            Y = words[words.index("and") + 1]
            Z = words[-1]
                
            # Add the fact to the Prolog knowledge base
            add_fact("parents_of", X, Z)
            add_fact("parents_of", Y, Z)
            print("\tI've learned Something !")
            return
        elif "children" in words:
            X = words[0]
            Y = words[words.index("and") + 1]
            Z = words[-1]
                
            # Add the fact to the Prolog knowledge base
            add_fact("parents_of", Z, X)
            add_fact("parents_of", Z, Y)
            print("\tI've learned Something !")
            return
        
        elif "siblings" in words:
            X = words[0]
            Y = words[words.index("and") + 1]

            add_fact("siblings_of", X, Y)
            add_fact("siblings_of", Y, X)
            print("\tI've learned Something !")
            return
    print("\tInvalid Input.")


def parsing_queries(words):
    if words[0] == "is" and "of" in words:
        X = words[1]
        Y = words[-1]
        relation = words[words.index("of") -1] + "_of"

        
        query = query_fact(relation, X, Y)
            
        if query:
            print(f"\tYes, {X} is the {words[words.index("of") -1]} of {Y}.")
        else:
            print("\tI am unable to confirm that fact.")
        return

    elif words[0] == "who":
        X = words[-1]
        relation = words[words.index("of") -1] + "_of"

        query = query_fact(relation, X, "_")
        for result in query:
            print(result)
        return
    
    elif words[0] == "are" and "and" in words:
        X = words[1]
        Y = words[words.index("and") + 1]
        relation = words[-1] + "_of"  
        if words[-1] == "siblings":
            query = query_fact("are_siblings", X, Y)
        else:
            query = query_fact(relation, X, Y)              
        if query:
            print(f"\tYes, {X} and {Y} are {words[-1]}.")
        else:
            print("\tI am unable to confirm that fact.")
        return
    print("\tInvalid Input.")

print("\n\n\tI am you're personal logic chatbot. Please ask me anything !\n")
while True:
    try:
        user_input = input("\t-> ")
        words = user_input.lower().replace(".", "").split()  
        if user_input == "exit":
            break 
        if words[0] == "is" or words[0] == "are" or words[0] == "who":
            parsing_queries(words)
        else:  
            fact_asked = parsing_fact(words)
    except ValueError as e:
        print(f"Error: {e}")    
        break
