## Development skills

Repository skills are in `.agents/skills/`. Use the workflow that fits the request and read only the selected skill and relevant references. State the selected workflow briefly so its effect is visible. Do not run all skills for every task.

| Request | Skill |
| --- | --- |
| Implement, refactor, review, audit, or inventory technical debt | `lean-senior-engineering` |
| Investigate a bug, build error, or test failure | `systematic-debugging` |
| Verify a coding change before handoff | `verification-before-completion` |
| Clarify an ambiguous feature or consequential design decision | `feature-discovery` |
| Research or execute a substantial change across modules or sessions | `research-plan-implement` |
| Explain architecture, data processing, or impact with code evidence | `architecture-map` |
| Assess a release and its outstanding checks | `release-readiness` |
| Reproduce a web UI issue using browser evidence | `browser-diagnostics` |

Keep investigation and testing proportional. Reuse existing project commands and patterns. A simple fix can use debugging, a minimal implementation, and focused verification without generating a specification or repository map. A diagnosis or review request produces findings unless changes are also requested.

Explicit user choices and this repository's specific conventions take precedence over skill defaults. Continue work already authorized; do not create extra approval steps. Report actual checks and material limitations. Do not invent unavailable tools, completed tests, or runtime evidence.
