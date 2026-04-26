(define (domain testpd)
(:requirements :strips :typing :durative-actions :fluents)
(:types loc agent)

(:predicates (at ?a - agent ?l - loc))

(:functions (dist ?a ?b - loc) - number)

(:durative-action move
  :parameters (?a - agent ?from ?to - loc)
  :duration (= ?duration (dist ?from ?to))
  :condition (at start (at ?a ?from))
  :effect (and (at start (not (at ?a ?from))) (at end (at ?a ?to))))
)
