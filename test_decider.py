from decider.infer import Decider

d = Decider("Mapika/decider-2b")   # downloads ~3.8 GB on first run

ticket = "My laptop won't connect to the office VPN since this morning. I have a client demo at 2pm."

result = d.decide(ticket, [
    {"question": "Which IT category is this ticket?",
     "options": ["network", "account", "hardware", "software", "security"]},
    {"question": "Should this be escalated to a human engineer now?",
     "options": ["no", "yes"]},
])
print(result)