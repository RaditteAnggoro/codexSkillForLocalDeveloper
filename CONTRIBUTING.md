# Contributing

Improve one workflow at a time and explain the failure or recurring need it addresses.

## Propose a change

For a bug report, include the skill name, a sanitized prompt, expected behaviour, observed behaviour, and enough project context to reproduce the issue. Include the Codex version/model if known. Remove tokens, private source, and personal data from examples.

For a new skill, first explain why an existing skill or optional reference cannot cover the use case. A longer skill list is not a goal by itself.

## Develop locally

Follow the environment setup in [README.md](README.md), then run:

```sh
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

Keep skill names aligned with their directory names. UI metadata belongs in `agents/openai.yaml`. Link detailed procedures from the entrypoint rather than duplicating them. Use repository-relative file links in saved documents.

For a tooling change, add a test that detects the relevant failure. For a workflow change, try a realistic prompt where practical; document what actually happened and what remains untested. Do not treat wording-matching tests as proof of good agent behaviour.

## Submit a pull request

Describe the problem, resulting behaviour, verification, and limitations. Keep unrelated cleanup separate. Update [CHANGELOG.md](CHANGELOG.md) under `Unreleased` for changes that affect users.

Contributions are provided under the repository's [MIT license](LICENSE). Do not submit content that you lack permission to distribute. Imported third-party material must retain its required notices and source attribution.
