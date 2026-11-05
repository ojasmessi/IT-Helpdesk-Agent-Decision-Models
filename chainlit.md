# 🖥️ IT Help Desk Agent

Describe your IT issue and I'll triage it.

**Under the hood:**
- 🛡️ **Laya** + **decider-2b** vote on prompt injection and abuse (layered defence)
- 🔒 Passwords and API keys are masked before anything leaves this machine
- 🏷️ **decider-2b** classifies category and urgency facts; Python rules set the priority
- ✍️ OpenAI writes the reply from the masked text only