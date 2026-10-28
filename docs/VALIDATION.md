# Validation scope

## Automated checks

Run `python scripts/validate_skills.py` after installing `requirements-dev.txt`.

The validator checks:

- Each skill has YAML frontmatter, a valid directory-matching name, a concise nonempty description, and a nonempty body.
- Skill metadata has no duplicate keys.
- UI metadata has a display name, a correctly sized description, and an explicit invocation of its skill.
- Linked local files exist, stay inside the repository, and use portable links.
- GitHub workflow and issue-form YAML can be parsed.

External URLs, Markdown anchors, model decisions, and application runtime behaviour are outside structural validation.

Run `python -m unittest discover -s tests -v` to test the validator and archive builder, including rejection of invalid metadata, missing references, and paths outside the repository.

The initial repository preparation passed 18 tooling tests locally on Python 3.9.6. The eight skills passed structure and local-link validation, and the generated ZIP passed its integrity check. Hosted GitHub Actions has not yet run; the workflow is configured for Python 3.9 and 3.13.

## Workflow trial

The initial pack was exercised on 2026-10-28 using a disposable Python pagination fixture. An independent agent read the implementation, debugging, and verification skills and received a request to fix a failing first-page test.

Observed results:

| Stage | Outcome |
| --- | --- |
| Existing baseline | 2 tests, first-page test failed |
| Expanded regression cases before fix | 6 tests, 4 failed |
| Focused offset fix | One implementation line changed |
| Verification after fix | 6 tests passed |

A separate independent file review examined all eight skills and the initial documentation. The resulting refinements clarified reuse of existing regression tests, diagnosis-only source boundaries, and saved-artifact scope.

This trial does not establish behaviour across all models, codebases, or every workflow. Browser access, actual release execution, and hosted GitHub CI were not exercised by that trial. Report new evaluation results with the prompt, environment, expected behaviour, and observed evidence.
