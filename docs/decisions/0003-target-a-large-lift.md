# 0003: Size the test for a 50% lift, and say why

**Status:** accepted, 0.1.0

## Context

At a 1.37% baseline, a 20% lift needs about 62,000 customers, 13 months of traffic plus the 90-day window.

## Decision

Design for a 50% relative lift (to about 2.06%): about 11,300 customers and 5.4 months. If the real effect is smaller, it is too small to matter for this business anyway.

## Tradeoff

- An answer within two quarters.
- A real but small effect will look like no effect. The decision rule allows one extension.
- Only happy, on-time customers are eligible, which keeps the message relevant but limits traffic.
