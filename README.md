# Skills for Lazy Developer
<!-- Author: Raditte Anggoro | Provenance: RA.CODEXSKILLS.2026.10 | Metadata: docs/provenance.json -->

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Eight practical skills for working with Codex: make focused changes, investigate failures, verify results, clarify features, and understand unfamiliar code.

Each workflow has its own `SKILL.md`. Load the one the task needs, use the project's existing tools, and keep evidence behind completion claims.

![Conceptual workflow: describe your task, select a focused skill, inspect the code, and return an evidence-backed result.](docs/assets/skills-workflow.svg)

*Workflow illustration, not an application screenshot. The skills guide the agent inside your existing development project.*

[Get started](#quick-start) · [Choose a workflow](#choose-your-workflow) · [Try a task](#try-a-task) · [All eight skills](#skills) · [Development](#development)

## Quick start

1. Clone this repository or download its source ZIP.
2. Copy the skill folders you want from `.agents/skills/` into the same location in your project. Copy the whole folder, including `references/` and `agents/` when present.
3. Merge [AGENTS.snippet.md](AGENTS.snippet.md) into your project's existing `AGENTS.md`. If the project has none, create it from the snippet.
4. Open Codex in your project and try a skill explicitly:

```text
Use $systematic-debugging to reproduce and fix [describe the bug].
Keep the change focused and use $verification-before-completion
before handing it back.
```

The discovery path in the target project must be `.agents/skills/<skill-name>/SKILL.md`. Do not copy this repository as an extra nested folder and expect its skills to apply to the parent project. Codex detects skill changes; restart it if the new skills do not appear. See the [official local-skills documentation](https://learn.chatgpt.com/docs/build-skills).

On macOS, press Command-Shift-period to show the hidden `.agents` folder. Merge existing directories carefully. Same-name skills from different locations do not merge; keep one active copy or invoke the desired `SKILL.md` by its path.

## Choose your workflow

Start with the outcome you need. This diagram shows common routes; it does not install tools or run commands by itself.

```mermaid
flowchart TD
    A[What do you need help with?] --> B{Task}
    B -->|A failure to understand or fix| C[systematic-debugging]
    B -->|A clear code change or review| D[lean-senior-engineering]
    B -->|A feature with open decisions| E[feature-discovery]
    B -->|An unfamiliar data flow| F[architecture-map]
    B -->|Work across modules or sessions| G[research-plan-implement]
    B -->|A browser interaction| H[browser-diagnostics]
    C --> I[Relevant checks and disclosed gaps]
    D --> I
    G --> I
    H --> I
    I --> J[verification-before-completion]
    J --> K[Result with evidence]
    E --> L[Decisions and acceptance criteria]
    F --> M[Diagram tied to source files]
    K --> N[release-readiness when assessing a release]
```

Diagnosis, review and planning requests keep their requested scope. For example, “diagnose only” produces findings; it does not authorize a fix. Use the linked [skill catalog](#skills) to inspect any workflow before trying it.

## Try a task

Open a scenario below, replace the bracketed input, and paste the prompt into Codex from your project. These are illustrative walkthroughs, not recorded executions or guaranteed results.

<details>
<summary><strong>Fix a failing test</strong> — reproduce → explain → change → verify</summary>

```text
Use $systematic-debugging to reproduce and fix [failing scenario].
The command is [test command] and the output is [relevant failure].
Keep the fix focused and use $verification-before-completion.
```

Look for a reproduction when the environment permits, a cause tied to the affected code, a focused fix and a check of the original case. If a dependency is unavailable, the agent should say which check it could not run.

</details>

<details>
<summary><strong>Understand an unfamiliar app</strong> — input → processing → storage → response</summary>

```text
Use $architecture-map to trace [endpoint or UI action].
Show validation, transformations, storage and the response,
with a diagram and links to the relevant source. Do not edit code.
```

Look for a source-backed flow with unknowns labeled. Static inspection explains the implementation; it should not be presented as a captured runtime trace.

</details>

<details>
<summary><strong>Shape a feature before building it</strong> — inspect → decide → define acceptance</summary>

```text
Use $feature-discovery to plan [feature].
Inspect the current flow, ask only questions that change the design,
and produce observable acceptance criteria. Planning only.
```

Look for the decisions that affect scope and a small set of testable outcomes. When you are ready to implement, ask for the chosen change explicitly.

</details>

For more prompts, including review, browser diagnosis and resumable work, see [Try the skills in Codex](docs/TRY-IT.md).

## Skills

| Skill | Use it for | What you get |
| --- | --- | --- |
| [lean-senior-engineering](.agents/skills/lean-senior-engineering/SKILL.md) | Implementation, refactoring, review, audit, technical debt | Small complete changes, focused checks, prioritized findings |
| [systematic-debugging](.agents/skills/systematic-debugging/SKILL.md) | Bugs, failing tests, build failures | Reproduction, supported cause, focused fix when requested |
| [verification-before-completion](.agents/skills/verification-before-completion/SKILL.md) | Implementation handoff, verification requests | Actual check results and clearly stated gaps |
| [feature-discovery](.agents/skills/feature-discovery/SKILL.md) | Ambiguous features, consequential design choices | Decisions and observable acceptance criteria |
| [research-plan-implement](.agents/skills/research-plan-implement/SKILL.md) | Changes across modules or sessions | Code-backed research, execution plan, resumable handoff |
| [architecture-map](.agents/skills/architecture-map/SKILL.md) | Architecture, data processing, change impact | Diagrams connected to real source evidence |
| [release-readiness](.agents/skills/release-readiness/SKILL.md) | Pre-release assessment | Scoped readiness decision, blockers, rollout considerations |
| [browser-diagnostics](.agents/skills/browser-diagnostics/SKILL.md) | UI, console, network, browser performance | Reproduction evidence and an explanation of the failing path |

Start with one skill on a representative task. Descriptions allow Codex to select matching workflows automatically; explicit invocation makes the first trial easier to observe. See [example prompts and expected behaviour](docs/TRY-IT.md).

## Design

- Reuse the repository's patterns and dependencies before introducing new ones.
- Complete the requested behaviour, including affected callers and meaningful checks.
- Diagnose from evidence and report the scope of verification.
- Keep reviews and diagnosis separate from implementation when the user requests findings only.
- Keep detailed references out of the initial skill context until needed.

The pack contains workflow instructions and optional UI metadata. It does not install hooks, a browser, an MCP server, or an application test framework. Browser diagnostics requires available browser tooling or an existing browser-test setup. Architecture diagrams use available rendering tools and disclose when rendering was not verified.

These workflows are independently maintained files informed by the projects credited in [Sources](docs/SOURCES.md). This is an independent project, with no affiliation with OpenAI or the credited upstream projects. It does not reproduce their full plugins, dashboards, or benchmark results.

## Repository layout

```text
.agents/skills/       Skill entrypoints, references, and UI metadata
.github/             CI, issue forms, and pull-request template
docs/                Trial prompts, sources, publishing, validation
scripts/             Structure validator and release archive builder
tests/               Tests for validation and packaging behaviour
AGENTS.md            Guidance for maintaining this repository
AGENTS.snippet.md    Guidance to merge into a consuming project
```

Copy the skills and snippet into your application. Keep this repository's maintenance `AGENTS.md`, CI, and tooling in the skills repository.

## Development

Using the skills requires no Python packages. Maintaining this repository requires Python 3.9+ and the development dependency below:

```sh
python3 -m venv .venv
# macOS/Linux:
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
```

On Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe`.

The validator checks metadata, directory/name agreement, invocation prompts, portable references, and local links. It does not execute the skill instructions or verify external URLs. CI runs the same validation and tests on pushes and pull requests.

The archive builder writes a versioned source ZIP and SHA-256 checksum to `dist/`, using an explicit list of distributable paths. It excludes local Git history, virtual environments, working artifacts, and operating-system files.

## Status and contributing

Initial version: **0.1.0**. Read [validation scope](docs/VALIDATION.md), [change history](CHANGELOG.md), and the [contribution guide](CONTRIBUTING.md). Behaviour varies with the model, application, and available tools; report a reproducible example when a workflow misbehaves.

To publish your own copy, follow [Publishing to GitHub](docs/PUBLISHING.md). For vulnerabilities or unintended sensitive-data exposure, see [Security](SECURITY.md).

## License

[MIT](LICENSE). Keep upstream notices if you later import upstream material; source acknowledgements do not replace those licenses.
