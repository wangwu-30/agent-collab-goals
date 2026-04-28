from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_collab.context import AgentContext


class ValidationError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValidationError(f"{path}: top-level value must be an object")
    return payload


def require_keys(path: Path, payload: dict[str, Any], keys: list[str]) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise ValidationError(f"{path}: missing required keys: {', '.join(missing)}")


def require_string(path: Path, payload: dict[str, Any], key: str) -> None:
    if not isinstance(payload.get(key), str) or not payload[key]:
        raise ValidationError(f"{path}: {key} must be a non-empty string")


def require_list(path: Path, payload: dict[str, Any], key: str, *, non_empty: bool) -> None:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ValidationError(f"{path}: {key} must be a list")
    if non_empty and not value:
        raise ValidationError(f"{path}: {key} must not be empty")


def require_object(path: Path, payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: {key} must be an object")
    return value


def validate_goal(path: Path) -> None:
    payload = load_json(path)
    require_keys(
        path,
        payload,
        [
            "id",
            "title",
            "summary",
            "status",
            "created_by",
            "acceptance_criteria",
            "constraints",
            "success_metrics",
            "tasks",
        ],
    )
    if not payload["id"].startswith("goal-"):
        raise ValidationError(f"{path}: id must start with goal-")
    if payload["status"] not in {"draft", "ready", "active", "blocked", "verifying", "done"}:
        raise ValidationError(f"{path}: invalid status {payload['status']!r}")
    for key in ["title", "summary", "created_by"]:
        require_string(path, payload, key)
    for key in ["acceptance_criteria", "success_metrics"]:
        require_list(path, payload, key, non_empty=True)
    require_list(path, payload, "constraints", non_empty=False)
    require_list(path, payload, "tasks", non_empty=False)
    for task_id in payload["tasks"]:
        if not isinstance(task_id, str) or not task_id.startswith("task-"):
            raise ValidationError(f"{path}: every task id must start with task-")


def validate_task(path: Path) -> None:
    payload = load_json(path)
    require_keys(
        path,
        payload,
        [
            "id",
            "goal_id",
            "title",
            "status",
            "owner",
            "scope",
            "acceptance_criteria",
            "verification",
        ],
    )
    if not payload["id"].startswith("task-"):
        raise ValidationError(f"{path}: id must start with task-")
    if not payload["goal_id"].startswith("goal-"):
        raise ValidationError(f"{path}: goal_id must start with goal-")
    if payload["status"] not in {"ready", "claimed", "active", "blocked", "review", "done"}:
        raise ValidationError(f"{path}: invalid status {payload['status']!r}")
    require_string(path, payload, "title")
    for key in ["scope", "acceptance_criteria", "verification"]:
        require_list(path, payload, key, non_empty=True)


def validate_context(path: Path) -> None:
    payload = load_json(path)
    require_keys(
        path,
        payload,
        [
            "avatar",
            "capabilities",
            "origin_task",
            "progress",
            "dynamic_context",
            "current_context_size",
            "max_size",
        ],
    )
    context = AgentContext.from_dict(payload)
    if not isinstance(context.avatar.get("name"), str) or not context.avatar["name"]:
        raise ValidationError(f"{path}: avatar.name is required")
    if not isinstance(context.avatar.get("role"), str) or not context.avatar["role"]:
        raise ValidationError(f"{path}: avatar.role is required")


def validate_handoff(path: Path) -> None:
    payload = load_json(path)
    require_keys(
        path,
        payload,
        [
            "source_agent",
            "origin_task",
            "progress",
            "recent_dynamic_context",
            "context",
            "repository_state",
            "next_action",
        ],
    )
    context = payload["context"]
    require_keys(
        path,
        context,
        ["current_context_size", "max_size", "context_unit", "handoff_threshold"],
    )
    ratio = context["current_context_size"] / context["max_size"]
    if ratio < context["handoff_threshold"]:
        raise ValidationError(f"{path}: handoff payload was created before threshold")
    require_string(path, payload, "next_action")


def validate_game(path: Path) -> None:
    payload = load_json(path)
    require_keys(
        path,
        payload,
        [
            "id",
            "title",
            "summary",
            "status",
            "supported_level_types",
            "supported_player_types",
            "action_protocol",
            "scoring",
            "fairness_rules",
        ],
    )
    if not payload["id"].startswith("game-"):
        raise ValidationError(f"{path}: id must start with game-")
    if payload["status"] not in {"draft", "active", "archived"}:
        raise ValidationError(f"{path}: invalid status {payload['status']!r}")
    for key in ["title", "summary"]:
        require_string(path, payload, key)
    require_list(path, payload, "supported_level_types", non_empty=True)
    require_list(path, payload, "supported_player_types", non_empty=True)
    require_object(path, payload, "action_protocol")
    require_object(path, payload, "scoring")
    require_list(path, payload, "fairness_rules", non_empty=True)
    for level_type in payload["supported_level_types"]:
        if level_type not in {"static", "agent_directed_dynamic"}:
            raise ValidationError(f"{path}: unsupported level type {level_type!r}")
    for player_type in payload["supported_player_types"]:
        if player_type not in {"human", "agent"}:
            raise ValidationError(f"{path}: unsupported player type {player_type!r}")


def validate_level(path: Path) -> None:
    payload = load_json(path)
    require_keys(
        path,
        payload,
        [
            "id",
            "game_id",
            "title",
            "level_type",
            "builder",
            "summary",
            "player_interface",
            "objective",
            "rules",
            "acceptance_criteria",
            "verification",
        ],
    )
    if not payload["id"].startswith("level-"):
        raise ValidationError(f"{path}: id must start with level-")
    if not payload["game_id"].startswith("game-"):
        raise ValidationError(f"{path}: game_id must start with game-")
    if payload["level_type"] not in {"static", "agent_directed_dynamic"}:
        raise ValidationError(f"{path}: invalid level_type {payload['level_type']!r}")
    for key in ["title", "summary"]:
        require_string(path, payload, key)

    builder = require_object(path, payload, "builder")
    require_keys(path, builder, ["type", "name"])
    if builder["type"] not in {"human_builder", "builder_agent"}:
        raise ValidationError(f"{path}: invalid builder.type {builder['type']!r}")
    if not isinstance(builder["name"], str) or not builder["name"]:
        raise ValidationError(f"{path}: builder.name must be a non-empty string")

    interface = require_object(path, payload, "player_interface")
    require_keys(path, interface, ["supported_player_types", "observations", "actions"])
    for key in ["supported_player_types", "observations", "actions"]:
        require_list(path, interface, key, non_empty=True)
    for player_type in interface["supported_player_types"]:
        if player_type not in {"human", "agent"}:
            raise ValidationError(f"{path}: invalid player type {player_type!r}")

    require_object(path, payload, "objective")
    require_list(path, payload, "rules", non_empty=True)
    require_list(path, payload, "acceptance_criteria", non_empty=True)
    require_list(path, payload, "verification", non_empty=True)

    if payload["level_type"] == "agent_directed_dynamic":
        director = require_object(path, payload, "director")
        require_keys(
            path,
            director,
            [
                "agent_role",
                "permissions",
                "forbidden_actions",
                "fairness_constraints",
                "event_log",
            ],
        )
        require_string(path, director, "agent_role")
        for key in ["permissions", "forbidden_actions", "fairness_constraints", "event_log"]:
            require_list(path, director, key, non_empty=True)
    elif "director" in payload:
        raise ValidationError(f"{path}: static levels must not define director")


def validate_repo(root: Path) -> list[Path]:
    checked: list[Path] = []

    validators = [
        (root / "examples" / "goals", "*.goal.json", validate_goal),
        (root / "examples" / "tasks", "*.task.json", validate_task),
        (root / "examples" / "games", "*.game.json", validate_game),
        (root / "examples" / "levels", "*.level.json", validate_level),
        (root / "examples" / "contexts", "*.agent-context.json", validate_context),
        (root / "examples" / "handoffs", "*.handoff.json", validate_handoff),
    ]

    for directory, pattern, validator in validators:
        if not directory.exists():
            raise ValidationError(f"{directory}: directory is required")
        files = sorted(directory.glob(pattern))
        if not files:
            raise ValidationError(f"{directory}: no {pattern} files found")
        for path in files:
            validator(path)
            checked.append(path)

    return checked
