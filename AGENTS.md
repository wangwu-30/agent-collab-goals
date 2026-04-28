# Agent Operating Rules

This repository is designed for multi-agent open-source work. Agents should
follow these rules when contributing.

## Work Selection

- Start from a GitHub issue linked to a goal.
- Work on one issue at a time.
- Claim work by commenting on the issue before making changes.
- Do not take tasks that lack acceptance criteria.
- Prefer small pull requests that close one issue.

## Context Requirements

Maintain an agent context with these fields:

- `avatar`
- `capabilities`
- `origin_task`
- `progress`
- `dynamic_context`
- `current_context_size`
- `max_size`

`capabilities` must include `handoff`. The `handoff` capability is not a normal
manual action. It may only trigger when context usage is near the configured
limit.

## ReAct Trace

Record dynamic context as structured ReAct entries:

- `observation`: facts learned from the repo, issue, tests, or user.
- `thought`: task-relevant reasoning summary.
- `action`: command, edit, or external operation performed.
- `result`: outcome of an action.
- `reflection`: updated plan, risk, or lesson.

Keep entries concise and avoid private chain-of-thought. The trace should help
the next agent continue the work, not expose unnecessary internals.

## Pull Request Requirements

Every pull request should include:

- linked issue or goal
- summary of changed behavior
- verification performed
- remaining risks or follow-up tasks

Do not rewrite unrelated files. Do not revert other contributors' work unless
the issue explicitly asks for it.

## Handoff

When context is near full, generate a handoff payload that includes:

- current goal and task
- progress summary
- recent dynamic context
- open blockers
- verification status
- exact next action

After handoff, the next agent should verify the repo state before continuing.
