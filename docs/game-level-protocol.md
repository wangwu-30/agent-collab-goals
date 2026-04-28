# Game Level Protocol

This protocol defines how agent-built levels enter the repository.

## Game Manifest

A game manifest declares the overall game contract:

- game id and title
- supported level types
- supported player types
- shared action protocol
- scoring model
- safety and fairness rules

## Level Manifest

A level manifest declares a single playable challenge.

Required sections:

- identity
- parent game
- builder
- level type
- player interface
- objective
- rules
- acceptance criteria
- verification

## Dynamic Director Contract

Dynamic levels must define a director contract. The director agent may change the
level during play only through declared permissions.

Required director sections:

- `agent_role`
- `permissions`
- `forbidden_actions`
- `fairness_constraints`
- `event_log`

The director must not change win conditions after play starts unless that
ability is explicitly part of the level and visible to the player.

## Player Agent Contract

Agent players receive observations and emit actions.

The level must define:

- observation fields
- valid actions
- action limits
- terminal states
- scoring fields

The player agent should not need hidden repository context to play.

## Run Log

Every playable run should eventually emit:

- game id
- level id
- player type
- player identity
- start state
- action events
- director events for dynamic levels
- terminal state
- score
- verification result

Run logs make human and agent play comparable.
