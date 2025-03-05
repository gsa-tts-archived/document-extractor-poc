# 3. User Interface to S3 Data Flow

Date: 2025-02-14

## Status

Accepted.

## Context

When a user visits the user interface (UI), they see a form allowing them to
select a file and a button to upload it.

How are files uploaded?  When a user selects a file on their local system and
clicks submit to upload it, what actually happens?  How does that file get to
S3?

## Decision

When a user selects a file and then clicks the button to upload it, the
resulting HTTP POST request is sent to a well-known API Gateway endpoint.
From there, API Gateway interacts with a Lambda function that receives the
API request, extracts the uploaded file, and pushes that file to an S3 bucket.

This approach allows us to test the system by uploading files directly to S3
via CLI or console.  Also, this approach does not preclude us from exploring
pre-signed S3 URLs in the future.


## Consequences

Files that are uploaded must pass through API Gateway and a Lambda function
prior to being written to S3.  This gives us control over file names and allows
us to manipulate or filter files prior to their being written to S3.  At the
same time, we're bottlenecked (processing, bandwidth) on API Gateway and
Lambda whereas a pre-signed URL upload directly to S3 wouldn't have those
bottlenecks.
