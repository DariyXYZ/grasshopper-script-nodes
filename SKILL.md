---
name: grasshopper-script-nodes
description: Write production-ready scripts for Grasshopper C# Script, C# Script component, Python 3 Script, and IronPython 2 nodes inside Rhino/Grasshopper without switching to plugin development. Use when the user asks for a Grasshopper node script, Rhino node code, GH C# script, GH Python script, copy-paste code for a Rhino/Grasshopper script component, input/output generation via RunScript signature, idle-safe node behaviour, Rhino version detection, Grasshopper runtime detection, or persistent custom Grasshopper scripting rules.
---

# Grasshopper Script Nodes

This skill is for script components inside Grasshopper, not for compiled `.gha` plugins.

## Core workflow

1. Detect the local Rhino/Grasshopper scripting environment before writing code.
2. Prefer the highest installed Rhino version unless the user names a different target.
3. Read [references/default-rules.md](references/default-rules.md) every time.
4. Read [references/custom-rules.md](references/custom-rules.md) every time and treat it as higher priority than defaults.
5. For version-sensitive behaviour, read [references/official-rhino-notes.md](references/official-rhino-notes.md).
6. Generate code that is directly copy-pasteable into the requested node type.

## Detect environment first

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\detect_rhino_environment.py --pretty
```

If the script finds Rhino, use its results to drive the answer:

- Use detected Rhino and Grasshopper versions in the response.
- Use detected Python runtime information for Python nodes.
- Use detected Roslyn/runtime information for C# nodes.
- For Rhino 8, treat `C# 9.0 compatibility` as the safe default unless the user explicitly wants newer syntax and the detected environment supports it.

If detection fails:

- Fall back to `Rhino 8`.
- Fall back to `Grasshopper on Rhino 8`.
- Fall back to `C# 9.0 compatibility` for C#.
- Fall back to `Python 3` for Rhino 8 Python scripts unless the user explicitly asks for IronPython 2.

## Output policy

- Default to code-first answers.
- Return only the code when the user asks for code-only output.
- Keep the code inside one script component unless the user explicitly asks for a plugin or external assembly.
- Match the requested node family exactly:
  - `C# Script` or Rhino 8 C# script component: `GH_ScriptInstance` structure
  - Python 3 Script in simple cases: Script-Mode is acceptable
  - Python 3 Script with component-like lifecycle or previews: use SDK-Mode
  - IronPython 2: avoid Python 3-only syntax and packages

## Grasshopper-specific defaults

- Missing or disconnected inputs are a normal idle state, not an error, unless the user explicitly wants required inputs.
- Initialize outputs early with safe empty defaults.
- Avoid orange/red states caused only by empty optional inputs.
- Remove default `out`/debug outputs unless the user asked for diagnostics.
- Name inputs and outputs deliberately so Grasshopper creates useful parameters immediately.
- Prefer parameterized thresholds over hardcoded magic numbers.

## C# rules

- Generate `GH_ScriptInstance` code with `#region Usings`, `public class Script_Instance : GH_ScriptInstance`, and `private void RunScript(...)`.
- Keep code self-contained in one node.
- Use RhinoCommon carefully and verify ambiguous return types against [references/official-rhino-notes.md](references/official-rhino-notes.md).
- Prefer compatibility over novelty. For Rhino 8, write code that stays safe under a `C# 9.0` baseline unless the user asks otherwise.

## Python rules

- For Rhino 8, prefer Python 3 unless the user specifically asks for IronPython 2 or a Rhino 7-compatible legacy flow.
- Use SDK-Mode only when the task needs component-style hooks, typed `RunScript`, preview overrides, or stable IO generation from the signature.
- In Script-Mode, handle `None` and empty inputs explicitly to avoid runtime errors.

## Persisting user rules

If the user says any of the following, treat it as a persistent rule candidate:

- "this is a rule"
- "remember this"
- "always do it this way"
- "this is mandatory for me"
- "add this to the skill"
- Any equivalent Russian phrasing with the same intent

Then update `references/custom-rules.md` with a dated rule entry by running:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\update_custom_rules.py --rule "<rule text>" --source "user conversation"
```

When the rule affects generation strategy, also update this `SKILL.md` or [references/default-rules.md](references/default-rules.md) if the rule has become a stable global default rather than a user-specific preference.

## Clarification policy

Ask only when the choice changes the generated code materially and cannot be inferred:

- C# vs Python
- Python 3 vs IronPython 2
- Rhino 7 vs Rhino 8 when compatibility matters
- Script-Mode vs SDK-Mode for Python when lifecycle hooks matter

Otherwise make the safest assumption, state it briefly, and produce the working code.
