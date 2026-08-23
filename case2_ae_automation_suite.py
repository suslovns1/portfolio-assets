#!/usr/bin/env python3
"""Case 2 — After Effects Creative Automation Suite (custom CEP panel)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowkit import Flow

f = Flow("CASE 02 · STORYBY · IN-TOOL AUTOMATION",
         "After Effects Creative Automation Suite",
         "A custom panel that removes the routine of comp assembly without taking the designer out of After Effects.")

f.step(1, "Creative code",
       "The composition name is the spec: film, scene, hook, on-screen copy, music.",
       role="input",
       note="The naming convention the studio already used.")

f.step(2, "Parser and asset resolver",
       "Decodes the code, resolves every asset from the library, repairs unreadable media.",
       role="system", chips=["Naming grammar", "Auto-heal", "Preflight report"],
       note="Gaps are reported before the queue starts.")

f.step(3, "Automated comp build",
       "Footage and hook layout, automatic overlay keying, approved copy from the production database.",
       role="system", chips=["Auto colour key", "Airtable text DB", "Brand typography"])

f.step(4, "Caption track",
       "The voice is isolated, aligned to the read, then animated word by word.",
       role="ai", chips=["Vocal isolation", "Forced alignment"])

f.step(5, "Variation matrix and batch render",
       "Eight variations per pack built in one pass — hook × copy × music.",
       role="system", chips=["Split-test ready", "Renders as video or as statics"])

f.step(6, "Designer review",
       "Native, fully editable comps come back to the designer.",
       role="human")

f.step(7, "Variation pack",
       "Eight variations ready to test. Three to ten packs go out on a normal day.",
       role="output")

f.outcome([
    ("24–80", "creatives per day"),
    ("8 × 3–10", "per pack × packs per day"),
    ("20–100 min → minutes", "per pack, hands-on"),
    ("0", "renders lost to gaps"),
])
f.footnote("Case 03 rebuilt the same logic outside After Effects. Figures are relative deltas under NDA.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case2_ae_automation_suite.svg")
print(*f.save(out))
