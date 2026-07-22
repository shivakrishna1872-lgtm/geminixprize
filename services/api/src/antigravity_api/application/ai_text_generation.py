from typing import Protocol


class AiTextGeneration(Protocol):
    def generate_json(self, *, prompt: str) -> dict[str, object]:
        """Generate a JSON object from a model prompt."""
