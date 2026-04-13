# grasshopper-script-nodes

Codex skill for writing copy-paste-ready Grasshopper C# and Python node scripts for Rhino, with local environment detection and an editable custom-rules memory.

## What this repo contains

- `SKILL.md`: the actual Codex skill
- `references/`: default rules, official Rhino notes, and user-grown custom rules
- `scripts/`: environment detection, rule updates, install/update helper, and repo validation
- `.github/workflows/validate.yml`: lightweight CI checks for GitHub

## Intended workflow

1. Keep this repo under git in your workspace.
2. Install or update the discoverable skill copy into `~/.codex/skills`.
3. When Codex is asked for a Grasshopper node script, the skill first detects Rhino/Grasshopper/runtime details on the machine.
4. If you say a behaviour is a permanent rule, Codex updates `references/custom-rules.md`.

## Install locally

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\install_skill.py --source . --target "$env:USERPROFILE\.codex\skills"
```

## Validate

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\check_skill_md.py SKILL.md
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\inspect_skill_repo.py .
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\detect_rhino_environment.py --pretty
```
