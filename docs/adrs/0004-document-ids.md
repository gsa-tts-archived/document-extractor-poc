# 4. Document IDs

Date: 2025-02-17

## Status

Accepted.

## Context

We need to be able to have a unique ID that follows a work session with a file.
That is, from the moment a file is uploaded, we ought to be able to reference
that file, its data, the results, etc. when we make a ReSTful API call using
that document ID.

## Decision

Document IDs will be randomly-generated,
[RFC-4122](https://datatracker.ietf.org/doc/html/rfc4122.html)-compliant UUIDs
(uuid4) in hex digest format that are passed to the API endpoints with the
name `documentId`.

Python documentation for
[uuid.uuid4()](https://docs.python.org/3/library/uuid.html#uuid.uuid4)

## Consequences

Because we're using very large unique identifiers, it's extremely unlikely
that we'll experience reference collision.  At the same time, because of the
size of these IDs, a simple request will have keys that are 36 characters
long:

```text
A6B3839B-27C4-4DFC-AA17-8D08F7475062
```

Also, because we're using an RFC-provided specification, we can be relatively
assured that we'll be able to interact with, validate, etc. keys like these
regardless of the platform, language, tech stack, etc. being used.
