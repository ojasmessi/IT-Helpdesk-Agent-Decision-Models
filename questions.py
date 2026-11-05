"""
Single source of truth for every decision the help desk agent makes.
Each question: instructions + options {key: description}.
Keep every question under 11 options (Laya calibration warning).
"""

QUESTIONS = {
    "category": {
        "instructions": "Which IT category does this ticket belong to?",
        "options": {
            "network":  "VPN, Wi-Fi, internet, connectivity, DNS",
            "account":  "passwords, login, MFA, locked or disabled accounts",
            "hardware": "laptop, desktop, printer, monitor, keyboard, physical devices",
            "software": "applications, installs, updates, crashes, licences",
            "security": "phishing, malware, suspicious emails or activity, data leaks",
            "email":    "Outlook, mailbox, calendar, sending or receiving mail",
        },
    },
        "blocking": {
        "instructions": "Is the user currently unable to do their work because of this issue?",
        "options": {
            "blocks_work": "the user cannot work or cannot do a key task right now",
            "can_work":    "the user can still work; this is an inconvenience or a request",
        },
    },
    "scope": {
        "instructions": "How many people does this issue affect?",
        "options": {
            "single_user":    "only the person writing",
            "multiple_users": "several people, a team, a floor, or the whole office",
        },
    },
    "deadline": {
        "instructions": "Does the user mention a deadline, meeting or time pressure?",
        "options": {
            "deadline":    "a specific time, meeting, demo or deadline is mentioned",
            "no_deadline": "no time pressure is mentioned",
        },
    },
    
    "request_type": {
        "instructions": "What kind of ticket is this?",
        "options": {
            "how_to":   "the user asks how to do something",
            "problem":  "something is broken or not working",
            "request":  "the user wants access, new software or new equipment",
        },
    },
    "security_incident": {
        "instructions": "Could this be a security incident, such as phishing, malware, account compromise or data exposure?",
        "options": {
            "incident":     "possible security incident, needs the security team",
            "not_incident": "ordinary IT issue with no security concern",
        },
    },
    "needs_human": {
        "instructions": "Does this ticket need a human IT engineer rather than self-service steps?",
        "options": {
            "human":        "needs hands-on work, admin rights, or physical access",
            "self_service": "the user can fix it by following instructions",
        },
    },
}


def to_laya(questions: dict) -> dict:
    """Convert to Laya's format: {name: {type, instructions, criteria}}."""
    return {
        name: {
            "type": "choice",
            "instructions": q["instructions"],
            "criteria": q["options"],
        }
        for name, q in questions.items()
    }


def to_decider(questions: dict) -> list:
    """Convert to decider-2b's format: [{question, options}], in the same order."""
    out = []
    for q in questions.values():
        described = "; ".join(f"{k} = {v}" for k, v in q["options"].items())
        out.append({
            "question": f"{q['instructions']} Options: {described}",
            "options": list(q["options"].keys()),
        })
    return out