# Try the skills in Codex

Run the following prompts from your repository. Replace bracketed input with a real file, route, command, or task. The examples are user prompts, not shell commands.

## Confirm discovery

```text
List the repo-local skills under .agents/skills. Show each name and
when you would select it. Do not edit files.
```

Expect eight names. If the selector omits them, check the location, hidden folder, and YAML frontmatter, then restart Codex. If a skill name collides with another installed skill, request this pack's exact SKILL.md path.

## Implement a small feature

```text
Use $lean-senior-engineering in full mode to add [small feature].
Follow the existing implementation patterns and finish relevant checks.
```

Expect reuse of existing helpers, a focused diff, and checks matched to the changed behaviour. It should not generate a whole architecture or new framework for a small feature. You can request `lite`, `ultra`, or `off` in plain language; this is a conversational preference rather than a persistent plugin setting.

## Diagnose without implementing

```text
Use $systematic-debugging to diagnose why [scenario] fails.
Investigate and explain the cause. Do not implement a fix.
```

Expect an evidence-backed cause, unresolved uncertainty where appropriate, and a fix direction. Source code should remain unchanged. Temporary diagnostics should respect the requested inspection scope.

## Fix a real regression

```text
Use $systematic-debugging to reproduce and fix [bug].
The failing command is [command], with this output: [output].
Add an appropriate regression check and use
$verification-before-completion before the handoff.
```

Expect the failure established before the fix when the environment permits, an explanation tied to source, and the original case checked afterwards. Missing dependencies should be reported as a verification gap.

## Review or inventory debt

```text
Use $lean-senior-engineering to review my uncommitted changes.
Prioritize concrete defects and regressions. Do not implement changes.
```

```text
Use $lean-senior-engineering to inventory shortcut comments and
important technical debt in [subsystem]. Inspect the surrounding code,
prioritize by impact, and return a ledger without modifying files.
```

Expect locations and triggers, not generic best-practice complaints. A debt ledger should not invent due dates, owners, or previous acceptance.

## Clarify a feature

```text
Use $feature-discovery to plan a CSV import preview for this app.
Inspect the existing import flow, ask only consequential questions,
and produce acceptance criteria. Planning only.
```

Expect questions tied to implementation decisions and a small useful scope. A clear button-label change should bypass this workflow and be handled directly.

## Trace data processing

```text
Use $architecture-map to trace [endpoint or UI action] from input
through validation and transformation to storage and response.
Show a diagram, important field mappings, and source evidence.
Do not refactor the implementation.
```

Expect a diagram tied to real files and labelled unknowns. Static code inspection should not be presented as observed runtime execution.

## Complete substantial work

```text
Use $research-plan-implement to add [multi-module feature].
Research affected code, maintain a local plan and handoff,
then implement and verify the requested behaviour.
```

To resume in another chat after opening the same repository:

```text
Use $research-plan-implement to resume from
.agents/artifacts/[task-slug]/handoff.md.
Verify the current code state before completing the remaining work.
```

Expect a compact record of decisions, completed work, evidence, and next actions. The handoff does not automatically transfer chat history.

## Assess a release

```text
Use $release-readiness to assess the current uncommitted changes
for our staging release. Inspect existing scripts and CI, run safe
relevant local checks, and report blockers. Do not deploy.
```

Expect a scoped readiness verdict and disclosed checks, not an assumed green pipeline. Production or staging mutations are separate actions.

## Investigate a UI

```text
Use $browser-diagnostics to diagnose [UI issue] at [development URL].
Inspect the relevant interaction, console, and network evidence.
Use available browser tooling and report anything you cannot verify.
Diagnosis only.
```

Expect actual browser evidence if tools are available, or an honest source-based diagnosis and reproduction checklist if not. A Markdown file cannot install Chrome DevTools MCP or grant access to a browser.

## Compare the result

Choose a small representative change and use equivalent starting code in separate disposable copies if you want a comparison. Do not reset a working repository to create a baseline.

Compare correct behaviour, verification coverage, unrelated edits, unnecessary dependencies, human corrections, and elapsed effort. Smaller diffs only help when the behaviour is complete. These skills do not collect telemetry or calculate a savings score.

Watch for failure signs: an interview for a trivial task, a whole-repository scan for one-line work, speculative review findings, repeated tests with no changed evidence, or a completion claim without a result. Keep observations concrete and revise the relevant skill rather than adding broad rules to every file.
