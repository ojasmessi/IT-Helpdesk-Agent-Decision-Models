def from_laya(result: dict) -> dict:
    out = {}
    for name, ans in result["answers"].items():
        out[name] = {
            "choice": ans["choice"],
            "probs": ans["probabilities"],
            "confidence": ans["confidence"],          # use this for gating (per model card)
            "top_prob": ans["answer_confidence"],
        }
    return out


def from_decider(result: list, question_names: list) -> dict:
    out = {}
    for name, ans in zip(question_names, result):
        out[name] = {
            "choice": ans["choice"],
            "probs": ans["probs"],
            "confidence": ans["confidence"],
            "top_prob": ans["confidence"],
        }
    return out