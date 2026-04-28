import unittest

from agent_collab.context import AgentContext, Capability


def make_context(current_context_size: int) -> AgentContext:
    return AgentContext(
        avatar={
            "name": "ContextAgent",
            "role": "Agent runtime coordinator",
        },
        capabilities=[
            Capability(
                name="handoff",
                description="Create a compact continuation payload.",
                trigger="near_context_limit",
            )
        ],
        origin_task={
            "request": "Create an agent collaboration repo.",
            "objective": "Let agents complete open-source work from goals.",
        },
        progress={
            "status": "in_progress",
            "completed": ["Defined protocol"],
            "current": "Validate handoff",
            "blockers": [],
            "next_steps": ["Publish repo"],
        },
        dynamic_context=[
            {
                "kind": "observation",
                "content": "The user needs handoff only near context limit.",
            }
        ],
        current_context_size=current_context_size,
        max_size=100,
    )


class AgentContextTest(unittest.TestCase):
    def test_rejects_handoff_before_threshold(self) -> None:
        context = make_context(89)

        with self.assertRaises(RuntimeError):
            context.trigger_handoff(
                repository_state={
                    "branch": "main",
                    "open_files": [],
                    "verification": [],
                },
                next_action="Continue implementation.",
            )

    def test_allows_handoff_at_threshold(self) -> None:
        context = make_context(90)

        payload = context.trigger_handoff(
            repository_state={
                "branch": "main",
                "open_files": ["README.md"],
                "verification": ["python3 -m unittest discover -s tests -v"],
            },
            next_action="Run validation.",
        )

        self.assertEqual(payload["source_agent"]["name"], "ContextAgent")
        self.assertEqual(payload["context"]["current_context_size"], 90)
        self.assertEqual(payload["context"]["max_size"], 100)
        self.assertEqual(payload["next_action"], "Run validation.")

    def test_requires_handoff_capability(self) -> None:
        with self.assertRaises(ValueError):
            AgentContext(
                avatar={"name": "NoHandoff", "role": "test"},
                capabilities=[],
                origin_task={},
                progress={},
                dynamic_context=[],
                current_context_size=1,
                max_size=100,
            )


if __name__ == "__main__":
    unittest.main()
