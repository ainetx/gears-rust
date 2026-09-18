# Required headers guard plugin enforcement

## Setup

Bind the builtin `required_headers` guard plugin to the upstream (or route):

```json
{
  "plugins": {
    "sharing": "private",
    "items": [
      {
        "plugin_ref": "gts.cf.core.oagw.guard_plugin.v1~cf.core.oagw.required_headers.v1",
        "config": {
          "required_request_headers": "x-correlation-id"
        }
      }
    ]
  }
}
```

`config.required_request_headers` (and the symmetric `required_response_headers`) is a comma-separated list of header names (see [ADR-0017](../../../docs/ADR/0017-required-headers-guard-plugin.md)).

## Scenario A: required header present → allowed

```http
POST /api/oagw/v1/proxy/<alias>/echo HTTP/1.1
Host: oagw.example.com
Authorization: Bearer <tenant-token>
Content-Type: application/json
X-Correlation-Id: test-123
```

Expected: `200 OK`, request forwarded to upstream.

## Scenario B: required header missing → rejected

Same request without `X-Correlation-Id`.

Expected:
- `400 Bad Request`
- `X-OAGW-Error-Source: gateway`

## Scenario C: unconfigured guard fails open

A guard bound with an empty `config` (no `required_request_headers`, no `required_response_headers`) allows every request through — `200 OK` regardless of what headers are present.

## Scenario D: header name matching is case-insensitive

`config.required_request_headers: "X-Correlation-ID"` is satisfied by a request sending the lowercase `x-correlation-id` (HTTP header names are canonically case-insensitive; the guard follows that convention rather than doing a literal string match).

## What to check

- This is the only guard plugin identifier that is actually bindable via `plugins.items[].plugin_ref` — `timeout` and `cors` are cataloged GTS identifiers with no pluggable behavior; see [DESIGN.md](../../../docs/DESIGN.md#plugin-system) and [negative-10.1](negative-10.1-timeout-guard-plugin-enforces-request-timeout.md).
