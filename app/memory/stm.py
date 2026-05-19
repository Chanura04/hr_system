from collections import defaultdict
from typing import Dict, List


class ShortTermMemory:

    def __init__(self):
        self.memory: Dict[str, List[str]] = defaultdict(list)

    def add(self, user_id: str, message: str):
        self.memory[user_id].append(message)

        if len(self.memory[user_id]) > 5:
            self.memory[user_id].pop(0)

    def get(self, user_id: str) -> List[str]:
        return self.memory[user_id]