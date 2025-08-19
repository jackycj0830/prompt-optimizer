# Pull Request

## Summary
- Describe the change and motivation

## Related Docs
- Requirements: docs/requirements.md (or docs/requirements_en.md)
- Design: docs/design.md (or docs/design_en.md)
- Tasks: docs/task.md (or docs/task_en.md)

## Changes
- [ ] Core (packages/core)
- [ ] UI (packages/ui)
- [ ] Web (packages/web)
- [ ] Desktop (packages/desktop)
- [ ] Extension (packages/extension)
- [ ] MCP Server (packages/mcp-server)
- [ ] Infra (api/*, middleware.js, docker, vercel.json)

## Checklists
### Acceptance (from Requirements)
- [ ] Functionality meets scope
- [ ] Performance targets (UI <200ms; streaming smooth)
- [ ] Security (no key leakage; safe inputs/outputs)
- [ ] Compatibility (Web/Desktop/Extension/MCP)
- [ ] Deployment readiness (Vercel/Docker/Release)

### Tests (from Task Plan)
- [ ] Unit tests (Vitest)
- [ ] Integration/Component tests
- [ ] E2E (if applicable)
- [ ] Streaming/timeout/error edge cases

### CI/CD
- [ ] Builds on all relevant packages
- [ ] Lints/types/tests pass
- [ ] Artifacts generated for Desktop/Extension (if applicable)

### Docs
- [ ] Updated documentation index (docs/README.md)
- [ ] Cross-references added (requirements/design/task)

