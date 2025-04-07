# 11. Application Context in Python Code

Date: 2025-04-07

## Status

Accepted.

## Context

We need a way to test code without calling external services by swapping out implementations while in a test context.
For example, we do not want to call the real OCR service or ReST server while unit testing the code around that external
call.

## Decision

We've added the concept of an "application context" where one registers implementations for interfaces.  When the real
code executes, a real implementation is registered but a fake mock is registered during unit tests.

The implementation is either injected or accessed from the application context (i.e. dependency injection) and used.
The code using the implementation is supposed to know nothing about what specific implementation is being used.

## Consequences

Using the application context adds some complexity because its not built-in functionality to Python.  A new engineer to
the project will need to learn the concept.  Granted, it isn't a lot of code.

On the other hand, this will introduce better separation of concerns and testability by forcing us to think about when
we will need different implementations at different abstraction levels.
