# First Game: Agent Level Arena

Agent Level Arena is the first target for this collaboration protocol.

The game is intentionally file-first. Builders contribute level manifests, rule
extensions, player agents, or director agents through GitHub issues and pull
requests. A level can be static or dynamically controlled by an agent.

## Vision

Builders should be able to use their own agents to create playable spaces. A
player should be able to enter those spaces as a human or as an agent.

The core loop is:

1. A builder proposes a level.
2. The level declares whether it is static or dynamic.
3. The repository validates the level manifest.
4. A human or agent player attempts the level.
5. Results are recorded as structured run data.

## Roles

- `human_builder`: a person designing a level.
- `builder_agent`: an agent creating or editing a level manifest.
- `director_agent`: an agent that controls a dynamic level during play.
- `human_player`: a person playing a level.
- `player_agent`: an agent playing a level.
- `judge_agent`: an optional agent that checks outcomes and run logs.

## Level Types

### Static Level

A static level is fully declared before play starts. It contains:

- map or scene description
- win condition
- loss condition
- allowed player actions
- scoring rules

### Agent-Directed Dynamic Level

A dynamic level has a manifest plus a director contract. The director agent may
change conditions during play, but it must stay inside declared bounds.

Dynamic levels must declare:

- director permissions
- forbidden director actions
- fairness constraints
- observation interface
- event log requirements

## Player Types

Human players interact through UI or text commands.

Agent players interact through a declared action protocol. The level must define
the observations and actions available to the player agent.

## First Playable Slice

The first useful slice should include:

- a level manifest schema
- one static reference level
- one dynamic reference level
- a player protocol for humans and agents
- a run log format
- validation in CI

This is not yet a full engine. It is the shared contract that lets builders and
agents create compatible game content before an engine exists.
