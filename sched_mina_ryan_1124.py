"""Nov 24: schedule Ryan's ✅ G42 v3, G45, P13 v2, P14 v2 (Adrian: Ryan's 'Ready for post' is enough).
FB via Buffer (reel); IG = manual row in Moriah's list (never Buffer IG). Usage: python3 sched_mina_ryan_1121.py [--dry]"""
import json, sys, datetime as dt
from zoneinfo import ZoneInfo
sys.path.insert(0, '.')
import schedule_buffer as sb
TZ = ZoneInfo("America/Toronto"); FB = "6af4e47862b70b94b0fc7cdd"
BASE = "https://adriandimaccreators.github.io/bloomly-media/m/solae/"
LINK = "https://solaecosmetics.com/products/cream?sca_ref=12750467.MH839tklVMdylh"
PTAGS = " #syntheticperformer #solaepartner #ad #over50skincare #kbeauty #glassskin"
GTAGS = " #kbeauty #over50skincare #glassskin #skincareover50 #syntheticperformer"
IGL = "/Users/adriandimac/Trialz/solae/manual_ig/mina_ig_schedule.json"
P = [  # id, kind, date, time, caption body
 ("MINA-G42", "growth", "2026-11-25", "8:17", "My 10-year egg yolk pad mask 🥚🍯 Two yolks, olive oil, coconut oil and honey, soaked into cotton pads and chilled in the fridge. Patch test on your jaw first. Save it for later and follow me for more Korean skin recipes ❤️"),
 ("MINA-G45", "growth", "2026-11-25", "12:52", "I started eating for my skin at 44. 10 years later, this honey garlic is still my holy grail 🧄🍯 Raw honey and fresh garlic slowly ferment, and the sharp garlic bite turns completely sweet. Follow me for more Korean skin recipes ❤️"),
 ("MINA-P13", "product", "2026-12-04", "7:36 PM", "Makeup creasing by noon after 50? It was never the foundation. It's the skin under it 💧 The peptide cream I use every night is linked in my bio 🤍 Comment GLOW and I'll send you my routine."),
 ("MINA-P14", "product", "2026-12-06", "7:29 PM", "Foundation cracking by noon isn't your makeup. It's skin that ran out of water 💧 The peptide cream I use every night is linked in my bio 🤍 Comment GLOW and I'll send you my routine."),
]
def when(d, t):
    pm = t.endswith("PM"); h, m = map(int, t.replace(" PM", "").split(":"))
    if pm and h < 12: h += 12
    return dt.datetime(*map(int, d.split("-")), h, m, tzinfo=TZ)
dry = "--dry" in sys.argv
st = json.load(open("solae_scheduled.json")); ig = json.load(open(IGL)); out = []
for vid, kind, d, t, body in P:
    w = when(d, t); url = BASE + f"solae_{vid}.mp4"
    fbtext = (f"{LINK}\n\n{body}" if kind == "product" else body) + (PTAGS if kind == "product" else GTAGS)
    igtext = body + (PTAGS if kind == "product" else GTAGS)
    if vid in st: print("SKIP already scheduled", vid); continue
    inp = {"text": fbtext, "channelId": FB, "schedulingType": "automatic", "mode": "customScheduled",
           "dueAt": w.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
           "assets": [{"video": {"url": url}}], "metadata": {"facebook": {"type": "reel"}}}
    tstr = t if "PM" in t else t + " PM" if int(t.split(":")[0]) == 12 else t + " AM"
    row = {"date": d, "time": tstr, "id": vid, "kind": kind,
           "post_as": "Main feed (Reel)" if kind == "product" else "Trial reel", "link": url, "caption": igtext}
    if dry: print("DRY", vid, w.isoformat(), url); print(fbtext[:120].replace("\n", " | ")); continue
    pid = sb.create(inp); st[vid] = {"facebook": pid, "instagram": "MANUAL via Moriah (never Buffer IG)", "source": "Ryan ✅ Nov 24"}
    json.dump(st, open("solae_scheduled.json", "w"), indent=1)
    if not any(r["id"] == vid for r in ig): ig.append(row)
    json.dump(ig, open(IGL, "w"), indent=1, ensure_ascii=False)
    print("NEW", vid, w.isoformat(), pid); out.append((vid, d, t, pid))
print(json.dumps(out))
