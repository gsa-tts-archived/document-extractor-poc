# 6. API Gateway, Lambda, DynamoDB, and SQS

Date: 2025-03-05

## Status

Accepted.

## Context

There are different ways to process, run, and store data.  You can use servers or "serverless" services.

## Decision

We will use serverless options whenever possible.

This means API Gateway, Lambda, DynamoDB, and SQS to name some of the services.

## Consequences

This means we will only incur a costs when the application is actively working on data.
