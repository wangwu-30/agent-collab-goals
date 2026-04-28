# Contributing

This project uses a goal-first workflow.

## Human Maintainers

1. Define a goal with clear acceptance criteria.
2. Create or approve tasks derived from that goal.
3. Review pull requests against the goal, not just against code style.
4. Keep issues small enough for one agent or contributor to complete.

## Agent Contributors

1. Pick a task issue with the `agent-ready` label.
2. Comment that you are claiming it.
3. Make the smallest useful change.
4. Run validation.
5. Open a pull request linked to the issue.

## Validation

Run:

```bash
python3 -m agent_collab validate
python3 -m unittest discover -s tests -v
```

CI runs the same checks.

## Labels

Recommended labels:

- `goal`: a desired outcome.
- `task`: a scoped unit of work.
- `agent-ready`: ready for an agent to claim.
- `blocked`: cannot proceed without more information.
- `handoff`: needs continuation from another agent.
- `needs-human`: requires maintainer judgment.
- `verification`: test or validation work.
