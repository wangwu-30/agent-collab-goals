import unittest
from tempfile import NamedTemporaryFile
from pathlib import Path

from agent_collab.validation import ValidationError, validate_level


def write_level(payload: str) -> Path:
    with NamedTemporaryFile("w", encoding="utf-8", suffix=".level.json", delete=False) as file:
        file.write(payload)
        return Path(file.name)


class LevelValidationTest(unittest.TestCase):
    def test_dynamic_level_requires_director(self) -> None:
        path = write_level(
            """
            {
              "id": "level-missing-director",
              "game_id": "game-agent-level-arena",
              "title": "Missing Director",
              "level_type": "agent_directed_dynamic",
              "builder": {"type": "builder_agent", "name": "Builder"},
              "summary": "Invalid dynamic level.",
              "player_interface": {
                "supported_player_types": ["human", "agent"],
                "observations": ["room"],
                "actions": ["inspect"]
              },
              "objective": {"win": "Inspect the room."},
              "rules": ["Do the thing."],
              "acceptance_criteria": ["Validation fails without director."],
              "verification": ["python3 scripts/validate.py"]
            }
            """
        )

        with self.assertRaises(ValidationError):
            validate_level(path)

    def test_static_level_rejects_director(self) -> None:
        path = write_level(
            """
            {
              "id": "level-static-with-director",
              "game_id": "game-agent-level-arena",
              "title": "Static With Director",
              "level_type": "static",
              "builder": {"type": "human_builder", "name": "Builder"},
              "summary": "Invalid static level.",
              "player_interface": {
                "supported_player_types": ["human"],
                "observations": ["room"],
                "actions": ["inspect"]
              },
              "objective": {"win": "Inspect the room."},
              "rules": ["Do the thing."],
              "director": {
                "agent_role": "Interfere",
                "permissions": ["change room"],
                "forbidden_actions": ["none"],
                "fairness_constraints": ["none"],
                "event_log": ["turn"]
              },
              "acceptance_criteria": ["Validation fails with director."],
              "verification": ["python3 scripts/validate.py"]
            }
            """
        )

        with self.assertRaises(ValidationError):
            validate_level(path)


if __name__ == "__main__":
    unittest.main()
