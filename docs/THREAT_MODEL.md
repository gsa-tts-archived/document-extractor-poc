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

1. Website.  Users interact with our application through the website.  Anyone can interact with the website.
2. API.  Users can interact with the API through the website or directly.
3. AWS console.  AWS credentials can be used to log into the AWS console directly and access data, code, and
   configuration.
4. S3 bucket document bucket.  The S3 bucket stores the documents and is written to by the application.

## Assets

1. The code itself.
2. The website.
3. Documents uploaded to the application.
4. The extracted data from the documents.

## Threats

<!-- ```threatdown
__Make the application unavailable__
- Harness a botnet and throw a bunch of traffic at the website or API.
  - [x] AWS has built-in DDOS mitigations.
  - [ ] Pay for AWS Shield Advaced that provides additional protections.
- Change the code to become inoperable.
  - Have access to GitHub.
    - [x] GSA requires a user have a GSA e-mail, which requires a background check.
    - [x] GitHub accounts in the GSA GitHub organization requires two-factor authentication.
  - Have access to AWS.
    - [x] Protected by two-factor authentication and only specific individuals are given access.
  - Suppy chain attack.
    - [x] We use well known dependencies distributed through well known distribution channels like PyPi and NPM.
    - [ ] Improve dependabot to automatically update dependencies.
    - [ ] Do SCA scanning.
``` -->
```mermaid
flowchart TD
  A0{Make the application unavailable}:::objective
    A0---B1(((OR))):::booleanOr
      B1---C1(Harness a botnet and throw a bunch of traffic at the website or API.):::condition
        C1---D1(((OR))):::booleanOr
          D1-- mitigated by ---E1(AWS has built-in DDOS mitigations.):::condition
          D1-. mitigated by .-E2(Pay for AWS Shield Advaced that provides additional protections.):::condition
      B1---C2(Change the code to become inoperable.):::condition
        C2---D2(((OR))):::booleanOr
          D2---E3(Have access to GitHub.):::condition
            E3---F1(((OR))):::booleanOr
              F1-- mitigated by ---G1(GSA requires a user have a GSA e-mail, which requires a background check.):::condition
              F1-- mitigated by ---G2(GitHub accounts in the GSA GitHub organization requires two-factor authentication.):::condition
          D2---E4(Have access to AWS.):::condition
            E4-- mitigated by ---F2(Protected by two-factor authentication and only specific individuals are given access.):::condition
          D2---E5(Suppy chain attack.):::condition
            E5---F3(((OR))):::booleanOr
              F3-- mitigated by ---G3(We use well known dependencies distributed through well known distribution channels like PyPi and NPM.):::condition
              F3-. mitigated by .-G4(Improve dependabot to automatically update dependencies.):::condition
              F3-. mitigated by .-G5(Do SCA scanning.):::condition
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  style E1 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E2 stroke:#4a3dff,stroke-width:2px
  style G1 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style G2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style G3 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style G4 stroke:#4a3dff,stroke-width:2px
  style G5 stroke:#4a3dff,stroke-width:2px
  linkStyle 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17 stroke:#4a3dff,stroke-width:2px
```


<!-- ```threatdown
__Steal the raw, uploaded documents__
- stuff
``` -->
```mermaid
flowchart TD
  A0{Steal the raw, uploaded documents}:::objective
    A0---B1(stuff):::condition
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  linkStyle 0 stroke:#4a3dff,stroke-width:2px
```


<!-- ```threatdown
__Steal the extracted data__
- stuff
``` -->
```mermaid
flowchart TD
  A0{Steal the extracted data}:::objective
    A0---B1(stuff):::condition
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  linkStyle 0 stroke:#4a3dff,stroke-width:2px
```


<!-- ```threatdown
__Vandalize the website__
- stuff
``` -->
```mermaid
flowchart TD
  A0{Vandalize the website}:::objective
    A0---B1(stuff):::condition
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  linkStyle 0 stroke:#4a3dff,stroke-width:2px
```
