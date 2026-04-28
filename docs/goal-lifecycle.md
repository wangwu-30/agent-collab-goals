# Goal Lifecycle

Goals move through explicit states so agents know what kind of work is allowed.

## States

| State | Meaning |
| --- | --- |
| `draft` | Goal is being shaped. Agents should ask clarifying questions. |
| `ready` | Goal has enough detail to decompose into tasks. |
| `active` | Tasks are being implemented. |
| `blocked` | Work is waiting on a decision or dependency. |
| `verifying` | Implementation exists and needs validation. |
| `done` | Acceptance criteria are met. |

## Required Goal Fields

- `id`
- `title`
- `summary`
- `status`
- `created_by`
- `acceptance_criteria`
- `constraints`
- `success_metrics`

## Decomposition

A good task:

- can be owned by one agent
- has testable acceptance criteria
- names the files or area likely to change
- has an explicit verification method
- can be merged without waiting for unrelated work

## Example

Goal:

```text
Create a shared agent handoff protocol.
```

Tasks:

```text
Define schema.
Add examples.
Add validator.
Document GitHub issue flow.
```
