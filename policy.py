def compute_urgency(a: dict) -> str:
    """Turn the model's factual answers into an urgency level. Rules are ours, not the model's."""
    incident = a["security_incident"]["choice"] == "incident"
    multi    = a["scope"]["choice"] == "multiple_users"
    blocks   = a["blocking"]["choice"] == "blocks_work"
    rtype    = a["request_type"]["choice"]

    if multi or (incident and blocks):
        return "critical"
    if incident or blocks:
        return "high"
    if rtype == "problem":
        return "medium"
    return "low"