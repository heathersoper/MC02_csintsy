% family_kb.pl - Family Relationship Knowledge Base

% Dynamic predicates that can be asserted at runtime
:- dynamic(parent_of/2).
:- dynamic(is_male/1).
:- dynamic(is_female/1).

% Basic derived relationships
father_of(X, Y) :- parent_of(X, Y), is_male(X).
mother_of(X, Y) :- parent_of(X, Y), is_female(X).

% Child relationship (inverse of parent)
child_of(Y, X) :- parent_of(X, Y).

% Sibling relationships
sibling_of(X, Y) :- 
    parent_of(Z, X), 
    parent_of(Z, Y), 
    X \= Y.

brother_of(X, Y) :- sibling_of(X, Y), is_male(X).
sister_of(X, Y) :- sibling_of(X, Y), is_female(X).

% Grandparent relationships
grandparent_of(X, Y) :- 
    parent_of(X, Z), 
    parent_of(Z, Y).

grandfather_of(X, Y) :- grandparent_of(X, Y), is_male(X).
grandmother_of(X, Y) :- grandparent_of(X, Y), is_female(X).

% Aunt and Uncle relationships
aunt_of(X, Y) :- 
    sibling_of(X, Z), 
    parent_of(Z, Y), 
    is_female(X).

uncle_of(X, Y) :- 
    sibling_of(X, Z), 
    parent_of(Z, Y), 
    is_male(X).

% Niece and Nephew relationships
niece_of(X, Y) :- 
    parent_of(Z, X), 
    sibling_of(Y, Z), 
    is_female(X).

nephew_of(X, Y) :- 
    parent_of(Z, X), 
    sibling_of(Y, Z), 
    is_male(X).

% Cousin relationships
cousin_of(X, Y) :- 
    parent_of(A, X), 
    parent_of(B, Y), 
    sibling_of(A, B), 
    X \= Y.

% General relative relationship
relative(X, Y) :- 
    (parent_of(X, Y); parent_of(Y, X); 
     sibling_of(X, Y); grandparent_of(X, Y); grandparent_of(Y, X);
     aunt_of(X, Y); aunt_of(Y, X); uncle_of(X, Y); uncle_of(Y, X);
     cousin_of(X, Y)).

% Ancestor relationship (transitive closure of parent)
ancestor_of(X, Y) :- parent_of(X, Y).
ancestor_of(X, Y) :- parent_of(X, Z), ancestor_of(Z, Y).

% Descendant relationship (inverse of ancestor)
descendant_of(X, Y) :- ancestor_of(Y, X).