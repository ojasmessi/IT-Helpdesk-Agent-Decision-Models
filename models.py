import env_setup  # must be first
import re

from laya import Router
from decider.infer import Decider

from questions import QUESTIONS, to_laya, to_decider
from guardrails import GUARD_QUESTIONS
from normalize import from_laya, from_decider
from policy import compute_urgency

# ---------- Layer 3: regex secret detection + masking ----------
KEY_RE = re.compile(r"\b(sk-[\w-]{8,}|AKIA[0-9A-Z]{16}|gh[pousr]_\w{20,})")
PW_RE = re.compile(r"(?i)\b(password|passwd|pwd|pin)(\s*(?:is|:|=)\s*)(\S+)")


def has_secret_regex(text: str) -> bool:
    return bool(KEY_RE.search(text) or PW_RE.search(text))


def mask_secrets(text: str) -> str:
    text = KEY_RE.sub("[REDACTED_KEY]", text)
    return PW_RE.sub(r"\1\2[REDACTED]", text)


# ---------- Model service ----------
LAYA_GUARDS = {k: GUARD_QUESTIONS[k] for k in ("injection", "tone")}


class DeskModels:
    def __init__(self):
        print("[models] loading Laya + decider-2b...")
        self.laya = Router(device="cuda", max_loaded=2)   # keep English + multilingual loaded
        self.decider = Decider("Mapika/decider-2b")

        self._laya_guard_q = to_laya(LAYA_GUARDS)
        self._guard_names = list(GUARD_QUESTIONS)
        self._guard_q = to_decider(GUARD_QUESTIONS)
        self._cls_names = list(QUESTIONS)
        self._cls_q = to_decider(QUESTIONS)

        self.laya.predict("warm up", self._laya_guard_q)
        self.decider.decide("warm up", self._guard_q)
        print("[models] ready")

    def guard(self, text: str) -> dict:
        """Layered safety checks. Runs on the RAW message."""
        raw = self.laya.predict(text, self._laya_guard_q)
        L = from_laya(raw)
        D = from_decider(self.decider.decide(text, self._guard_q), self._guard_names)

        return {
            # refuse only when decider is clearly sure it's off-topic
            "is_it":      D["is_it"]["probs"]["off_topic"] < 0.7,
            # OR-vote: flagged if EITHER model flags it
            "injection":  L["injection"]["choice"] == "injection" or D["injection"]["choice"] == "injection",
            "abusive":    L["tone"]["choice"] == "abusive" or D["tone"]["choice"] == "abusive",
            "has_secret": has_secret_regex(text) or D["secret"]["choice"] == "contains_secret",
            "language":   raw["routing"].get("detection", {}).get("language", "en"),
            "votes": {
                "injection": {"laya": L["injection"]["choice"], "decider": D["injection"]["choice"]},
                "tone":      {"laya": L["tone"]["choice"],      "decider": D["tone"]["choice"]},
                "off_topic_prob": round(D["is_it"]["probs"]["off_topic"], 2),
            },
        }

    def classify(self, text: str) -> dict:
        """Ticket classification. Call with the MASKED message."""
        D = from_decider(self.decider.decide(text, self._cls_q), self._cls_names)
        return {
            "category":          D["category"]["choice"],
            "category_conf":     round(D["category"]["confidence"], 2),
            "request_type":      D["request_type"]["choice"],
            "security_incident": D["security_incident"]["choice"] == "incident",
            "needs_human":       D["needs_human"]["choice"] == "human",
            "urgency":           compute_urgency(D),
        }