from dataclasses import dataclass
from typing import List


@dataclass
class HistoryItem:
    id: str
    chain_id: str
    type: str
    model_name: str
    template_id: str
    input: str
    output: str
    created_at: int


class HistoryManager:
    def __init__(self, repo) -> None:
        self.repo = repo

    def append(self, type_: str, input_: str, output: str, model_name: str, template_id: str) -> None:
        self.repo.add_history(type_, input_, output, model_name, template_id)

    def list(self) -> List[HistoryItem]:
        return self.repo.fetch_history()

