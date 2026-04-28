# Agent Collab Goals

Agent Collab Goals is a GitHub-first collaboration protocol for open-source
agents. Humans define goals, agents decompose them into tasks, and contributors
complete those tasks through issues and pull requests.

The repository is intentionally small and text-based. Every major object is a
file that can be reviewed, versioned, validated, and handed off.

## Core Idea

1. A human or maintainer writes a goal in `examples/goals/*.goal.json`.
2. Agents turn the goal into scoped tasks and GitHub issues.
3. Each agent works on one claimed task at a time.
4. Progress is recorded in issue comments, task files, and pull requests.
5. When an agent context is near its limit, the `handoff` capability creates a
   compact continuation payload for the next agent.

## First Attempt: Agent-Built Game

The first collaboration target is a game where builders can bring their own
agents to create levels. Levels can be static manifests or dynamic levels run by
an agent director. Players can be humans or agents.

Start from:

- `docs/first-game.md`
- `docs/game-level-protocol.md`
- `examples/goals/first-game.goal.json`
- `examples/games/agent-level-arena.game.json`
- `examples/levels/tutorial-static.level.json`
- `examples/levels/director-dynamic.level.json`

## Repository Map

- `.agent/`: default runtime policy for agent collaboration.
- `schemas/`: JSON Schemas for goals, tasks, contexts, handoffs, games, and
  levels.
- `examples/`: valid example payloads that document the protocol by example.
- `docs/`: collaboration protocol, goal lifecycle, and handoff rules.
- `.github/`: issue templates, pull request template, and CI validation.
- `src/agent_collab/`: minimal Python validator used by CI and local checks.

## Agent Context Contract

Every agent context should include:

- `avatar`: identity, role, constraints, and operating style.
- `capabilities`: available actions. It must include `handoff`.
- `origin_task`: the original task the agent is serving.
- `progress`: completed work, current step, blockers, and next steps.
- `dynamic_context`: ReAct-style trace entries: observation, thought, action,
  result, reflection.
- `current_context_size`: current measured context usage.
- `max_size`: maximum allowed context size.

The `handoff` capability must only trigger when the context is near full:

```text
current_context_size / max_size >= handoff_threshold
```

The default threshold is `0.90`.

## Quick Start

Validate the repository examples without installing the package:

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Create a new goal by copying `examples/goals/minimal.goal.json`, then open a
GitHub issue with the `Goal` template. Agents should not start implementation
until the goal has clear acceptance criteria.

## License

MIT
