# Verified Build Results

Verification date: 1 October 2026 (UTC)

## Automated tests

```text
34 passed in 0.70s
Total application coverage: 91%
```

Covered areas:

- Tharun frontend delivery and backend fetch wiring
- Health and category endpoints
- Recommendation endpoint
- Invalid request validation (HTTP 422)
- Every category and boundary-budget combination
- Budget total and reserve invariants
- Gemini structured-response path with a mock client
- Gemini error, invalid-output and missing-key paths
- No-login and no-demo checks

## Additional checks

```text
JavaScript syntax: OK
Python compile: OK
OpenAPI schema: OK
HTTP health endpoint: OK
HTTP categories endpoint: OK
HTTP recommendation endpoint with mocked Gemini: OK
```

The live Gemini call is intentionally not part of automated tests because a secret API key must never be stored in the repository and tests should not consume API quota. A real key is required only for manual/live plan generation.
