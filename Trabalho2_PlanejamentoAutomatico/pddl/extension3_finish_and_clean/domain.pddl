(define (domain cafeteria-finish)
(:requirements :strips :typing :durative-actions :fluents)

(:types location order waiter - object
        table - location)

(:constants bar - location)

(:predicates (at ?w - waiter ?l - location)
             (barista-free)
             (hand-free ?w - waiter)
             (holding-tray ?w - waiter)
             (no-tray ?w - waiter)
             (tray-at-bar)
             (pending ?o - order)
             (ready ?o - order)
             (carried-hand ?w - waiter ?o - order)
             (carried-tray ?w - waiter ?o - order)
             (served ?o - order)
             (drinking-start ?o - order)
             (cold ?o - order)
             (hot ?o - order)
             (for-table ?o - order ?t - table)
             (dirty ?t - table)
             (clean ?t - table))

(:functions (travel-empty ?from ?to - location)
            (travel-tray  ?from ?to - location)
            (clean-time   ?t - table)
            (tray-load    ?w - waiter)
            (customers    ?t - table)
            - number)

; Extensao 3: cliente termina a bebida em 4 u.t. = 8 unidades PDDL.
; serve-* marca (drinking-start ?o). A acao drinking (duracao = 8) consome
; essa marca e, ao terminar, decrementa (customers ?t). clean so roda com
; (customers ?t) = 0. A meta exige clean de todas as mesas.

(:durative-action prepare-cold
  :parameters (?o - order)
  :duration (= ?duration 6)
  :condition (and (at start (barista-free)) (at start (pending ?o)) (at start (cold ?o)))
  :effect (and (at start (not (barista-free))) (at start (not (pending ?o)))
               (at end (barista-free)) (at end (ready ?o))))

(:durative-action prepare-hot
  :parameters (?o - order)
  :duration (= ?duration 10)
  :condition (and (at start (barista-free)) (at start (pending ?o)) (at start (hot ?o)))
  :effect (and (at start (not (barista-free))) (at start (not (pending ?o)))
               (at end (barista-free)) (at end (ready ?o))))

(:durative-action move-empty
  :parameters (?w - waiter ?from ?to - location)
  :duration (= ?duration (travel-empty ?from ?to))
  :condition (and (at start (at ?w ?from)) (over all (no-tray ?w)))
  :effect (and (at start (not (at ?w ?from))) (at end (at ?w ?to))))

(:durative-action move-tray
  :parameters (?w - waiter ?from ?to - location)
  :duration (= ?duration (travel-tray ?from ?to))
  :condition (and (at start (at ?w ?from)) (over all (holding-tray ?w)))
  :effect (and (at start (not (at ?w ?from))) (at end (at ?w ?to))))

(:durative-action clean-table
  :parameters (?w - waiter ?t - table)
  :duration (= ?duration (clean-time ?t))
  :condition (and (over all (at ?w ?t)) (at start (dirty ?t))
                  (at start (<= (customers ?t) 0))
                  (over all (hand-free ?w)) (over all (no-tray ?w)))
  :effect (and (at start (not (dirty ?t))) (at end (clean ?t))))

(:durative-action take-tray
  :parameters (?w - waiter)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w bar)) (at start (hand-free ?w))
                  (at start (no-tray ?w)) (at start (tray-at-bar))
                  (at start (<= (tray-load ?w) 0)))
  :effect (and (at start (not (tray-at-bar))) (at start (not (no-tray ?w)))
               (at end (holding-tray ?w))))

(:durative-action return-tray
  :parameters (?w - waiter)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w bar)) (at start (holding-tray ?w))
                  (at start (<= (tray-load ?w) 0)))
  :effect (and (at start (not (holding-tray ?w))) (at end (tray-at-bar))
               (at end (no-tray ?w))))

(:durative-action load-hand
  :parameters (?w - waiter ?o - order)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w bar)) (at start (hand-free ?w))
                  (over all (no-tray ?w)) (at start (ready ?o)))
  :effect (and (at start (not (ready ?o))) (at start (not (hand-free ?w)))
               (at end (carried-hand ?w ?o))))

(:durative-action load-tray
  :parameters (?w - waiter ?o - order)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w bar)) (over all (holding-tray ?w))
                  (at start (ready ?o)) (at start (< (tray-load ?w) 3)))
  :effect (and (at start (not (ready ?o))) (at end (carried-tray ?w ?o))
               (at start (increase (tray-load ?w) 1))))

(:durative-action serve-hand
  :parameters (?w - waiter ?o - order ?t - table)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w ?t)) (at start (carried-hand ?w ?o))
                  (at start (for-table ?o ?t)))
  :effect (and (at start (not (carried-hand ?w ?o))) (at end (served ?o))
               (at end (hand-free ?w)) (at end (drinking-start ?o))))

(:durative-action serve-tray
  :parameters (?w - waiter ?o - order ?t - table)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w ?t)) (at start (carried-tray ?w ?o))
                  (at start (for-table ?o ?t)))
  :effect (and (at start (not (carried-tray ?w ?o))) (at end (served ?o))
               (at start (decrease (tray-load ?w) 1)) (at end (drinking-start ?o))))

(:durative-action drinking
  :parameters (?o - order ?t - table)
  :duration (= ?duration 8)
  :condition (and (at start (drinking-start ?o)) (at start (for-table ?o ?t)))
  :effect (and (at start (not (drinking-start ?o)))
               (at end (decrease (customers ?t) 1))))

)
