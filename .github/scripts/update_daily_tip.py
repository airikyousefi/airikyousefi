"""Rotate the Daily Web Tip section in README.md (runs inside the repo on GitHub Actions)."""
import datetime
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]  # .github/scripts -> repo root
README = ROOT / "README.md"
TIPS = ROOT / "daily-tips.json"

tips = json.loads(TIPS.read_text(encoding="utf-8"))["tips"]
doy = int(datetime.datetime.utcnow().strftime("%j"))
tip = tips[doy % len(tips)]

block = (
    "<!-- DAILY-TIP:START -->\n"
    "> 💡 **Today's Web Tip** — نکتهٔ روز\n"
    ">\n"
    f"> {tip['en']}\n"
    ">\n"
    f"> {tip['fa']}\n"
    "<!-- DAILY-TIP:END -->"
)

text = README.read_text(encoding="utf-8")
new_text, n = re.subn(r"<!-- DAILY-TIP:START -->.*?<!-- DAILY-TIP:END -->", block, text, flags=re.S)

if n == 0:
    print("DAILY-TIP markers not found in README.md — nothing changed")
elif new_text == text:
    print("Tip already up to date — nothing to commit")
else:
    README.write_text(new_text, encoding="utf-8")
    print(f"Updated daily tip (day {doy}, tip #{doy % len(tips)} of {len(tips)})")
