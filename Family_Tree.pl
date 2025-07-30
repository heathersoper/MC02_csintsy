
:- dynamic(parents_of/3).
:- dynamic(mother_of/2).
:- dynamic(father_of/2).
:- dynamic(child_of/2).
:- dynamic(children_of/4).
:- dynamic(daughter_of/2).
:- dynamic(son_of/2).
:- dynamic(are_siblings/2).
:- dynamic(sister_of/2).
:- dynamic(brother_of/2).
:- dynamic(grandparent_of/2).
:- dynamic(grandmother_of/2).
:- dynamic(grandfather_of/2).
:- dynamic(aunt_of/2).
:- dynamic(uncle_of/2).


/* ***** Nuclear Family Establishment ***** */

/* *** Parents Relationship *** */

/* If both are the mother and father of Z */
parents_of(X, Y, Z) :-
    parent_of(X, Z), 
    parent_of(Y, Z),
    X \= Y.

/* If two siblings share the same mother/father */
parents_of(X, Y, Z) :-
    parent_of(X, Z), 
    parent_of(Y, A), 
    are_siblings(Z, A),
    X \= Y.


/* *** Mother Relationship *** */

/* If X is a parent of Y and X is female */
mother_of(X, Y) :-
    parent_of(X, Y),
    is_female(X),
    X \= Y.

/* If Y has a sibling that is a child of X and X is female */
mother_of(X, Y) :-
    are_siblings(Y, A),
    parent_of(X, A),
    is_female(X).


/* *** Father Relationship *** */

/* If X is a parent of Y and X is male */
father_of(X, Y) :-
    parent_of(X, Y),
    is_male(X).

/* If Y has a sibling that is a child of X and X is male */
father_of(X, Y) :-
    are_siblings(Y, A),
    parent_of(X, A),
    is_male(X).


/* *** Child Relationship *** */

/* If Y is a parent of X */
child_of(X, Y) :-
    parent_of(X, Y).

/* If X has a sibling that has a parent */
child_of(X, Y) :-
    are_siblings(X, A),
    child_of(A, Y).


/* *** Children Relationship *** */
/* ?: Consider more than 3 children */

/* If all are children of A */
children_of(X, Y, Z, A) :-
    child_of(X, A),
    child_of(Y, A),
    child_of(Z, A).


/* *** Daughter Relationship *** */

/* If X is a child of Y and X is female */
daughter_of(X, Y) :-
    child_of(X, Y),
    is_female(X).


/* *** Son Relationship *** */

/* If X is a child of Y and X is male */
son_of(X, Y) :-
    child_of(X, Y),
    is_male(X).


/* *** Sibling Relationship *** */


/* *** Sister Relationship *** */

/* If they are siblings and X is female */
sister_of(X, Y) :-
    are_siblings(X, Y),
    is_female(X).


/* *** Brother Relationship *** */

/* If they are siblings and X is male */
brother_of(X, Y) :-
    are_siblings(X, Y),
    is_male(X).



/* ***** Extended Family Establishment ***** */

/* *** Grandparent Relationship *** */

/* If X is a parent of A who is a parent of Y */

/* If Y has an aunt or uncle that has a parent */



/* *** Grandmother Relationship *** */

/* If X is a grandparent of Y and X is female */
grandmother_of(X, Y) :-
    grandparent_of(X, Y),
    is_female(X).


/* *** Grandfather Relationship *** */

/* If X is a grandparent of Y and X is male */
grandfather_of(X, Y) :-
    grandparent_of(X, Y),
    is_male(X).


/* *** Aunt Relationship *** */

/* If X is an auncle and X is female */
aunt_of(X, Y) :-
    auncle_of(X, Y),
    is_female(X).

/* If the parent of Y has a sibling X and X is female */
aunt_of(X, Y) :-
    parent_of(A, Y),
    are_siblings(X, A),
    is_female(X).

/* If the grandparent of Y has a child X that is not the parent of Y and X is female */
aunt_of(X, Y) :-
    grandparent_of(A, Y),
    parent_of(A, X),
    not(parent_of(X, Y)),
    is_female(X).


/* *** Uncle Relationship *** */

/* If X is an auncle and X is female */
uncle_of(X, Y) :-
    auncle_of(X, Y),
    is_male(X).

/* If the parent of Y has a sibling X and X is male */
uncle_of(X, Y) :-
    parent_of(A, Y),
    are_siblings(X, A),
    is_male(X).

/* If the grandparent of Y has a child X that is not the parent of Y and X is male */
uncle_of(X, Y) :-
    grandparent_of(A, Y),
    parent_of(A, X),
    not(parent_of(X, Y)),
    is_male(X).
