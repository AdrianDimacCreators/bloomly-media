"""Nov 23: schedule Ryan's ✅ P07 v2 Mina videos (Adrian: Ryan's 'Ready for post' is enough).
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
 ("MINA-P07", "product", "2026-12-03", "7:33 PM", "The cheapest products at Sephora that actually work after 50 🛍️ Plus the one peptide cream I use for plumper, smoother-looking skin, it's cheaper online, link in my bio 🤍 Comment GLOW and I'll send you the full list."),
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
    pid = sb.create(inp); st[vid] = {"facebook": pid, "instagram": "MANUAL via Moriah (never Buffer IG)", "source": "Ryan ✅ Nov 23 (P07 v2)"}
    json.dump(st, open("solae_scheduled.json", "w"), indent=1)
    if not any(r["id"] == vid for r in ig): ig.append(row)
    json.dump(ig, open(IGL, "w"), indent=1, ensure_ascii=False)
    print("NEW", vid, w.isoformat(), pid); out.append((vid, d, t, pid))
print(json.dumps(out))
