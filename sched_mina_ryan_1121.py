"""Nov 21: schedule Ryan's 6 fixed Mina videos (Adrian: Ryan's 'Ready for post' is enough).
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
 ("MINA-G12", "growth", "2026-11-22", "12:41", "My DIY oat mask for tight, dry winter skin 🥣 Blend half a cup of oats to a fine powder, add warm water for a soft paste, chill 10 minutes, pat it on, rinse with lukewarm water. Patch test first. Follow me for more Korean skin tricks you can do at home after 50 ❤️"),
 ("MINA-P01", "product", "2026-11-22", "7:36 PM", "Cheap stuff from Trader Joe's that's just as good as the luxury version 🛒 Plus the one night cream I use on skin over 50: peptides, hyaluronic acid and sodium PCA for plumper, smoother-looking skin. It's linked in my bio 🤍 Comment GLOW and I'll send you my routine."),
 ("MINA-P02", "product", "2026-11-23", "7:28 PM", "Never a makeup wipe, never coconut oil on your face, never a jade roller… here's what I'd buy at Target instead 🎯 And the one cream I recommend for skin over 50 is only online, link in my bio 🤍 Comment TARGET and I'll send you the full list."),
 ("MINA-P03", "product", "2026-11-24", "7:41 PM", "Never ever use a face scrub after 50 🙅‍♀️ My Costco skincare picks, plus the peptide cream I use every night. You won't find it at Costco, it's only online, link in my bio 🤍 Comment T for my exact nightly routine."),
 ("MINA-P04", "product", "2026-11-25", "7:33 PM", "Cheap stuff from Dollar Tree that's just as good as the luxury stuff 💚 And the peptide cream I use for plumper, smoother-looking skin over 50, link in my bio 🤍 Comment GLOW and I'll send you the links to everything."),
 ("MINA-P06", "product", "2026-11-26", "7:24 PM", "If your skin does this after 50, it's moisture your skin can't hold onto anymore 💧 Peptides, hyaluronic acid and sodium PCA working together for plumper, smoother-looking skin. The cream I use is linked in my bio 🤍 Comment GLOW for my night routine."),
]
def when(d, t):
    pm = t.endswith("PM"); h, m = map(int, t.replace(" PM", "").split(":"))
    if pm and h < 12: h += 12
    return dt.datetime(*map(int, d.split("-")), h, m, tzinfo=TZ)
dry = "--dry" in sys.argv
st = json.load(open("solae_scheduled.json")); ig = json.load(open(IGL)); out = []
for vid, kind, d, t, body in P:
    w = when(d, t); url = BASE + f"solae_{vid}_ryan.mp4"
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
    pid = sb.create(inp); st[vid] = {"facebook": pid, "instagram": "MANUAL via Moriah (never Buffer IG)", "source": "Ryan M link"}
    json.dump(st, open("solae_scheduled.json", "w"), indent=1)
    if not any(r["id"] == vid for r in ig): ig.append(row)
    json.dump(ig, open(IGL, "w"), indent=1, ensure_ascii=False)
    print("NEW", vid, w.isoformat(), pid); out.append((vid, d, t, pid))
print(json.dumps(out))
