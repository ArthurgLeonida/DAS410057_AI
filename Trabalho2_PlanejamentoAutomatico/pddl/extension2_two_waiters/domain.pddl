(define (domain cafeteria-2w)
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
             (bar-free)
             (unassigned ?t - table)
             (assigned ?w - waiter ?t - table)
             (pending ?o - order)
             (ready ?o - order)
             (carried-hand ?w - waiter ?o - order)
             (carried-tray ?w - waiter ?o - order)
             (served ?o - order)
             (cold ?o - order)
             (hot ?o - order)
             (for-table ?o - order ?t - table)
             (dirty ?t - table)
             (clean ?t - table))

(:functions (travel-empty ?from ?to - location)
            (travel-tray  ?from ?to - location)
            (clean-time   ?t - table)
            (tray-load    ?w - waiter)
            - number)

; Extensao 2: dois garcons.
; - (bar-free) e um semaforo: cada acao no balcao toma e devolve esse recurso;
; - (unassigned ?t) + (assigned ?w ?t) + claim-table impedem que duas atendentes
;   sirvam ou limpem a mesma mesa.

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

(:durative-action claim-table
  :parameters (?w - waiter ?t - table)
  :duration (= ?duration 1)
  :condition (at start (unassigned ?t))
  :effect (and (at start (not (unassigned ?t))) (at end (assigned ?w ?t))))

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
                  (over all (assigned ?w ?t))
                  (over all (hand-free ?w)) (over all (no-tray ?w)))
  :effect (and (at start (not (dirty ?t))) (at end (clean ?t))))

(:durative-action take-tray
  :parameters (?w - waiter)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w bar)) (at start (hand-free ?w))
                  (at start (no-tray ?w)) (at start (tray-at-bar)) (at start (bar-free))
                  (at start (<= (tray-load ?w) 0)))
  :effect (and (at start (not (tray-at-bar))) (at start (not (bar-free)))
               (at start (not (no-tray ?w)))
               (at end (holding-tray ?w)) (at end (bar-free))))

(:durative-action return-tray
  :parameters (?w - waiter)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w bar)) (at start (holding-tray ?w))
                  (at start (bar-free)) (at start (<= (tray-load ?w) 0)))
  :effect (and (at start (not (holding-tray ?w))) (at start (not (bar-free)))
               (at end (tray-at-bar)) (at end (bar-free)) (at end (no-tray ?w))))

(:durative-action load-hand
  :parameters (?w - waiter ?o - order ?t - table)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w bar)) (at start (hand-free ?w))
                  (over all (no-tray ?w)) (at start (bar-free))
                  (at start (ready ?o)) (at start (for-table ?o ?t))
                  (over all (assigned ?w ?t)))
  :effect (and (at start (not (ready ?o))) (at start (not (hand-free ?w)))
               (at start (not (bar-free))) (at end (carried-hand ?w ?o))
               (at end (bar-free))))

(:durative-action load-tray
  :parameters (?w - waiter ?o - order ?t - table)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w bar)) (over all (holding-tray ?w))
                  (at start (bar-free)) (at start (ready ?o))
                  (at start (for-table ?o ?t)) (over all (assigned ?w ?t))
                  (at start (< (tray-load ?w) 3)))
  :effect (and (at start (not (ready ?o))) (at start (not (bar-free)))
               (at start (increase (tray-load ?w) 1))
               (at end (carried-tray ?w ?o)) (at end (bar-free))))

(:durative-action serve-hand
  :parameters (?w - waiter ?o - order ?t - table)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w ?t)) (at start (carried-hand ?w ?o))
                  (at start (for-table ?o ?t)) (over all (assigned ?w ?t)))
  :effect (and (at start (not (carried-hand ?w ?o))) (at end (served ?o))
               (at end (hand-free ?w))))

(:durative-action serve-tray
  :parameters (?w - waiter ?o - order ?t - table)
  :duration (= ?duration 1)
  :condition (and (over all (at ?w ?t)) (at start (carried-tray ?w ?o))
                  (at start (for-table ?o ?t)) (over all (assigned ?w ?t)))
  :effect (and (at start (not (carried-tray ?w ?o))) (at end (served ?o))
               (at start (decrease (tray-load ?w) 1))))

)
