# Governance

This repository separates human authority from agent execution.

## Maintainers

Maintainers decide:

- which goals are accepted
- whether acceptance criteria are sufficient
- whether a pull request satisfies the goal
- when blocked work needs human judgment

## Agents

Agents may:

- propose decomposition
- claim ready tasks
- open pull requests
- run validation
- generate handoff payloads near context limit

Agents may not:

- change goal acceptance criteria without review
- merge their own pull requests unless explicitly permitted
- bypass the handoff threshold
- claim broad ownership over unrelated tasks

## Review Standard

Review should focus on:

- correctness against the goal
- clarity of task scope
- repeatable verification
- low conflict with parallel work
