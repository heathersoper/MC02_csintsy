/*
    Gender and Parent Relationship are separated as 
    these serve as the basis for the structure 
    of the family tree
*/

:- dynamic(is_female/1).
:- dynamic(is_male/1).
:- dynamic(parent_of/2).
:- dynamic(are_siblings/2).
:- dynamic(grandparent_of/2).
:- dynamic(auncle_of/2).

/* ***** Gender Establishment ***** */

/* *** Female *** */

/* If X is a mother */
is_female(X) :- 
    mother_of(X, _).

/* If X is a daughter */
is_female(X) :- 
    daughter_of(X, _).

/* If X is a sister */
is_female(X) :- 
    sister_of(X, _).

/* If X is a grandmother */
is_female(X) :- 
    grandmother_of(X, _).

/* If X is an aunt */
is_female(X) :- 
    aunt_of(X, _).


/* *** Male *** */

/* If X is a father */
is_male(X) :- 
    father_of(X, _).

/* If X is a son */
is_male(X) :- 
    son_of(X, _).

/* If X is a brother */
is_male(X) :- 
    brother_of(X, _).

/* If X is a grandfather */
is_male(X) :- 
    grandfather_of(X, _).

/* If X is an uncle */
is_male(X) :- 
    uncle_of(X, _).



/* ***** Familial Role Establishment ***** */

/* *** Parent Relationship *** */

/* If X is the mother of Y */
parent_of(X, Y) :-
    mother_of(X, Y).

/* If X is the father of Y */
parent_of(X, Y) :-
    father_of(X, Y).

/* If X is one of the parents of Y */
parent_of(X, Y) :-
    parents_of(X, _A, Y);
    parents_of(_A, X, Y).

/* If Y is the child of X */
parent_of(X, Y) :-
    child_of(Y, X).

% TODO: take into consideration more than 3 children in one statement
/* If Y is one of the children of X */
parent_of(X, Y) :-
    children_of(Y, _A, _B, X);
    children_of(_A, Y, _B, X);
    children_of(_A, _B, Y, X).

/* If X is a daughter of Y */
parent_of(X, Y) :-
    daughter_of(Y, X).

/* If X is a son of Y */
parent_of(X, Y) :-
    son_of(Y, X).

/* If Y has a sibling that has a parent */
parent_of(X, Y) :-
    are_siblings(Y, A), 
    parent_of(X, A).


/* *** Sibling Establishment *** */

/* If they are sisters */
are_siblings(X, Y) :- 
    sister_of(X, Y);
    sister_of(Y, X).

/* If they are brothers */
are_siblings(X, Y) :- 
    brother_of(X, Y);
    brother_of(Y, X).


/* *** Grandparent Establishment *** */

/* If X is a grandmother */
grandparent_of(X, Y) :-
    grandmother_of(X, Y),
    X \= Y.

/* If X is a grandfather */
grandparent_of(X, Y) :-
    grandfather_of(X, Y),
    X \= Y.


/* *** Auncle Establishment *** */

/* If X is an aunt */
auncle_of(X, Y) :-
    aunt_of(X, Y).

/* If X is an uncle */
auncle_of(X, Y) :-
    uncle_of(X, Y).