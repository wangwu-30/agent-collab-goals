# Handoff

Handoff exists to prevent context loss when an agent is close to its context
limit. It is not a normal delegation mechanism.

## Trigger

Only trigger handoff when context is near full:

```text
current_context_size / max_size >= handoff_threshold
```

The default threshold is `0.90`.

## Payload

A handoff payload should include:

- source agent avatar
- origin task
- current progress
- recent dynamic context
- blockers
- verification state
- exact next action
- repository state summary

## Receiver Duties

The receiving agent should:

1. Verify the current repository state.
2. Read the linked issue and pull request.
3. Compare the handoff payload with files on disk.
4. Continue from the next action only if it still matches reality.

## Forbidden Uses

Do not use handoff:

- to avoid finishing a small task
- to skip verification
- before context is near full
- as a replacement for GitHub issue comments
