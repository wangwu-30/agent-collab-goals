# Agent Collaboration Protocol

The protocol turns a broad goal into reviewable open-source work.

## Objects

- `Goal`: desired outcome, constraints, acceptance criteria, and owners.
- `Task`: small work item derived from a goal.
- `AgentContext`: current agent state.
- `Handoff`: compact continuation payload produced only near context limit.
- `Pull Request`: proposed change that resolves one or more tasks.

## Workflow

1. A maintainer writes a goal.
2. Agents or maintainers decompose the goal into tasks.
3. Each task becomes a GitHub issue.
4. An agent claims one issue by comment.
5. The agent changes files and records verification.
6. The agent opens a pull request linked to the issue.
7. Reviewers check the pull request against the goal acceptance criteria.
8. If an agent approaches its context limit, it produces a handoff payload.

## Coordination Rules

- Goals define why the work exists.
- Tasks define what can be completed independently.
- Issues coordinate ownership.
- Pull requests integrate work.
- Handoffs preserve continuity when an agent cannot safely continue.

## Conflict Handling

When two agents touch the same area:

1. Prefer issue comments to coordinate ownership.
2. Split tasks if the conflict is caused by scope.
3. Rebase or merge only after reading the other change.
4. Ask for human review when the conflict changes the goal.

## Done Criteria

A task is done when:

- its acceptance criteria pass
- validation has run
- the pull request links the issue
- no unresolved blocker remains
- the change has been reviewed and merged
