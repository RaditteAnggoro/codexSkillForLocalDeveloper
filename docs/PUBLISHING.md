# Publishing to GitHub

## Create the repository

For this copy, the intended destination is **RaditteAnggoro/codexSkillForLocalDeveloper**, with **public** visibility. Create the empty repository there and leave GitHub's README, license, and gitignore initialization options unchecked: this source already contains those files.

If you are publishing a fork under another account, substitute your own destination in the commands below.

Only publish the skills project directory. Its parent workspace may contain unrelated or confidential documents.

## Push with Git

If the project is not already initialized:

```sh
git init -b main
```

Before committing, check the file list:

```sh
git status --short
git add .agents/skills .github docs scripts tests AGENTS.md AGENTS.snippet.md README.md LICENSE VERSION CHANGELOG.md CONTRIBUTING.md SECURITY.md .gitignore .gitattributes requirements-dev.txt
git diff --cached --stat
git diff --cached --check
git commit -m "Initial release of Codex Developer Skills"
```

Use your existing Git identity. If Git reports a missing identity, set your own name and email; do not copy a placeholder identity into the commit.

After creating the repository, add its remote:

```sh
git remote add origin https://github.com/RaditteAnggoro/codexSkillForLocalDeveloper.git
git push -u origin main
```

If `origin` already exists, inspect `git remote -v` and use the intended remote rather than adding another or replacing it blindly. Authenticate using your normal GitHub connection, credential manager, or SSH setup. Do not paste tokens into source files or clone URLs.

## Verify the published result

- Confirm GitHub shows the intended visibility (**Public** for this copy).
- Confirm the eight skills and their supporting files are present.
- Wait for the **Validate skills** workflow to finish.
- Check the README and relative documentation links render correctly.
- Invite collaborators only as intended.

CI is included in the source, but a local test run is not evidence that hosted GitHub Actions has passed.

## Package version 0.1.0

```sh
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/build_release.py
```

This produces a ZIP and checksum in `dist/`. It does not create a GitHub release or tag. For a later release, update `VERSION` and `CHANGELOG.md`, verify the new state, then publish the desired tag and assets as a separate step.
