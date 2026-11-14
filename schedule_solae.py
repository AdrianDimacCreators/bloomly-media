#!/usr/bin/env python3
"""Schedule Solae (Moriah's WishlistRiley) reels into Buffer — 1 post/day on Instagram + Facebook.
Reuses the Buffer API helpers in schedule_buffer.py (same key in .env). Media: m/solae/ on GitHub Pages.

  python3 schedule_solae.py plan            show the schedule
  python3 schedule_solae.py all [--dry]     schedule every not-yet-scheduled item (never double-posts)
State: solae_scheduled.json (item -> {service: buffer post id}).
"""
import json, sys, datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo
import schedule_buffer as sb

HERE = Path(__file__).parent
BASE = "https://adriandimaccreators.github.io/bloomly-media/m/solae/"
TZ = ZoneInfo("America/Toronto")
TIME = (11, 30)                      # 11:30 AM local, 1x per day
STATE = HERE / "solae_scheduled.json"
CHANNELS = {"instagram": "6af4e39b62b70b94b0fc7692", "facebook": "6af4e47862b70b94b0fc7cdd"}  # wishlistriley IG / WishlistRiley FB
ITEMS = json.load(open(HERE / "solae_items.json"))   # [{id, day 'YYYY-MM-DD', file, caption}]


def due(it):
    d = dt.date.fromisoformat(it["day"])
    h, m = map(int, it.get("time", "%d:%d" % TIME).split(":"))
    return dt.datetime(d.year, d.month, d.day, h, m, tzinfo=TZ)


def payload(it, svc):
    meta = {"instagram": {"type": "reel", "shouldShareToFeed": True}} if svc == "instagram" else {"facebook": {"type": it.get("fb_type", "reel")}}  # FB Reels max 90 s -> longer videos go out as FB video posts
    return {"text": it["caption"], "channelId": CHANNELS[svc], "schedulingType": "automatic", "mode": "customScheduled",
            "dueAt": due(it).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "assets": [{"video": {"url": BASE + it["file"]}}], "metadata": meta}


def main():
    a = sys.argv[1:]; dry = "--dry" in a; cmd = ([x for x in a if x != "--dry"] or ["plan"])[0]
    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    for it in ITEMS:
        if cmd == "plan":
            print(it["id"], due(it).strftime("%a %d %b %I:%M %p"), it["file"], "| done:", list(st.get(it["id"], {}).keys())); continue
        if it.get("hold"): print(it["id"], "HOLD -", it["hold"]); continue
        done = st.get(it["id"], {})
        for svc in CHANNELS:
            if svc in done: continue
            inp = payload(it, svc)
            if dry: print("DRY", it["id"], svc, inp["dueAt"], inp["assets"][0]["video"]["url"]); continue
            try:
                done[svc] = sb.create(inp); print(it["id"], svc, "scheduled", inp["dueAt"], "->", done[svc])
            except RuntimeError as e:
                done.setdefault("errors", {})[svc] = str(e)[:300]; print(it["id"], svc, "ERROR", e)
            st[it["id"]] = done; STATE.write_text(json.dumps(st, indent=1))


if __name__ == "__main__":
    main()
