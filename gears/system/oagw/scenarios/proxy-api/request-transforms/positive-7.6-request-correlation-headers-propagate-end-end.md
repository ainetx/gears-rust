# Request correlation headers propagate end-to-end

## Scenario A: client provides X-Request-ID

```http
GET /api/oagw/v1/proxy/httpbin.org/get HTTP/1.1
Host: oagw.example.com
Authorization: Bearer <tenant-token>
X-Request-ID: req-abc-123
```

Expected:
- Upstream receives `X-Request-ID: req-abc-123`.
- Client response includes the same `X-Request-ID`.
- Audit log uses this request id.

## Scenario B: client does not provide X-Request-ID

Same request without `X-Request-ID`.

Expected:
- A generated request id reaches the upstream and is consistent across response headers and audit log record — **only if** the builtin `request_id` `TransformPlugin` (`gts.cf.core.oagw.transform_plugin.v1~cf.core.oagw.request_id.v1`) is explicitly bound via `plugins.items[].plugin_ref`. This is not automatic core gateway behavior; without the plugin bound, no `x-request-id` is injected. See [positive-11.9](../../plugins/transforms/positive-11.9-request-id-transform-injects-correlation-id.md) for the plugin's own UUID-generation/preservation contract.
