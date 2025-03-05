# 6. Upload API endpoint responses

Date: 2025-02-17

## Status

Accepted

## Context

When the UI uploads a file to the Upload API endpoint, the API endpoint needs
to respond with something to indicate the state of the document processing.
This provides a structured, well-known mechanism for providing that feedback.

## Decision

The request to upload a document takes the form of a `POST` to the Upload
API endpoing.  The request includes a JSON object including and describing
the file.

1. `body`: an object with two fields
    1. `file_content`: the base64-encoded content of the file being uploaded
    2. `file_name`: the name of the file being uploaded

When the UI uploads a file to the Upload API endpoint, it will await a
Document ID tracking the document's status.  From there, the API will respond
with a JSON object with the following fields:

1. `resultCode`: an integer representing the state of the request
2. `resultString`: a string explaining in plain language what's going on
3. `documentId`: a string representing the document that was uploaded

The `resultCode` integer will be similar to HTTP response codes:

- `201`: the upload was successful and is now being processed
- `500`: there was a problem with the upload

The `resultsString` is free-form and should be descriptive of what's happening.

### Example

#### Request

```text
POST /document
```
```JSON
{
  "body": {
    "file_content": "<base64-encoded-content>",
    "file_name": "test-file.txt"
  }
}
```

#### Response

```JSON
{
  "resultCode": 201,
  "resultString": "The document was uploaded successfully",
  "documentId": "27CB2808-C91E-4105-BC40-5D192906357B"
}
```

## Consequences

We've plenty of room to insert additional codes, expand upon codes, etc. while
also having some level of structure to give some general indication of the
state of things.
