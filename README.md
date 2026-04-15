# Grasshopper Script Nodes

Write copy-paste-ready Rhino and Grasshopper node scripts for `C# Script`, `Python 3 Script`, and legacy `IronPython 2` workflows without drifting into plugin development.

This repository contains a Codex-native skill for people who need practical Grasshopper node code quickly and accurately.

![Validate Skill](https://github.com/DariyXYZ/grasshopper-script-nodes/actions/workflows/validate.yml/badge.svg)

It helps with:

- detecting the locally installed Rhino and Grasshopper version before writing code
- detecting the available Python and C# scripting runtimes on the machine
- generating `GH_ScriptInstance`-compatible C# code for Rhino 8 script components
- generating Python 3 or IronPython 2 node code matched to the detected environment
- keeping script nodes neutral on empty or disconnected optional inputs
- shaping `RunScript(...)` signatures so Grasshopper creates useful inputs and outputs
- preserving practical node behavior such as no red or orange state for idle inputs
- verifying ambiguous RhinoCommon APIs against the locally installed `RhinoCommon.xml`
- using a curated gotcha registry for high-risk geometry semantics
- accumulating persistent user-specific rules in `references/custom-rules.md`
- keeping the whole workflow inside script nodes instead of compiled `.gha` plugins

## Who this is for

- Rhino and Grasshopper users who need code pasted directly into script components
- Codex users who want a reusable skill for Grasshopper scripting tasks
- teams that want more reliable script generation than generic LLM answers usually provide

## Why this repo exists

Many Grasshopper scripting requests fail because assistants mix up:

- script nodes vs compiled plugin development
- Rhino versions and runtime availability
- tricky RhinoCommon semantics around surfaces, faces, trims, or data trees

This repo is designed to reduce those mistakes by using local environment detection, curated gotchas, and exact documentation lookup.

## Quick install

Copy or clone this folder into your local Codex skills directory:

- Windows: `C:\Users\<you>\.codex\skills\grasshopper-script-nodes`
- or any Codex-indexed skills path used by your environment

Then restart Codex.

You can also install the current repo copy with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\install_skill.py --source . --target "$env:USERPROFILE\.codex\skills"
```

## Quick use

Typical prompts:

- "Write a Grasshopper C# script that does ..."
- "Write a Rhino 8 Grasshopper node script for ..."
- "Give me Python 3 code for a Grasshopper script component"
- "Keep the node neutral when optional inputs are empty"
- "Treat this as a new rule for future node code"

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
- read default rules, failure modes, custom rules, and gotchas
- choose C# vs Python based on the request
- choose Python 3 vs IronPython 2 only when compatibility requires it
- verify ambiguous geometry APIs against local RhinoCommon docs
- return code that is directly pasteable into the node

## Reliability strategy

This repo intentionally does not rely on memory alone for RhinoCommon geometry semantics.

The trust hierarchy is:

1. local `RhinoCommon.xml`
2. official Rhino developer docs
3. official McNeel sample code
4. curated gotcha registry in this repo
5. community forum threads

This is the core design choice that makes the skill more stable on geometry-heavy tasks such as trimmed surfaces, isocurves, domains, and face orientation.

## Common failure areas this skill now guards against

- `Surface` vs `BrepFace` vs `Brep`
- trim-aware behavior and underlying surfaces
- `IsoCurve` direction semantics
- `TrimAwareIsoCurve` returning `Curve[]`
- `DivideByCount` returning parameters
- face orientation and normals
- boundary, seam, and singularity issues
- accidental `Item` vs `List` vs `Tree` access mismatches

## What is inside

- `SKILL.md`: the main Codex skill
- `agents/openai.yaml`: Codex UI metadata
- `references/default-rules.md`: default behavior for Grasshopper node generation
- `references/common-failure-modes.md`: common categories of script generation failure
- `references/custom-rules.md`: persistent user-specific generation rules
- `references/official-rhino-notes.md`: official-doc-derived Rhino and Grasshopper notes
- `references/rhinocommon-gotchas.json`: machine-readable high-risk API facts and reminders
- `scripts/check_gotcha_registry.py`: validates the gotcha registry schema
- `scripts/detect_rhino_environment.py`: local Rhino, Grasshopper, and runtime detector
- `scripts/lookup_rhinocommon_docs.py`: local RhinoCommon XML lookup for exact API semantics
- `scripts/update_custom_rules.py`: appends new persistent rules to the custom rules file
- `scripts/install_skill.py`: copies the repo into a discoverable Codex skills path
- `scripts/check_skill_md.py`: validates skill frontmatter and body presence
- `scripts/inspect_skill_repo.py`: quick repo structure validation
- `scripts/run_python.ps1`: resilient Python launcher for Windows environments with broken `python` shims

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
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\check_gotcha_registry.py .\references\rhinocommon-gotchas.json
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\inspect_skill_repo.py .
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\detect_rhino_environment.py --pretty
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\lookup_rhinocommon_docs.py --member Surface.IsoCurve --member BrepFace.TrimAwareIsoCurve --pretty
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

## Scope boundary

This repo is for script-node generation only. It is not a framework for compiled Grasshopper plugin architecture.

## License

MIT. See `LICENSE.txt`.
