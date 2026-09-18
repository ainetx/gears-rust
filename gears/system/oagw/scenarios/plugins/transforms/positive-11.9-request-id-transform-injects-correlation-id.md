# Request ID transform plugin injects/preserves correlation id

## Setup

Bind the builtin `request_id` transform plugin:

```json
{
  "plugins": {
    "sharing": "private",
    "items": [
      {
        "plugin_ref": "gts.cf.core.oagw.transform_plugin.v1~cf.core.oagw.request_id.v1",
        "config": {}
      }
    ]
  }
}
```

## Scenario A: no client `x-request-id` → plugin injects a UUID

```http
POST /api/oagw/v1/proxy/<alias>/echo HTTP/1.1
Host: oagw.example.com
Authorization: Bearer <tenant-token>
Content-Type: application/json
```

Expected: the upstream receives `x-request-id: <uuid>` — a freshly generated, valid UUID.

## Scenario B: client provides `x-request-id` → preserved unchanged

```http
POST /api/oagw/v1/proxy/<alias>/echo HTTP/1.1
Host: oagw.example.com
Authorization: Bearer <tenant-token>
Content-Type: application/json
X-Request-ID: e2e-trace-abc123
```

Expected: the upstream receives `x-request-id: e2e-trace-abc123` unchanged (not overwritten).

## What to check

- Correlation-id propagation is **not** automatic gateway behavior — it only happens when the `request_id` `TransformPlugin` is explicitly bound via `plugins.items[].plugin_ref`, same as any other transform plugin. See [positive-7.6](../../proxy-api/request-transforms/positive-7.6-request-correlation-headers-propagate-end-end.md) for the general end-to-end correlation-header contract this plugin fulfills.
