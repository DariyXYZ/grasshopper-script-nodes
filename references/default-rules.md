# Default Grasshopper Script Rules

Apply these defaults unless the user explicitly overrides them.

## Scope

- Work inside Grasshopper script nodes, not compiled plugins.
- Target copy-paste-ready code for:
  - Rhino 8 C# script component
  - Rhino 8 Python 3 script component
  - Legacy IronPython 2 component when explicitly requested

## Environment defaults

- If auto-detection succeeds, trust the detected Rhino and Grasshopper versions.
- If auto-detection fails, assume `Rhino 8`.
- For Rhino 8 C# scripts, use `C# 9.0 compatibility` as the safe baseline.
- For Rhino 8 Python scripts, prefer `Python 3`.

## Idle-safe node behaviour

- Treat missing or disconnected optional inputs as a neutral idle state.
- Do not raise warnings or errors only because optional inputs are empty.
- Initialize outputs before validation and return safe empty values early.
- Warn only when data is present but invalid for computation.
- Keep the component neutral instead of orange/red whenever the issue is only "nothing connected yet".

## IO shaping

- Keep only working inputs and outputs that the algorithm actually needs.
- Remove default `out` unless diagnostics are requested.
- Use meaningful input and output names so Grasshopper creates useful parameters.
- Expose tunable thresholds as inputs instead of hardcoding them.

## C# script shape

- Return `GH_ScriptInstance` code.
- Include `#region Usings`.
- Use `public class Script_Instance : GH_ScriptInstance`.
- Implement `private void RunScript(...)`.
- Keep helper methods in the same script unless there is a strong reason not to.

## Python script shape

- Prefer Script-Mode for small logic-only scripts.
- Prefer SDK-Mode when the task needs:
  - typed `RunScript` signature
  - component-like IO generation from signature edits
  - `BeforeRunScript` / `AfterRunScript`
  - preview overrides
- In Python, guard against `None`, empty lists, and disconnected inputs before doing operations.

## RhinoCommon precision notes

- Verify ambiguous RhinoCommon return types before generating final code.
- `Curve.DivideByCount(count, includeEnds)` should be treated as returning curve parameters, not `Point3d[]`, in the workflow this skill targets.
- Convert returned parameters into points explicitly with `curve.PointAt(t)`.
- For mesh topology checks, prefer `TopologyEdges` and `TopologyVertices` over raw mesh vertex indices when connectivity matters.

## Validation philosophy

- Show only actionable warnings.
- Prefer user-meaningful categories over low-level API diagnostics.
- Avoid flooding outputs with technical noise that does not help the user decide what to fix.
