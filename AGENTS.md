# Repository Guidelines

## Project Structure & Module Organization
This repository is currently a minimal scaffold with no committed source tree. If you add code, keep a predictable layout such as `src/` for application code, `tests/` for automated tests, and `assets/` or `public/` for static files. Document any nonstandard directories in this file.

## Build, Test, and Development Commands
No build or test tooling is defined yet. Once you add a toolchain, list the exact commands here and keep them runnable from the repository root. Example patterns to follow:
- `npm run dev` to start a local dev server
- `npm test` or `pytest` to run the test suite
- `make build` to produce production artifacts

## Coding Style & Naming Conventions
No style guide is enforced at the moment. When introducing a language or framework, define:
- Indentation and formatting rules (for example, 2 spaces for JS/TS, 4 spaces for Python)
- Naming patterns (for example, `PascalCase` for components, `snake_case` for Python modules)
- Formatting or linting tools (for example, `prettier`, `eslint`, `ruff`)

## Testing Guidelines
Testing frameworks are not yet specified. When adding tests, document:
- The framework used (for example, `vitest`, `jest`, `pytest`)
- Test file naming (for example, `*.test.ts`, `test_*.py`)
- Minimum expectations (for example, critical paths must have coverage)

## Commit & Pull Request Guidelines
No commit convention is established yet. If you adopt one, write it down here. Suggested baseline:
- Commit messages in the imperative mood (for example, "Add API client")
- PRs include a clear description, linked issues (if any), and screenshots for UI changes

## Agent-Specific Instructions
If you add automation or agent workflows, document required environment variables and any local setup steps (for example, `cp .env.example .env`).
