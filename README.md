# Document Extractor Proof of Concept

Public Benefits Studio's Document Extractor to automate document data extraction with AI and OCR.

## Using and Running

Using your browser of choice, navigate to the CloudFront distribution URL to start using.

## Development

### Requirements to Deploy

The requirements needed to deploy are...

- [Python](https://docs.python-guide.org/starting/installation/).
- [uv](https://docs.astral.sh/uv/).
- [Terraform](https://www.terraform.io).
- [Node.js](https://nodejs.org).
- An [AWS](https://aws.amazon.com/) account.

### Deploying

You can mimic the steps in our [Continuous Delivery GitHub Action](.github/workflows/cd.yml).

The basic steps to accomplish this are...
1. Build the backend.
2. Build the frontend.
3. Deploy using the Infrastructure as Code (IaC).

### Building

#### Backend

To build the backend, execute...

```shell
cd ./backend/
uv sync
uv run build.py
```

The built artifact is `backend/dist/lambda.zip`.

#### Frontend

To build the frontend, execute...

```shell
cd ./ui/
npm ci
npm run build
```

The built artifact is in `ui/dist/`.

### Additional Requirements to Develop

The additional requirements needed to contribute towards development are...

- [Pre-Commit](https://pre-commit.com).

### Pre-Commit Hooks

We use [`pre-commit`](https://pre-commit.com) to run [some hooks](.pre-commit-config.yaml) on every commit.  These
hooks do linting to ensure things are in a good spot before a commit is made.  Please install `pre-commit` and then
install the hooks.

```shell
pre-commit install
```

Most of the time any errors encountered by pre-commit are automatically fixed.  Run `git status` to see the fixed files,
run `git add .` to add the fixes, and rerun the commit.  You will need to manually fix any errors that are not
automatically fixed.
