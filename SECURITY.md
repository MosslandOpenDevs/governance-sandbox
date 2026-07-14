# Security Policy

## Status

`governance-sandbox` is **Labs / Experimental** software. It is a local command-line
tool and is **not** intended to be exposed as a public web service in its current form.

## Reporting a vulnerability

Please report suspected vulnerabilities privately to the maintainers rather than
opening a public issue. Include reproduction steps and the affected commit. We aim to
acknowledge reports within a reasonable timeframe given the project's experimental status.

## Known input-handling caveats

The CLI is designed for trusted, local use. Be aware that a scenario file can:

- reference and read arbitrary local files (e.g. a proposal body loaded from a path); and
- write generated report artifacts to absolute paths or paths outside the working directory.

These are acceptable conveniences for a local CLI operated by its owner. **They are not
safe on a server**: before any web or multi-tenant mode is built, the input layer must be
hardened to reject paths outside a workspace, reject absolute/`..`/symlinked targets,
disable scenario-controlled output paths, and bound input size and run time. This work is
tracked in [docs/ROADMAP.md](docs/ROADMAP.md) (P1) and is a prerequisite for any hosted demo.

## Scope

Because the engine is a deterministic renderer with no network calls, no authentication,
and no persistent state, its attack surface today is limited to local input handling.
