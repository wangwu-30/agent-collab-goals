# Agent Context Schema

An agent context is the minimum state required for another agent to understand
the task and continue safely.

## Required Fields

### avatar

The identity and behavior contract for the agent.

### capabilities

Actions the agent can perform. `handoff` is required.

The `handoff` capability must use:

```json
{
  "name": "handoff",
  "trigger": "near_context_limit"
}
```

### origin_task

The original task request, objective, constraints, and success criteria.

### progress

Current execution state:

- `status`
- `completed`
- `current`
- `blockers`
- `next_steps`

### dynamic_context

ReAct-style public trace entries:

- `observation`
- `thought`
- `action`
- `result`
- `reflection`

The trace should summarize useful state, not expose private reasoning.

### current_context_size

The current measured context usage.

### max_size

The maximum allowed context size.

## Handoff Rule

Handoff is allowed only when:

```text
current_context_size / max_size >= handoff_threshold
```

Default `handoff_threshold`: `0.90`.
