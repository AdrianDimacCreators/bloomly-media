"""Nov 22: schedule Ryan's 13 ✅ Mina videos (Adrian: Ryan's 'Ready for post' is enough).
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
 ("MINA-G35", "growth", "2026-11-22", "3:34 PM", "My morning glow shot 🥕🍊 Carrot and orange blended into one little shot, every morning. This is how I keep my skin looking fresh at 54. Follow me for more Korean skin habits you can do at home ❤️"),
 ("MINA-G37", "growth", "2026-11-23", "8:07", "The egg-white pore pack Korean moms swear by 🥚 Whip one egg white, paint a thin layer, let it dry, rinse with lukewarm water. Patch test first. Follow me for more Korean tricks after 50 ❤️"),
 ("MINA-G38", "growth", "2026-11-23", "12:36 PM", "Clove water: the simple thing I make at home for my skin 🌿 A few cloves, hot water, let it steep. Follow me for more of what I actually do at 54 ❤️"),
 ("MINA-G41", "growth", "2026-11-23", "3:27 PM", "Snow fungus soup, the Korean grandma secret for glowy skin 🍲 Soak, simmer, add a little sweetness, enjoy warm. Follow me for more Korean skin recipes ❤️"),
 ("MINA-G43", "growth", "2026-11-24", "8:13", "My warm veggie glow juice 🥕 Simple vegetables, gently warmed and blended. This is what I drink for my skin after 50. Follow me for more ❤️"),
 ("MINA-G44", "growth", "2026-11-24", "12:44 PM", "Why I take a spoon of olive oil every morning 🫒 One small habit I do for my skin at 54. Follow me for more Korean habits that work after 50 ❤️"),
 ("MINA-G36", "growth", "2026-11-24", "3:38 PM", "Korean mom's homemade ABC jelly 🍎 Apple, beet and carrot, made into little bites I eat every day. Follow me for more Korean skin recipes you can make at home ❤️"),
 ("MINA-P10", "product", "2026-11-27", "7:31 PM", "My Target skincare dupes after 50 🎯 Cheap finds that work just as well as the luxury stuff, plus the one peptide cream I only buy online, link in my bio 🤍 Comment GLOW and I'll send you the full list."),
 ("MINA-P12", "product", "2026-11-28", "7:26 PM", "Why Korean women don't rush to Botox 🇰🇷 Peptides, hyaluronic acid and sodium PCA for plumper, smoother-looking skin. The cream I use is $49, link in my bio 🤍 Comment GLOW for my night routine."),
 ("MINA-P11", "product", "2026-11-29", "7:39 PM", "More Target dupes: foundation and glow 🎯 The cheap picks I'd buy again, and the one cream I recommend for skin over 50, link in my bio 🤍 Comment GLOW and I'll send you the list."),
 ("MINA-P15", "product", "2026-11-30", "7:22 PM", "If water just slides off your skin after 50, this is why 💧 Peptides, hyaluronic acid and sodium PCA working together for plumper, smoother-looking skin, for a third of the department store jar. Link in my bio 🤍 Comment GLOW for my routine."),
 ("MINA-P16", "product", "2026-12-01", "7:34 PM", "The ginger tea I made for my friend's dry, flaky skin 🫚 Plus the peptide cream for the skin itself, link in my bio 🤍 Comment GLOW and I'll send you the recipe."),
 ("MINA-P17", "product", "2026-12-02", "7:27 PM", "Water-skin tea for dry, ashy skin after 50 🍯 My recipe, plus the cream I use for plumper, smoother-looking skin, link in my bio 🤍 Comment GLOW and I'll send you the recipe."),
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
    pid = sb.create(inp); st[vid] = {"facebook": pid, "instagram": "MANUAL via Moriah (never Buffer IG)", "source": "Ryan ✅ Nov 22"}
    json.dump(st, open("solae_scheduled.json", "w"), indent=1)
    if not any(r["id"] == vid for r in ig): ig.append(row)
    json.dump(ig, open(IGL, "w"), indent=1, ensure_ascii=False)
    print("NEW", vid, w.isoformat(), pid); out.append((vid, d, t, pid))
print(json.dumps(out))
