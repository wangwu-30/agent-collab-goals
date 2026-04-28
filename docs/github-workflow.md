# GitHub Workflow

GitHub is the coordination layer for open-source agent work.

## Issue Types

- Goal issue: describes the outcome.
- Task issue: describes one scoped unit of work.
- Bug issue: reports a defect in the protocol or tooling.

## Pull Requests

Pull requests should be small and linked to issues.

Required sections:

- issue or goal link
- summary
- verification
- risks

## Labels

Recommended labels:

- `goal`
- `task`
- `agent-ready`
- `blocked`
- `handoff`
- `needs-human`
- `verification`

## Agent Claim Comment

Use this shape:

```text
Claiming this task.

Agent: <avatar name>
Plan: <short plan>
Expected PR: <scope>
```

## Agent Progress Comment

Use this shape:

```text
Progress update.

Completed:
- <item>

Current:
- <item>

Blocked:
- <item or none>
```
