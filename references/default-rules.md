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

## Trust hierarchy

When facts conflict or memory is uncertain, prefer sources in this order:

1. Local `RhinoCommon.xml` from the installed Rhino version
2. Official Rhino developer documentation
3. Official McNeel sample code
4. Curated gotchas in this repo
5. Community forum posts
6. Memory

Never trust memory over the locally installed RhinoCommon documentation for ambiguous API semantics.

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
- Choose `Item`, `List`, or `Tree` access deliberately.
- When one logical input may produce multiple fragments, prefer grouped output over a lossy flat list.

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

## Geometry semantics guardrails

- Distinguish `Surface`, `BrepFace`, and `Brep` before writing geometry code.
- If the visible boundary matters, prefer `BrepFace` over `Surface`.
- Do not assume `UnderlyingSurface()` is interchangeable with a trimmed face.
- Treat `Surface.IsoCurve`, `BrepFace.TrimAwareIsoCurve`, `Curve.DivideByCount`, orientation APIs, and tolerance-sensitive intersection or projection methods as high-risk APIs.
- If a method name contains direction flags, constant parameters, or overloaded return shapes, verify the exact semantics against local docs before finalizing.
- For user requests about surface grids, rulings, isocurves, or generatrices:
  - restate which parameter is constant
  - decide whether boundaries are included
  - account for trims, seams, singularities, and periodic domains when relevant

## Geometry preflight checklist

Before finalizing geometry-heavy code, verify:

1. The runtime geometry representation matches the user-visible object.
2. Trims, seams, singularities, and face orientation have been considered when relevant.
3. Ambiguous API members were checked against local docs or the gotcha registry.
4. Return types match reality: single item, array, parameters, points, or grouped tree.
5. Boundary inclusion was chosen deliberately rather than accidentally inherited from the domain sampling loop.
6. The node remains neutral when optional inputs are empty.

## Validation philosophy

- Show only actionable warnings.
- Prefer user-meaningful categories over low-level API diagnostics.
- Avoid flooding outputs with technical noise that does not help the user decide what to fix.
