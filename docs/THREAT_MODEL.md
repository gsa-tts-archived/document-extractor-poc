# Document Extractor

This document uses [`threatdown`](https://threatdown.xyz) to help create the final document.

Run `npx threatdown ./THREAT_MODEL.template.md --output ./THREAT_MODEL.md` to create it.  Don't forget to run this
command and commit the final document.

Do not edit `THREAT_MODEL.md` directly.

## Introduction

The threat model is intended to ensure that the application is developed with security built-in from the beginning and
in an ongoing way.  By documenting potential threats and assets, along with countermeasures and mitigation actions
explicitly, better and more informed decisions can be made for improved security.

This document is stored in revision control along with the application code so that it is highly visible and accessible
to the individuals doing development and deployment and can be modified in concert with the code.

## Entry Points

1. asdf

## Assets

1. asdf

## Threats

<!-- ```threatdown
__DDOS the application__
``` -->
```mermaid
flowchart TD
  A0{DDOS the application}:::objective
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  linkStyle  stroke:#4a3dff,stroke-width:2px
```
