# Maintaining Codex Developer Skills

This repository distributes instructions, examples, and small validation tools. Keep changes focused on a demonstrated workflow need. The consuming-project snippet is `AGENTS.snippet.md`; do not confuse it with this maintenance guide.

## Skill changes

- Keep one focused goal and a precise triggering description per skill.
- Read only relevant supporting references; avoid copying the same procedure into several skills.
- Preserve the user's explicit intent: a diagnosis, review, or planning request must not silently become implementation.
- Preserve useful autonomy for authorized implementation. Do not add routine approval gates.
- Do not claim a tool, browser, hook, test result, or integration is available merely because instructions mention it.
- Cite and retain applicable license notices for imported third-party material.

## Verification

Use the configured Python environment. Required checks after skill or tooling changes:

```sh
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

For packaging changes, also run `python scripts/build_release.py` and inspect its archive contents. Local checks use temporary fixtures and have no production access. Fix failures caused by the requested change and rerun affected checks without seeking confirmation at each step.

Structural tests do not prove skill quality. For significant workflow changes, try a representative request and record the observed outcome and limitations in the pull request. Do not invent evaluation results or promise efficiency gains.

## Scope and artifacts

Keep developer-specific paths, secrets, private source, local artifacts, and build output out of commits. Update documentation and the changelog for user-visible changes. Increment `VERSION` only for an intended release. Creating or publishing a GitHub release remains a separate action from building an archive.
