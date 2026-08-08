#!/usr/bin/env bash
# Build every artifact for "IoT with Raspberry Pi" (TGS-2020505433) from the
# single source of truth (course_data.py + data_domain1..5.py).
#
#   PPT + PDF   ->  courseware/
#   LP  + PDF   ->  courseware/   (Word TOC field injected with real page numbers)
#   LG  + PDF   ->  courseware/   (+ the Markdown mirror at the repo root)
#   labs/*.md   ->  labs/
#   assessment  ->  assessment/   (WA + PP, question paper + answer key)
#
# The TOC pass needs page numbers, so each DOCX is rendered to PDF once, the TOC
# is injected from that render, and the DOCX is rendered again.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
OUT="$REPO/courseware"
SOFFICE="${SOFFICE:-soffice}"

cd "$HERE"

echo "==> Slides"
python3 build_slides.py

echo "==> Lesson Plan"
python3 build_lesson_plan.py

echo "==> Learner Guide"
python3 build_learner_guide.py

echo "==> Labs"
python3 build_labs.py

echo "==> Assessment"
REPO="$REPO" python3 build_assessment.py

echo "==> PDFs (pass 1)"
"$SOFFICE" --headless --convert-to pdf --outdir "$OUT" "$OUT"/*.pptx "$OUT"/*.docx >/dev/null 2>&1

echo "==> Injecting Word TOC fields with real page numbers"
for doc in "$OUT"/LP-*.docx "$OUT"/LG-*.docx; do
  pdf="${doc%.docx}.pdf"
  [ -f "$pdf" ] && python3 inject_toc.py "$doc" "$pdf"
done

echo "==> PDFs (pass 2 — with the injected TOC)"
"$SOFFICE" --headless --convert-to pdf --outdir "$OUT" "$OUT"/LP-*.docx "$OUT"/LG-*.docx >/dev/null 2>&1

echo
echo "Done. Artifacts in $OUT and $REPO/{labs,assessment}"
ls -1 "$OUT"
