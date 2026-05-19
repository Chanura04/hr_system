class SignificanceScorer:

    @staticmethod
    def score(text: str) -> float:
        score = 0.0

        important_keywords = [
            "leave",
            "policy",
            "manager",
            "meeting",
            "urgent",
            "compliance",
            "salary"
        ]

        for word in important_keywords:
            if word.lower() in text.lower():
                score += 0.2

        score += min(len(text) / 500, 0.5)

        return round(min(score, 1.0), 2)