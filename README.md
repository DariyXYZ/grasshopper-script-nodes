# Grasshopper Script Nodes

Write copy-paste-ready Rhino/Grasshopper node scripts for `C# Script`, `Python 3 Script`, and legacy `IronPython 2` workflows without drifting into plugin development.

This repository contains a Codex-native skill that helps with:
- detecting the locally installed Rhino and Grasshopper version before writing code
- detecting the available Python and C# scripting runtimes on the machine
- generating `GH_ScriptInstance`-compatible C# code for Rhino 8 script components
- generating Python 3 or IronPython 2 node code matched to the detected environment
- keeping script nodes neutral on empty or disconnected optional inputs
- shaping `RunScript(...)` signatures so Grasshopper creates useful inputs and outputs
- preserving practical node behaviour such as no red or orange state for idle inputs
- accumulating persistent user-specific rules in `references/custom-rules.md`
- keeping the whole workflow inside script nodes instead of compiled `.gha` plugins

## Automatic Grasshopper markers

This skill should be used automatically when a user asks for Grasshopper script-node code, even if they do not explicitly mention the skill by name.

Strong markers include:
- `Grasshopper`, `GH`, `Rhino node`, `script node`, `C# Script`, `Python Script`
- requests like "write a script for a Grasshopper node"
- requests for code that can be pasted directly into a Rhino or Grasshopper node
- requests to auto-create inputs and outputs through the `RunScript(...)` signature
- requests to keep the node from going red or orange on empty inputs
- requests to remember future generation preferences as rules

Expected behavior:
- detect the local Rhino environment first
- read default and custom rules
- choose C# vs Python based on the request
- choose Python 3 vs IronPython 2 only when compatibility requires it
- return code that is directly pasteable into the node

## What is inside

- `SKILL.md`: the main Codex skill
- `agents/openai.yaml`: Codex UI metadata
- `references/default-rules.md`: default behaviour for Grasshopper node generation
- `references/custom-rules.md`: persistent user-specific generation rules
- `references/official-rhino-notes.md`: official-doc-derived Rhino and Grasshopper notes
- `scripts/detect_rhino_environment.py`: local Rhino/Grasshopper/runtime detector
- `scripts/update_custom_rules.py`: appends new persistent rules to the custom rules file
- `scripts/install_skill.py`: copies the repo into a discoverable Codex skills path
- `scripts/check_skill_md.py`: validates skill frontmatter and body presence
- `scripts/inspect_skill_repo.py`: quick repo structure validation
- `scripts/run_python.ps1`: resilient Python launcher for Windows environments with broken `python` shims

## Install In Codex

Copy or clone this folder into your local Codex skills directory:

- Windows: `C:\Users\<you>\.codex\skills\grasshopper-script-nodes`
- Or any Codex-indexed skills path used by your environment

Then restart Codex.

You can also install the current repo copy with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\install_skill.py --source . --target "$env:USERPROFILE\.codex\skills"
```

## Typical use cases

- "Write a Grasshopper C# script that does ..."
- "Напиши скрипт для ноды Grasshopper"
- "Give me Python 3 code for a Rhino 8 Grasshopper node"
- "Make this GH node stay neutral when no mesh is connected"
- "Create inputs and outputs from the RunScript signature"
- "Use IronPython 2 because this must stay compatible with an older setup"
- "This is a rule, remember it for future node code"

## Local checks

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\check_skill_md.py SKILL.md
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\inspect_skill_repo.py .
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\detect_rhino_environment.py --pretty
```

## Environment detection workflow

The repo includes a local environment detector that reads Rhino installation metadata from Windows and inspects Rhino-side scripting assemblies.

On the machine where this repo was prepared, it detected:
- `Rhino 8.27.26019.16021`
- `Grasshopper 8.27.26019.16021`
- `Python 3.9` runtime available in Rhino 8
- `IronPython` assemblies also present
- `C# 9.0` as the safe compatibility recommendation for generated C# node code

See `install-flow-report.md` for the packaging approach and `install-report-sample.md` for a sample environment report.

## License

MIT. See `LICENSE.txt`.
