# Sources and capability boundaries

These independently maintained workflows were first assembled on 2026-10-28. The projects below inform the selected practices and are credited for comparison. Their original plugins, hooks, services, and renderers are not bundled here.

| Reference | Practices reflected here | Upstream capabilities not bundled |
| --- | --- | --- |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Minimal complete changes, reuse preference, implementation levels, focused checks, reviews and shortcut/debt awareness | Original prompt, slash-command adapters, hooks, dashboard, measurements, plugin state |
| [obra/superpowers](https://github.com/obra/superpowers) | Root-cause investigation, regression checks, verification evidence, incremental testing | Full mandatory methodology, original skill collection, hooks and agent orchestration |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Consequential feature questions, observable acceptance criteria, shared terminology, short test feedback cycles | Full engineering collection, setup command, tracker actions and orchestration |
| [humanlayer/skills](https://github.com/humanlayer/skills) | Research, planning, implementation, and resumable local records | Original RPI implementation, automatic fresh-session execution and upstream integrations |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | Diagrams that help explain code and data paths | Archify renderer, interactive viewer, validation utilities and export pipeline |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Browser console/network evidence, interaction reproduction, measured performance | MCP server, Chrome, tooling installation and configuration |

`lean-senior-engineering` combines a short entrypoint with optional references for test design, reviews, audits, and debt. Repository copies are independent of any same-name personal skill.

## OpenAI documentation used for packaging

- [Build skills](https://learn.chatgpt.com/docs/build-skills): local `.agents/skills` discovery, required metadata, explicit and implicit invocation, duplicate-name behaviour.
- [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md): repository instructions and scope.
- [Build focused skills](https://developers.openai.com/plugins/build/skills): concise entrypoints, supporting references, workflow boundaries, representative testing.

Use explicit `$skill-name` prompts to compare workflows. Skill availability and actual tool access are separate: instructions cannot provide an absent browser, network access, a database connection, or a running application.

The sources evolve. For full upstream behaviour, install and review the relevant upstream project separately and follow its current license and setup instructions. This pack makes no claim to reproduce upstream benchmarks or every plugin feature.
