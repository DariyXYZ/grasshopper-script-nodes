# Official Rhino And Grasshopper Notes

Use these notes for version-sensitive behaviour. They are distilled from current McNeel developer documentation and local installation inspection.

## Official docs used

- Grasshopper Script Component overview:
  - https://developer.rhino3d.com/en/guides/scripting/scripting-component/
- Grasshopper Python scripting guide:
  - https://developer.rhino3d.com/guides/scripting/scripting-gh-python/
- Grasshopper C# scripting guide:
  - https://developer.rhino3d.com/guides/scripting/scripting-gh-csharp
- Essential C# Scripting for Grasshopper:
  - https://developer.rhino3d.com/en/guides/grasshopper/csharp-essentials/

## Facts from official docs

- Rhino 8 has the unified Grasshopper Script component and dedicated C# / Python script workflows.
- The generic Script component can run multiple supported languages.
- Python 3 scripts in Rhino 8 can install packages via `pip`.
- C# scripts in Rhino 8 can install packages via `NuGet`.
- Python 3 scripting supports both Script-Mode and SDK-Mode.
- Python Script components are optional by default; as of Rhino 8.14 there is a Required toggle on inputs.
- Rhino 8 Python scripting docs explicitly describe both Python 3 and IronPython 2 components.
- The Python editor status bar shows the Python language version.

## Local machine inspection captured during creation

These are machine-specific observations from this computer and may differ elsewhere:

- `Rhino.exe` found at `C:\Program Files\Rhino 8\System\Rhino.exe`
- Rhino product version detected: `8.27.26019.16021`
- Grasshopper detected from `C:\Program Files\Rhino 8\Plug-ins\Grasshopper\Grasshopper.dll`
- Grasshopper file version detected: `8.27.26019.16021`
- Roslyn assemblies detected, including `Microsoft.CodeAnalysis.CSharp.dll`
- `McNeel.Python39.Runtime.dll` detected, which strongly indicates a Rhino 8 Python 3.9 runtime on this machine
- IronPython assemblies are also present, so legacy IronPython 2 support exists locally

## Safe compatibility guidance

- For Rhino 8 C# node generation, prefer `C# 9.0 compatibility` as the safe baseline unless the user requests newer syntax and the local environment clearly supports it.
- For Rhino 8 Python node generation, prefer Python 3 unless Rhino 7 compatibility or IronPython 2 compatibility is explicitly requested.
- For Python tasks that need component lifecycle hooks or explicit typed signatures, switch to SDK-Mode.

## Maintenance note

If Rhino is updated on the machine, rerun:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_python.ps1 .\scripts\detect_rhino_environment.py --pretty
```

and refresh any version-specific notes if they change materially.
