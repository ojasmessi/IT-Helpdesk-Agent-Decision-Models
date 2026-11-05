import env_setup   # must be the first import
import time

import torch
from laya import Router
from decider.infer import Decider
from questions import QUESTIONS, to_laya, to_decider
from normalize import from_laya, from_decider
from policy import compute_urgency

TICKETS = [
    ("My laptop won't connect to the office VPN. Client demo at 2pm.",            "network",  "high"),
    ("I forgot my password and I'm locked out of my account.",                     "account",  "high"),
    ("Got an email asking me to verify my bank details via a link, looks fake.",   "security", "high"),
    ("How do I add a shared calendar in Outlook?",                                 "email",    "low"),
    ("The printer on floor 2 keeps jamming.",                                      "hardware", "medium"),
    ("Excel crashes every time I open a large file.",                              "software", "medium"),
    ("Can I get Adobe Acrobat Pro installed? Need it next week.",                  "software", "low"),
    ("My MFA app is on my old phone which I lost.",                                "account",  "high"),
    ("The whole office has no internet right now.",                                "network",  "critical"),
    ("I clicked a link and now my files have weird extensions and a ransom note.", "security", "critical"),
]

names = list(QUESTIONS.keys())
laya_q, dec_q = to_laya(QUESTIONS), to_decider(QUESTIONS)

print("Loading models...")
router = Router(device="cuda", max_loaded=1)
decider = Decider("Mapika/decider-2b")

print("Warming up...")
router.predict("warm up", laya_q)
decider.decide("warm up", dec_q)
print(f"GPU: {torch.cuda.get_device_name(0)} | VRAM used: {torch.cuda.memory_allocated()/1e9:.2f} GB\n")

score = {m: {"category": 0, "urgency": 0} for m in ("laya", "decider")}
times = {"laya": [], "decider": []}

print(f"{'Ticket':<40} {'Expected':<18} {'Laya':<22} {'Decider':<22} {'ms L/D'}")
print("-" * 115)

for text, exp_cat, exp_urg in TICKETS:
    t0 = time.perf_counter(); L = from_laya(router.predict(text, laya_q)); tl = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); D = from_decider(decider.decide(text, dec_q), names); td = (time.perf_counter() - t0) * 1000
    times["laya"].append(tl); times["decider"].append(td)

    row = {}
    for m, res in (("laya", L), ("decider", D)):
        urg = compute_urgency(res)
        score[m]["category"] += res["category"]["choice"] == exp_cat
        score[m]["urgency"] += urg == exp_urg
        row[m] = f"{res['category']['choice']}/{urg}"

    print(f"{text[:38]:<40} {exp_cat+'/'+exp_urg:<18} {row['laya']:<22} {row['decider']:<22} {tl:.0f}/{td:.0f}")

n = len(TICKETS)
print("\nAccuracy:")
for m in score:
    print(f"  {m:<8} category {score[m]['category']}/{n}   urgency {score[m]['urgency']}/{n}")
print(f"\nAvg time:  Laya {sum(times['laya'])/n:.0f} ms   decider-2b {sum(times['decider'])/n:.0f} ms")