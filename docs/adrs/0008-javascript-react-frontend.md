# 2. Use JavaScript and React Frontend

Date: 2025-03-05

## Status

Accepted.

## Context

We want a website and there are many ways to do it.

1. Raw HTML, CSS, and JavaScript.
2. JavaScript with some other reactive framework (e.g. Angular).
3. Involve TypeScript.
4. Other programming languages being transpiled to JavaScript (e.g. PyScript).

## Decision

We'll be using JavaScript with React for frontend development.

We went away from option 1 because we quicly outgrew this option being effective.  React is more popular than Angular,
so we decided against option 2.  We didn't pick TypeScript because there was already a decent amount of pure JavaScript
code.  All the options covered by option 4 are very esoteric.

## Consequences

JavaScript is not a typed language.  We may revisit this decision and adopt TypeScript.
