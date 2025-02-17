# 3. user interface to s3 data flow

Date: 2025-02-14

## Status

Accepted

## Context

When a user visits the user interface (UI), they see a form allowing them to
select a file and a button to upload it.

How are files uploaded?  When a user selects a file on their local system and
clicks submit to upload it, what actually happens?  How does that file get to
S3?

## Decision

When a user selects a file and then clicks the button to upload it, the
resulting HTTP POST request is sent to a well-known n API gateway endpoint.
From there, API gateway interacts with a Lambda function that receives the
API request, extracts the uploaded file, and pushes that file to an S3 bucket.

When an object is written to the S3 bucket, a Lambda function is called to
invoke Textract.

This approach allows us to test the system by uploading files directly to S3
via CLI or console.  Also, this approach does not preclude us from exploring
pre-signed S3 URLs in the future.


## Consequences

Files that are uploaded must pass through API gateway and a Lambda function
prior to being written to S3.  This gives us control over file names and allows
us to manipulate or filter files prior to their being written to S3.  At the
same time, we're bottlenecked (processing, bandwidth) on API gateway and
Lambda whereas a pre-signed URL upload directly to S3 wouldn't have those
bottlenecks.
