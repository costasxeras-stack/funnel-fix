# Case study: Funnel Fix

## The question

A marketplace can grow by finding new buyers or by bringing existing ones back. Olist's public data shows the second is almost not happening. Which step of the customer funnel is weakest, what explains it, and what experiment would fix it?

## Approach

Build the funnel from the first order to a second one, using only customers who had at least 180 days to come back so every customer gets the same chance. Find the step with the lowest conversion, test the obvious explanation (a bad first experience) against the data, find when and after which purchases people do return, then design the smallest experiment that could change it, and check how long it would take and whether the incentive could pay.

## Findings

### 1. The second order is the broken step (confirmed)

Every step from first order to a 4 or 5 star rating converts at 78% or more. Of 43,600 happy first-time customers, 888 (2.0%) ordered again within 180 days.

### 2. Same-day second orders are not returns (confirmed)

30% of second orders were placed on the same day as the first, so they are split baskets. Counting them would overstate retention.

### 3. A bad first order hurts, but is not the main cause (confirmed)

Late first orders return at 1.65% against 2.00% on time. 1 and 2 star raters at 1.64% against 2.05%. Even the happiest customers rarely come back.

### 4. Returning customers come back early (confirmed)

Median 68 days, a quarter within 22 days, and the first month is the busiest.

### 5. Home and sports purchases bring people back most (confirmed)

Bed and bath 2.66%, sports 2.61%, furniture and decor 2.42%, against 1.51% for computer accessories.

### 6. Free shipping needs a high margin to pay (estimate)

At a 1.37% baseline and a 50% lift, free shipping (median freight 17.19 BRL) costs 51 BRL per extra second order, against a median order of 86.57 BRL, so it needs about a 59% margin. Hence a cheap reminder first.

### 7. A day-21 reminder lifts 90-day repeat orders by 50% or more (hypothesis)

The experiment exists to test this. Needs about 11,300 customers and 5.4 months at 4,765 eligible customers a month.

## Decisions

### Do not count same-day second orders as a return

30% of second orders happen on the same day as the first. Counting them makes retention look 50% better than it is.

**Decision:** A return is an order on a later calendar day than the first order.

Full record: [decisions/0001-exclude-same-day-orders.md](decisions/0001-exclude-same-day-orders.md)

### Test a free reminder before a free-shipping voucher

Vouchers are the usual retention lever. They are also paid on every second order, including those that would have happened anyway.

**Decision:** Phase 1 tests a reminder alone. Phase 2, only if phase 1 works, tests adding free shipping, with the cost per extra order and break-even margin shown up front.

Full record: [decisions/0002-reminder-before-voucher.md](decisions/0002-reminder-before-voucher.md)

### Size the test for a 50% lift, and say why

At a 1.37% baseline, a 20% lift needs about 62,000 customers, 13 months of traffic plus the 90-day window.

**Decision:** Design for a 50% relative lift (to about 2.06%): about 11,300 customers and 5.4 months. If the real effect is smaller, it is too small to matter for this business anyway.

Full record: [decisions/0003-target-a-large-lift.md](decisions/0003-target-a-large-lift.md)

## What I learned as a PM

- The obvious fix (better delivery) would barely move retention. Checking the explanation before designing the test changed the experiment.
- A retention baseline under 2% makes experiments slow. Choosing the lift worth detecting is a product decision, not a statistics one.
- Showing the voucher economics up front prevents a test that wins on the metric and loses money.

## Limits

- Data from 2016 to August 2018.
- Customers matched by Olist's unique customer ID only.
- Segment differences are correlations.
- The experiment is a design. No result exists yet.

## What I would do next

1. Run phase 1 with a parcel insert if the marketplace owns the email address
2. Test the timing: day 7, 21 and 45
3. Model which first orders predict a return, to target the message

## My role

I framed the problem, made the product calls, checked every number and wrote the conclusions. 
