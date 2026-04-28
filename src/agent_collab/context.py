from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


Trigger = Literal["manual", "always", "near_context_limit"]


@dataclass(frozen=True)
class Capability:
    name: str
    description: str
    trigger: Trigger


@dataclass
class AgentContext:
    avatar: dict[str, Any]
    capabilities: list[Capability]
    origin_task: dict[str, Any]
    progress: dict[str, Any]
    dynamic_context: list[dict[str, Any]]
    current_context_size: int
    max_size: int
    context_unit: Literal["tokens", "bytes", "chars"] = "tokens"
    handoff_threshold: float = 0.9

    def __post_init__(self) -> None:
        if self.current_context_size < 0:
            raise ValueError("current_context_size must be >= 0")
        if self.max_size <= 0:
            raise ValueError("max_size must be > 0")
        if not 0 < self.handoff_threshold <= 1:
            raise ValueError("handoff_threshold must be in (0, 1]")
        if not self.handoff_capability:
            raise ValueError("capabilities must include handoff")
        if self.handoff_capability.trigger != "near_context_limit":
            raise ValueError("handoff must use trigger near_context_limit")

    @property
    def context_ratio(self) -> float:
        return self.current_context_size / self.max_size

    @property
    def handoff_capability(self) -> Capability | None:
        for capability in self.capabilities:
            if capability.name == "handoff":
                return capability
        return None

    def can_handoff(self) -> bool:
        return self.context_ratio >= self.handoff_threshold

    def trigger_handoff(
        self,
        *,
        repository_state: dict[str, Any],
        next_action: str,
        keep_recent: int = 20,
    ) -> dict[str, Any]:
        if not self.can_handoff():
            raise RuntimeError("handoff can only trigger near the context limit")
        if keep_recent < 1:
            raise ValueError("keep_recent must be >= 1")
        if not next_action:
            raise ValueError("next_action is required")

        return {
            "source_agent": {
                "name": self.avatar["name"],
                "role": self.avatar["role"],
            },
            "origin_task": self.origin_task,
            "progress": self.progress,
            "recent_dynamic_context": self.dynamic_context[-keep_recent:],
            "context": {
                "current_context_size": self.current_context_size,
                "max_size": self.max_size,
                "context_unit": self.context_unit,
                "handoff_threshold": self.handoff_threshold,
            },
            "repository_state": repository_state,
            "next_action": next_action,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> AgentContext:
        capabilities = [
            Capability(
                name=item["name"],
                description=item.get("description", ""),
                trigger=item["trigger"],
            )
            for item in payload["capabilities"]
        ]
        return cls(
            avatar=payload["avatar"],
            capabilities=capabilities,
            origin_task=payload["origin_task"],
            progress=payload["progress"],
            dynamic_context=payload["dynamic_context"],
            current_context_size=payload["current_context_size"],
            max_size=payload["max_size"],
            context_unit=payload.get("context_unit", "tokens"),
            handoff_threshold=payload.get("handoff_threshold", 0.9),
        )
