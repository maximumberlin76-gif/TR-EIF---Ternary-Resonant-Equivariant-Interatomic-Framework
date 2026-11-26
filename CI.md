
# TR-EIF Continuous Integration

## 1. Purpose

This document records the committed GitHub Actions execution contracts for the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The repository About describes a mathematical and computational framework integrating balanced ternary -1/0/1 dynamics, nonlinear resonance, equivariant mappings, and interatomic system modeling. The CI configuration exercises defined parts of that framework through package imports, structured-output checks, numerical tests, invariant tests, and schema qualification.

The authoritative executable definitions are the files under `.github/workflows/`. Test-specific input domains, numeric thresholds, provenance, and evidence classes remain defined by the tests, benchmarks, schemas, and validation documents themselves.

## 2. Workflow Inventory

| GitHub Actions workflow | File | Trigger | Role |
| --- | --- | --- | --- |
| TR-EIF Python CI | `.github/workflows/python-tests.yml` | Push to `main`, pull request to `main`, manual dispatch | Package smoke test, structured output, deterministic validation bench, complete pytest suite |
| TR-EIF Schema Validation | `.github/workflows/schema-validation.yml` | Push to `main`, pull request to `main`, manual dispatch | Root and configuration schema-contract tests |
| TR-EIF Markdown Validation | `.github/workflows/markdown-validation.yml` | Manual dispatch | Repository Markdown-format contract |
| TR-EIF Repository Naming Validation | `.github/workflows/repository-naming-validation.yml` | Manual dispatch | Repository-controlled path and filename contracts |
| TR-EIF One-File Editorial Cleanup | `.github/workflows/tr-eif-editorial-cleanup.yml` | Manual dispatch | Author-reviewed editorial audit and separately authorized modification operations |

The first two workflows are automatically triggered by the configured `main` events. The other three require explicit dispatch.

## 3. Python CI Environment

The workflow uses `ubuntu-latest` runners and Python `3.12` through `actions/setup-python@v5`.

Each Python CI job checks out the repository using `actions/checkout@v4`, upgrades pip, and installs the editable package with its development dependencies using `python -m pip install -e ".[dev]"`.

The package declares Python `>=3.11` in `pyproject.toml`; the CI workflow selects Python `3.12` for its configured runner.

The four Python CI jobs are separate GitHub Actions jobs and have independent conclusions.

## 4. Python CI Job Contracts

### TR-EIF Smoke Test

The smoke job executes `python -m compileall -q src/tr_eif` and imports the public package layers:

- `tr_eif`;
- `tr_eif.energy`;
- `tr_eif.equivariant`;
- `tr_eif.flibe`;
- `tr_eif.geometry`;
- `tr_eif.graph`;
- `tr_eif.md`;
- `tr_eif.multiscale`;
- `tr_eif.observables`;
- `tr_eif.resonance`;
- `tr_eif.ternary`.

The job reports Python compilation and import execution for the checked-out revision.

### TR-EIF Structured Output

The structured-output job runs:

- `tests/determinism/test_trace_file_export.py`;
- `tests/invariants/test_trace_schema_contract.py`.

Its command is `python -m pytest tests/determinism/test_trace_file_export.py tests/invariants/test_trace_schema_contract.py -q --junitxml=artifacts/structured-output.xml`.

### TR-EIF Deterministic Validation Bench

The deterministic validation job executes the following test directories:

- `tests/determinism/`;
- `tests/equivariance/`;
- `tests/conservation/`;
- `tests/numerical/`.

Its command is `python -m pytest tests/determinism tests/equivariance tests/conservation tests/numerical -q --junitxml=artifacts/deterministic-validation-bench.xml`.

The directory selection defines this job's scope. Tests in `tests/integration/` and `tests/invariants/` are also covered by the complete self-test job.

### TR-EIF Self Test

The complete repository test job runs `python -m pytest -q --junitxml=artifacts/full-self-test.xml` from the repository root.

Its collection is governed by `pyproject.toml` and the committed tests under `tests/`. In particular, the configured pytest test path is `tests`.

## 5. Schema Validation

The schema workflow uses `ubuntu-latest`, Python `3.12`, and the same editable development installation.

It runs exactly these two committed test modules:

- `tests/invariants/test_configuration_schema_contract.py`;
- `tests/invariants/test_root_schema_set_contract.py`.

The command is `python -m pytest tests/invariants/test_configuration_schema_contract.py tests/invariants/test_root_schema_set_contract.py -q --junitxml=artifacts/schema-validation.xml`.

The root schema inventory and each schema's semantic requirements remain defined in `schemas/` and the associated tests.

## 6. Test Reports and Artifacts

| Workflow job | Uploaded artifact name | JUnit XML path |
| --- | --- | --- |
| TR-EIF Structured Output | `tr-eif-structured-output-report` | `artifacts/structured-output.xml` |
| TR-EIF Deterministic Validation Bench | `tr-eif-deterministic-validation-report` | `artifacts/deterministic-validation-bench.xml` |
| TR-EIF Self Test | `tr-eif-full-self-test-report` | `artifacts/full-self-test.xml` |
| TR-EIF Complete Schema Validation | `tr-eif-schema-validation-report` | `artifacts/schema-validation.xml` |

The four report-upload steps use `if: always()`. Their configuration also uses `if-no-files-found: ignore`; artifact presence must therefore be checked on the individual run.

The smoke job has no configured JUnit artifact. The manually dispatched Markdown and naming validations report through their job logs. The editorial workflow's `audit` operation has its own report artifact, documented separately below.

The current Python and schema workflows do not configure a standalone branch-coverage report, a combined cross-workflow report, or a performance-profile artifact. Performance and physical-observable outputs are defined by their respective committed benchmark programs and qualification tests.

## 7. Markdown Validation

`TR-EIF Markdown Validation` traverses committed Markdown files and validates:

- UTF-8 decoding and nonempty content;
- a level-one heading as the first nonempty line;
- absence of trailing whitespace;
- balanced fenced-block delimiters;
- bare triple-backtick fence delimiters, without language suffixes;
- removal of service-specific writing markers, raw LaTeX expressions, and unresolved editorial marker tokens;
- canonical balanced ternary notation `-1/0/1` and `{-1, 0, 1}`.

It is manually dispatched from GitHub Actions. The `CI.md` file is covered by this validator when committed because the validation traverses Markdown files throughout the repository.

## 8. Repository Naming Validation

`TR-EIF Repository Naming Validation` is manually dispatched. Its checks cover:

- whitespace-free paths under `docs/`, `src/`, `tests/`, and `.github/workflows/`;
- lowercase snake_case documentation directory and regular Markdown names under `docs/`;
- contiguous numbered volume directories and chapter files;
- lowercase snake_case Python package and module names;
- `test_`-prefixed Python test module names;
- lowercase kebab-case workflow filenames.

The repository-root file `CI.md` is outside the validator's documentation-filename rule, which applies to the `docs/` tree.

## 9. Author-Reviewed Editorial Workflow

`TR-EIF One-File Editorial Cleanup` is a separate manually dispatched workflow with three declared operations:

- `audit`: produces `editorial-audit.json` and `editorial-audit.md`, uploaded as `tr-eif-editorial-audit`;
- `apply`: takes a single existing repository-relative file, its exact prior SHA-256 digest, and an author-reviewed array of exact text replacements;
- `finalize`: verifies its required confirmation and successful independent Python/schema runs for the selected HEAD, then attempts to delete the temporary workflow using the configured token.

The `apply` operation checks the requested preconditions, runs the complete Python test suite, and is configured to commit and push the single approved edit to `main`.

The `finalize` operation requires `EDITORIAL_AUDIT_COMPLETE` and the configured `TR_EIF_WORKFLOW_TOKEN` secret for its deletion step.

These are repository-mutating operations. Ordinary manual file creation and full-file replacement are performed directly in GitHub's file editor; using `audit` does not authorize `apply` or `finalize`.

## 10. Local Reproduction

Run the following commands from the repository root in an environment with Python `3.12`, matching the configured CI interpreter:

1. Install the development package: `python -m pip install -e ".[dev]"`.
2. Compile package modules: `python -m compileall -q src/tr_eif`.
3. Run the full test suite: `python -m pytest -q`.
4. Run the deterministic validation selection: `python -m pytest tests/determinism tests/equivariance tests/conservation tests/numerical -q`.
5. Run structured-output tests: `python -m pytest tests/determinism/test_trace_file_export.py tests/invariants/test_trace_schema_contract.py -q`.
6. Run schema-contract tests: `python -m pytest tests/invariants/test_configuration_schema_contract.py tests/invariants/test_root_schema_set_contract.py -q`.

A local run should record its interpreter version, installed dependencies, repository revision, command, exit status, and relevant output. Differences between local execution and GitHub-hosted execution remain visible as separate evidence records.

## 11. GitHub Actions Execution and Failure Investigation

For automatically configured workflows, inspect the `main` push or pull-request run. For a manual check, open the repository's **Actions** tab, select the workflow, choose **Run workflow**, and select the intended branch and revision available in the GitHub interface.

For each run, record:

- repository and full commit SHA;
- workflow name and workflow file;
- triggering event and branch or pull request;
- GitHub Actions run identifier and run URL;
- job names and individual conclusions;
- test summary, including failures and warnings;
- artifact names and available JUnit XML reports;
- runner/interpreter details where they affect the result.

When a job fails, inspect the first reported failing command, the pytest failure details if applicable, and the generated JUnit XML if available. A later successful run must be associated with its own exact commit SHA; results from different revisions remain distinct records.

An uploaded artifact and a successful job conclusion are independent pieces of run metadata. The workflow log and artifact contents provide the evidence for a particular execution.

## 12. Scientific and Architectural Evidence Boundaries

TR-EIF separates the following record types:

- retained balanced ternary execution state and pending target;
- continuous resonance state and descriptors;
- E(3)-equivariant representations;
- conservative energy, force, and stress observables;
- MD and multiscale execution results;
- material-specific experimental and computational sources;
- benchmark qualification and CI job conclusions.

The active-neutral state `0` retains its execution semantics; it is independent of missing inputs, test outcomes, and scientific evidence status. Opposite committed ternary transitions remain neutral-mediated as defined by the ternary execution contracts.

A CI result is associated with the declared test inputs, operations, tolerances, and exact revision. Source provenance, physical-state correspondence, uncertainty handling, and interpretation remain under their separately defined scientific contracts and author-controlled reporting.

## 13. Maintenance and Revision Discipline

Changes to CI behavior are made in `.github/workflows/` and the associated test/configuration files. This document records their currently configured behavior; editing `CI.md` alone does not modify any workflow.

For manually entered repository changes, use one file per step, preserve the complete target file when replacing it, record the commit SHA, and inspect the resulting configured CI jobs. Manual-only workflows must be deliberately dispatched when their checks are required.

Documentation, benchmark, schema, and scientific-claim revisions retain their original evidence identities. The qualification state of an artifact follows the committed test and workflow evidence for that artifact.

## 14. Related Repository Documents

- `README.md`: framework identity and implemented layers.
- `pyproject.toml`: package metadata, dependencies, pytest and coverage configuration.
- `docs/architecture/framework_architecture.md`: cross-layer architectural contract.
- `docs/architecture/determinism_contract.md`: determinism and replay contract.
- `docs/validation/invariant_validation_plan.md`: invariant requirements.
- `docs/validation/numerical_validation_plan.md`: numerical qualification requirements.
- `docs/validation/reproducibility_plan.md`: reproducibility and provenance.
- `docs/validation/flibe_validation_matrix.md`: FLiBe source, executable, and benchmark status matrix.

The repository's `.github/workflows/` files remain the source of truth for actual GitHub Actions execution behavior.
