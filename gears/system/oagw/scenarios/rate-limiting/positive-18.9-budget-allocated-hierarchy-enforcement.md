# Allocated budget: hierarchy sum enforcement

## Setup

Parent upstream with an inheritable, allocated budget:

```json
{
  "rate_limit": {
    "sharing": "inherit",
    "sustained": { "rate": 100, "window": "minute" },
    "budget": { "mode": "allocated", "total": 100, "overcommit_ratio": 1.0 }
  }
}
```

Descendant tenants create their own upstream bound to the same alias, each with its own `rate_limit.sustained.rate` — no `budget` field on the child.

## Scenario A: children within budget

Child A requests `60/min`, child B requests `50/min` after: `60 + 50 = 110 > 100` → **child B's creation is rejected**.

```
resp.status_code == 400
"budget allocation exceeded" in resp.text
```

Two children whose rates sum to `<= total` (e.g. `40 + 40 = 80 <= 100`) both succeed.

## Scenario B: overcommit_ratio raises the ceiling, does not remove it

With `overcommit_ratio: 1.5` on the parent (ceiling = `100 * 1.5 = 150`):
- Children summing to `80 + 60 = 140 <= 150` → both succeed.
- A further child pushing the sum to `100 + 60 = 160 > 150` → rejected with `400`, `"budget allocation exceeded"`.

## Scenario C: update-time revalidation

Updating an existing child's `sustained.rate` so the new sum exceeds the parent's budget is rejected the same way (`400`, `"budget allocation exceeded"`) — allocation is revalidated on every `PUT`, not just at creation.

## Scenario D: rates are normalized to req/s before comparison

Budget comparison converts every rate to requests/second regardless of each upstream's own `window`. Parent `total: 60` at `window: "minute"` (a `1 req/s` ceiling); a child requesting `2/second` (`2 req/s`) exceeds it and is rejected, even though `2 < 60` as raw numbers.

## Scenario E: allocated budget requires the child to declare a rate limit

Under an `allocated` parent budget, a child upstream that omits `rate_limit` entirely is rejected:

```
resp.status_code == 400
"rate_limit is required" in resp.text
```

## What to check

- `mode: "shared"` does not enforce this sum check — a child may bind to a `shared`-budget parent without declaring its own `rate_limit` at all (see [positive-18.7 Scenario B](positive-18.7-budget-modes-behave-specified.md)).
- `mode: "unlimited"` (or no `budget` field at all — the default) skips allocation validation entirely; children may declare any rate.
- See [negative-18.8](negative-18.8-budget-field-validation-errors.md) for the field-shape validation errors that apply before this sum-based enforcement is even reached.
