# 0001: Do not count same-day second orders as a return

**Status:** accepted, 0.1.0

## Context

30% of second orders happen on the same day as the first. Counting them makes retention look 50% better than it is.

## Decision

A return is an order on a later calendar day than the first order.

## Tradeoff

- The baseline reflects real return visits.
- A customer who split a basket and later came back is still counted, by their next later order.
