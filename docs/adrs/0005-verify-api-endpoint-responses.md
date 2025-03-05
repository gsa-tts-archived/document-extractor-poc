# 5. Verify API endpoint responses

Date: 2025-02-17

## Status

Accepted

## Context

When the UI queries the Verify API endpoint, the API endpoint needs to respond
with something to indicate the state of the document processing.  This provides
a structured, well-known mechanism for providing that feedback.

## Decision

When the UI queries the Verify API endpoint, it will send along a Document ID
so that the API can determine which document is being tracked.  From there,
the API will respond with a JSON object with the following fields:

1. `resultCode`: an integer representing the state of the request
2. `resultString`: a string explaining in plain language what's going on
3. `resultsData`: a JSON object with the results of the query (if any)

The `resultCode` integer will be similar to HTTP response codes:

- `102`: the extract is still running, please come back in a bit
- `200`: the extract is finished, the results are under the `resultsData` field
- `404`: the requested Document Id doesn't correspond to a known data set
- `500`: there was a problem with the extract and there are no results

The `resultsString` is free-form and should be descriptive of what's happening.

### Example

```JSON
{
  "resultCode": 200,
  "resultString": "Yay",
  "resultsData": {
    "foq": "bat"
  }
}
```

## Consequences

We've plenty of room to insert additional codes, expand upon codes, etc. while
also having some level of structure to give some general indication of the
state of things.
