# Northstar AI Personal Data Deletion Audit Agent

An evidence-driven, full-stack personal data deletion auditing system built for the **Northstar Shop challenge**. The project analyzes deletion requests across historical identity records, system activity logs, database snapshots, support records, and data retention policies to determine whether a user's personal data has been properly deleted.

The system produces structured, evidence-backed audit results, identifies unresolved deletion requirements and restoration risks, and generates reports for evaluation and submission. A React dashboard provides an interactive interface for investigating cases, exploring evidence, reviewing policy rules, and downloading generated artifacts.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Understanding the Output](#understanding-the-output)
- [Evaluation and Reports](#evaluation-and-reports)
- [Dashboard](#dashboard)
- [Troubleshooting](#troubleshooting)
- [Security and Privacy Considerations](#security-and-privacy-considerations)

---

## Project Overview

Personal data deletion is more complex than removing a single database record. A user's information may remain in historical records, backup snapshots, support systems, synchronization pipelines, or other systems that process personal data.

The Northstar AI Personal Data Deletion Audit Agent is designed to investigate these situations systematically.

For each audit case, the system examines the available evidence and applies deletion policy rules to determine the deletion status. When deletion cannot be conclusively verified, the system can identify outstanding issues, recommend remediation steps, and specify future verification checks.

The project combines a Python-based audit pipeline with a React dashboard and a Node.js development server.

### Objectives

- Resolve identities across historical email addresses, aliases, hashes, and stable user identifiers.
- Reconstruct relevant system activity at a specified audit timestamp.
- Evaluate available evidence against configured deletion policies.
- Identify incomplete deletion, active data flows, and potential backup restoration risks.
- Produce deterministic, consistently ordered audit steps.
- Evaluate results against the project's test and benchmark datasets.
- Provide an interactive dashboard for examining cases and generated reports.

> **Important:** The audit results depend on the available datasets, configured policies, and implemented verification logic. A generated status should not be interpreted as independent proof of deletion in a live production system unless the underlying evidence supports that conclusion.

---

## Key Features

### 1. Identity Resolution

Connects records that may refer to the same user by examining available identity references, including:

- Historical email addresses.
- Email aliases.
- SHA-256 email hashes.
- Stable `user_id` values.
- Identity references found in system change logs.

This helps the audit pipeline investigate records that might otherwise be missed when a user changes their email address or when systems store different identity representations.

### 2. Evidence-Driven Temporal Reconstruction

Analyzes the available system evidence in relation to each case's `audit_at` timestamp.

Supported evidence sources in the project include:

- System activity and change logs.
- SQLite database snapshots.
- JSON-based support records.
- Other configured dataset artifacts.

The audit should distinguish evidence relevant to the audit timestamp from events that occurred outside the applicable time window.

### 3. Policy Evaluation Engine

Uses `deletion_rules.csv` and the project's audit logic to evaluate required deletion treatments and identify potential problems, including:

- Data that still requires action.
- Permitted tombstone references.
- Active synchronization or recreation risks.
- Backup restoration paths.
- Verification requirements for deletion completion.

The exact behavior is determined by the rules and implementation included in the repository.

### 4. Deterministic Step Ordering

Organizes audit findings, remediation actions, and verification steps according to the project's phase and operation priority rules.

Steps are renumbered consecutively, starting from `1`, to produce predictable output and support sequence-order validation.

### 5. Full-Stack Dashboard

The dashboard provides a user interface for exploring the audit pipeline's results.

Depending on the configured project components, it includes:

- Case investigation.
- Evidence timeline exploration.
- Policy rule inspection.
- Evaluation-suite access.
- Token usage analysis.
- CSV and ZIP download options.

### 6. Evaluation and Submission Artifacts

The project includes scripts for evaluating audit output and packaging deliverables.

Expected artifacts include:

- `output.csv`
- `evaluation/evaluation_report.md`
- `evaluation/usage_report.md`

These files are generated or validated by the project's scripts, depending on the available input data and configuration.

---

## How It Works

The general workflow is:

1. **Prepare the dataset:** Load the supplied data or generate the challenge dataset.
2. **Resolve identities:** Associate historical identifiers with the relevant user or case.
3. **Reconstruct evidence:** Examine relevant records and system events as of the audit timestamp.
4. **Apply policies:** Compare the available evidence with the configured deletion requirements.
5. **Determine status:** Classify the case based on the implemented rules and available evidence.
6. **Generate steps:** Produce findings, remediation actions, and verification steps where appropriate.
7. **Evaluate results:** Run the evaluation suite and validate the generated output.
8. **Package deliverables:** Generate the submission archive and reports.
9. **Inspect results:** Use the dashboard to investigate cases and review available artifacts.

### High-Level Architecture

```text
                  Dataset and Policy Files
                            |
                            v
                Python Audit Pipeline
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        Identity        Evidence        Policy
        Resolution      Analysis        Evaluation
             |              |              |
             +--------------+--------------+
                            |
                            v
                    Audit Results
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
         output.csv     Evaluation       Reports and
                        Results          Submission ZIP
                            |
                            v
                   React Dashboard
                            |
                            v
                  Interactive Investigation
```

The diagram represents the intended workflow. Actual execution paths depend on the source files and configuration included in the repository.

---

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Audit pipeline | Python | Dataset processing, audit execution, and evaluation |
| Python environment | `uv` | Python dependency and virtual environment management |
| Dashboard | React | Interactive user interface |
| Frontend tooling | Vite | Development and frontend build tooling |
| Backend server | Node.js and Express | Serves application endpoints |
| Type checking | TypeScript | Static checks for application code |
| UI styling | Tailwind CSS | Dashboard styling |
| Icons | Lucide React | Interface icons |
| Motion | Motion | UI animations |
| AI integration dependency | Google Gen AI SDK | Provides Gemini API integration capabilities where implemented |
| Audit evidence storage | CSV, JSON, SQLite | Structured policy and evidence data |

**AI integration note:** Including the Google Gen AI SDK does not necessarily mean every audit operation uses an AI model. Whether Gemini is invoked depends on the actual application code and execution path.

---

## Project Structure

The following is a representative layout of the project. Actual filenames and directories may vary slightly depending on the supplied archive.

```text
northstar-ai-personal-data-deletion-audit-agent/
├── README.md
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
├── server.ts
├── .env.example
│
├── scripts/
│   ├── generate_dataset.py
│   ├── run_audit.py
│   ├── evaluate.py
│   └── package_submission.py
│
├── evaluation/
│   ├── evaluation_report.md
│   └── usage_report.md
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── App.tsx
│   └── main.tsx
│
├── data/
│   └── ...
│
└── output/
    └── ...
```

### Important files

| File | Purpose |
|---|---|
| `package.json` | Defines Node.js dependencies and npm scripts |
| `uv.lock` | Locks Python dependency versions, if included |
| `pyproject.toml` | Defines Python project metadata and dependencies, if included |
| `.env.example` | Example environment configuration |
| `server.ts` | Node.js/Express application server |
| `scripts/generate_dataset.py` | Generates the challenge dataset, if required |
| `scripts/run_audit.py` | Executes the audit pipeline |
| `scripts/evaluate.py` | Evaluates generated audit results |
| `scripts/package_submission.py` | Packages submission artifacts |
| `deletion_rules.csv` | Defines deletion policy rules, wherever located in the repository |
| `output.csv` | Generated audit results |

Some entries above are conditional on the supplied project layout. Check the repository before assuming every file or directory is present.

---

## System Requirements

This guide targets Ubuntu Linux.

Install or prepare the following:

- Python 3.10 or newer, subject to the Python version required by the project.
- `uv` for Python environment management.
- Node.js 22.12.0 or newer for Vite 8.
- npm, normally distributed with Node.js.
- An internet connection for installing dependencies.

Check whether the required tools are available:

```bash
python3 --version
uv --version
node --version
npm --version
```

If a command is not found, install the missing tool before continuing.

---

## Installation

### Step 1: Open the Project Directory

If you downloaded the project as a ZIP archive, navigate to the directory containing the extracted files.

You should be able to locate `package.json` and the project scripts. The Python setup files, such as `pyproject.toml`, should also be present if the repository uses `uv` for dependency management.

If you already extracted the project, simply change into that directory.

### Step 2: Install Python and uv

Check your Python installation:

```bash
python3 --version
```

Install `uv` using its official installation instructions if it is not already installed:

[Official uv documentation](https://docs.astral.sh/uv/)

After installation, verify it:

```bash
uv --version
```

### Step 3: Set Up the Python Environment

From the project root, inspect the Python configuration files:

```bash
ls pyproject.toml uv.lock requirements.txt
```

This command may report missing files because not every project uses all three formats.

#### If the project contains `pyproject.toml`

Run:

```bash
uv sync
```

This creates or updates the project's virtual environment and installs the dependencies declared in its Python project configuration.

If `uv.lock` is included and is compatible with the project configuration, `uv sync` uses the lockfile to resolve the intended dependency versions.

#### If the project has no `pyproject.toml`

Do not run `uv sync` blindly. Check whether the repository includes `requirements.txt` or another Python dependency specification.

If it contains `requirements.txt`, you can create a virtual environment and install the listed dependencies:

```bash
uv venv
uv pip install -r requirements.txt
```

If neither file exists, inspect the Python imports and project instructions to determine the dependencies required by the supplied code.

### Step 4: Install Node.js Dependencies

Check the Node.js version:

```bash
node --version
```

For Vite 8, use Node.js **22.12.0 or newer**.

If Node.js is too old, upgrade it before installing the JavaScript dependencies.

Then install the project packages:

```bash
npm install
```

If you encounter an `ERESOLVE` error related to Vite and esbuild, check that `package.json` declares a compatible esbuild version:

```json
"esbuild": "^0.28.0"
```

Then, if necessary, regenerate the dependency installation:

```bash
rm -rf node_modules
rm -f package-lock.json
npm install
```

### Step 5: Configure Environment Variables

Check whether the repository contains an example environment file:

```bash
ls -la .env.example
```

If it exists, copy it:

```bash
cp .env.example .env
```

Open the file for editing:

```bash
nano .env
```

The project may define variables such as:

```dotenv
GEMINI_API_KEY=
DATASET_DIR=
OUTPUT_DIR=
GEMINI_MODEL=
```

Set the values according to the project's implementation and the actual dataset and output locations.

For example, if the code expects a Gemini API key and you intend to use its Gemini integration, provide your own key:

```dotenv
GEMINI_API_KEY=your_actual_api_key
```

Do not commit `.env` to a public repository or share your API key.

**Important:** These variable names are examples from the project configuration. Confirm that the Python scripts and server actually read them. A variable being present in `.env` does not mean every component uses it.

If the audit pipeline is deterministic and does not call Gemini, a Gemini API key may not be necessary to run that pipeline.

---

## Running the Project

Run the following commands from the project root.

### Step 1: Generate the Dataset

If the supplied dataset must be generated, run:

```bash
uv run python scripts/generate_dataset.py
```

This invokes the dataset-generation script using the project's Python environment.

If the original dataset is already supplied and the script is not intended to overwrite it, inspect the script before running it.

### Step 2: Run the Audit Pipeline

Execute:

```bash
uv run python scripts/run_audit.py
```

The audit script processes the configured data and generates audit results.

Check the terminal output for errors and warnings. After execution, locate the generated `output.csv` file and any other artifacts produced by the script.

If the project does not have a configured `uv` project, use the Python environment created in the earlier setup step:

```bash
.venv/bin/python scripts/run_audit.py
```

The exact command depends on how the Python environment and dependencies are configured.

### Step 3: Evaluate the Results

Run:

```bash
uv run python scripts/evaluate.py
```

The evaluation script checks the audit results against the project's evaluation logic.

Review the output for:

- Case-level accuracy.
- Audit step metrics.
- Sequence ordering.
- Validation failures.
- Edge-case benchmarks.

The actual metrics depend on the generated output, available test data, and evaluation implementation.

### Step 4: Generate Submission Artifacts

Run:

```bash
uv run python scripts/package_submission.py
```

This script packages the files defined by the submission workflow.

Expected deliverables may include:

- `code.zip`
- `output.csv`
- `evaluation/evaluation_report.md`
- `evaluation/usage_report.md`

Check the script's output to confirm the actual destinations of the generated files.

### Step 5: Start the Web Application

Start the development server:

```bash
npm run dev
```

The project's `dev` script is configured to run:

```bash
tsx server.ts
```

If startup succeeds, the terminal should show the server's listening address or port.

Open the address printed by the server in your browser.

For example, if the application is listening on port `3000`, visit:

**http://localhost:3000**

If the server uses a different port, use that port instead.

Keep the terminal open while using the application. To stop the development server, press:

```text
Ctrl + C
```

### Quick Start: Commands in Order

Once all dependencies and configuration are in place, the complete workflow is:

```bash
# 1. Install Python dependencies
uv sync

# 2. Install JavaScript dependencies
npm install

# 3. Generate the dataset, if required
uv run python scripts/generate_dataset.py

# 4. Execute the audit
uv run python scripts/run_audit.py

# 5. Evaluate audit results
uv run python scripts/evaluate.py

# 6. Package submission artifacts
uv run python scripts/package_submission.py

# 7. Start the web application
npm run dev
```

Run `uv sync` only if the project has the appropriate Python project configuration. If it does not, follow the alternative Python installation instructions above.

You do not need to rerun the dataset-generation, audit, evaluation, and packaging steps every time you start the dashboard unless you have changed the input data or need fresh results.

---

## Understanding the Output

The primary audit output is:

```text
output.csv
```

The expected submission format contains three columns:

```csv
case_id,deletion_status,steps_json
```

The challenge specification describes an expected result of **518 data rows**, sorted by `case_id` in ascending order.

Confirm the row count and schema after running the pipeline rather than assuming the expected result was generated successfully.

### Output Columns

| Column | Description |
|---|---|
| `case_id` | Identifier for the audit case |
| `deletion_status` | Resulting deletion classification |
| `steps_json` | JSON-encoded list of findings, remediation actions, or verification steps |

### Deletion Statuses

#### `COMPLETE`

Indicates that the audit logic considers deletion demonstrably verified based on the evidence and rules it evaluates.

The output is expected to include verification steps that cite relevant evidence identifiers.

#### `INCOMPLETE`

Indicates that deletion requirements remain unresolved or the available evidence identifies risks requiring further action.

Potential reasons include:

- Remaining data requiring deletion.
- Active synchronization flows that may recreate data.
- Backup restoration risks.
- Insufficient evidence to verify completion.

The output is expected to contain relevant findings, remediation actions, and future verification steps.

#### `NOT_APPLICABLE`

Indicates that the user did not request deletion for the relevant case.

For these records, the expected `steps_json` value is an empty JSON array:

```json
[]
```

### Validate the CSV

After the audit finishes, inspect the file:

```bash
head -n 5 output.csv
```

Count the data rows, excluding the header:

```bash
python3 -c "import csv; print(sum(1 for _ in csv.DictReader(open('output.csv', newline='', encoding='utf-8'))))"
```

The expected count is `518` when using the complete challenge dataset.

To check the column names:

```bash
python3 -c "import csv; f=open('output.csv', newline='', encoding='utf-8'); print(next(csv.reader(f)))"
```

Expected column names:

```text
['case_id', 'deletion_status', 'steps_json']
```

The evaluation script should be treated as the primary validation mechanism for more detailed requirements, including ordering and case-specific correctness.

---

## Evaluation and Reports

The project provides scripts for checking the audit output and preparing submission artifacts.

### Evaluation report

Expected location:

```text
evaluation/evaluation_report.md
```

The report may contain:

- Case accuracy.
- Step-level metrics.
- Sequence-order validation.
- Edge-case benchmark results.
- Other validation results implemented by the evaluation script.

### Usage report

Expected location:

```text
evaluation/usage_report.md
```

The report may describe:

- Model token usage.
- Model-call breakdown.
- Estimated API costs.

The exact contents depend on the reporting implementation. If the audit runs without any model calls, model usage and cost fields may be empty, zero, or otherwise inapplicable.

### Submission archive

Expected filename:

```text
code.zip
```

The archive should contain the files selected by `scripts/package_submission.py`.

Inspect the script and its output to confirm which source files, configuration files, reports, and other artifacts are included.

---

## Dashboard

The React dashboard provides an interactive way to inspect generated audit results.

Depending on the implementation, you can use it to:

- Investigate individual audit cases.
- Explore the evidence associated with a case.
- Review deletion policy rules.
- View evaluation information.
- Examine token usage and model-related metrics.
- Download generated CSV or ZIP artifacts.

### Start the dashboard

From the project root:

```bash
npm run dev
```

Open the local URL displayed in the terminal.

If the application starts on port `3000`, use:

```text
http://localhost:3000
```

### Development build

To check and build the frontend:

```bash
npm run build
```

This runs the configured TypeScript and Vite build commands.

To run TypeScript checks without producing a build:

```bash
npm run lint
```

**Note:** The exact build output and production startup behavior depend on `tsconfig.json`, `vite.config.ts`, and `server.ts`. If the build fails, review the first TypeScript or Vite error and resolve it before proceeding.

---

## Troubleshooting

### 1. `uv: command not found`

Install `uv` using the official documentation:

https://docs.astral.sh/uv/

Restart your terminal if required, then verify:

```bash
uv --version
```

### 2. `npm: command not found` or an incompatible Node.js version

Check:

```bash
node --version
npm --version
```

Install a supported Node.js release if either command is unavailable or Node.js is too old for Vite 8.

### 3. `ERESOLVE unable to resolve dependency tree`

This may occur when the installed esbuild version does not satisfy Vite's peer dependency requirements.

Check `package.json` for:

```json
"esbuild": "^0.28.0"
```

Then reinstall dependencies if needed:

```bash
rm -rf node_modules
rm -f package-lock.json
npm install
```

### 4. `ModuleNotFoundError` when running a Python script

Make sure the Python dependencies have been installed.

For a project configured with `uv`:

```bash
uv sync
```

Then rerun the script:

```bash
uv run python scripts/run_audit.py
```

If the dependency is missing from the project's configuration, add it through the project's dependency-management workflow rather than installing packages randomly into the system Python environment.

### 5. `FileNotFoundError` or missing dataset errors

Check that the required dataset exists and that the configured paths point to the correct locations.

Inspect the project configuration and, if necessary, run:

```bash
uv run python scripts/generate_dataset.py
```

Only generate the dataset if that script is appropriate for your current data.

### 6. `GEMINI_API_KEY` errors

If the application actually invokes Gemini, verify that the API key is configured in the environment expected by that component.

If you are only running a deterministic audit pipeline that does not use Gemini, first identify which script is raising the error. Do not assume the entire pipeline requires an API key just because the SDK is installed.

### 7. The server starts, but the browser cannot connect

Check the terminal for the listening port and any startup errors.

Confirm that:

- The development server is still running.
- You are using the correct local port.
- No other process is blocking the selected port.
- The server is bound to an address accessible from your browser.

### 8. The dashboard opens, but the data is missing

Check whether the audit pipeline has generated its expected outputs.

Run:

```bash
uv run python scripts/run_audit.py
```

Then inspect the server's data-loading logic and configured dataset/output paths. The dashboard can only display data that its implemented backend and frontend actually load.

### 9. `npm run build` fails

Run:

```bash
npm run lint
```

Read the first error carefully. It may indicate a TypeScript issue, missing source file, incorrect import, or a mismatch between the server's output path and the configured build.

Do not assume every build error is a dependency problem.

---

## Security and Privacy Considerations

Because this project evaluates personal data deletion, security and evidence integrity are important.

- Do not commit API keys or other secrets to source control.
- Keep `.env` files private.
- Use synthetic or appropriately authorized datasets during development.
- Avoid exposing personal data through dashboard logs, downloads, or error messages.
- Restrict access to generated audit reports where they contain sensitive information.
- Preserve evidence identifiers and timestamps needed to explain audit decisions.
- Verify backup and synchronization behavior before concluding that deletion is complete.
- Treat audit output as a decision-support artifact whose reliability depends on the quality of its evidence and rules.

A production deployment should additionally implement appropriate authentication, authorization, secure transport, access logging, retention controls, and operational monitoring.

---

## License and Usage

This project was developed for the Northstar Shop personal data deletion audit challenge.

Refer to the repository's license and challenge requirements for redistribution, submission, and reuse terms.

---

## Summary

The Northstar AI Personal Data Deletion Audit Agent combines a Python audit pipeline, policy-driven evidence analysis, deterministic result generation, automated evaluation, and a React-based dashboard.

The recommended workflow is:

1. Install the Python and Node.js dependencies.
2. Configure the required environment variables and dataset paths.
3. Generate or prepare the dataset.
4. Run the audit pipeline.
5. Evaluate the results.
6. Package the submission artifacts.
7. Launch the dashboard with `npm run dev`.
8. Inspect the audit cases and generated reports.