import os
os.environ["USE_TF"] = "0"   # prevents a known hang if TensorFlow is installed

from laya import Router

router = Router()  # downloads ~800 MB on first run

ticket = "My laptop won't connect to the office VPN since this morning. I have a client demo at 2pm."

questions = {
    "category": {
        "type": "choice",
        "instructions": "Which IT category is this ticket?",
        "criteria": {
            "network": "VPN, Wi-Fi, internet, connectivity",
            "account": "passwords, login, MFA, locked accounts",
            "hardware": "laptop, printer, monitor, peripherals",
            "software": "apps, installs, crashes, licences",
            "security": "phishing, malware, suspicious activity",
        },
    },
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this?",
        "criteria": ["not urgent", "soon", "blocking work or deadline"],
    },
}

result = router.predict(ticket, questions)
import json
print(json.dumps(result, indent=2, default=str))