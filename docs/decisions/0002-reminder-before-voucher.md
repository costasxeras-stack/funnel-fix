# 0002: Test a free reminder before a free-shipping voucher

**Status:** accepted, 0.1.0

## Context

Vouchers are the usual retention lever. They are also paid on every second order, including those that would have happened anyway.

## Decision

Phase 1 tests a reminder alone. Phase 2, only if phase 1 works, tests adding free shipping, with the cost per extra order and break-even margin shown up front.

## Tradeoff

- Learns whether timing and relevance matter before spending money.
- Adds months to reach the voucher answer.
- The calculator makes the voucher economics visible before anyone asks for budget.
