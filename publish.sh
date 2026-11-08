#!/bin/bash
# Re-knit the report, password-protect it, and push to GitHub (run from repo root).
# Usage: ./publish.sh "commit message"      (message optional)
# The report passphrase is read from .report_password (gitignored) or $ADU_REPORT_PW.
set -e
PW="${ADU_REPORT_PW:-$(cat .report_password 2>/dev/null || true)}"
if [ -z "$PW" ]; then echo "No passphrase: put it in .report_password or set ADU_REPORT_PW"; exit 1; fi

Rscript -e 'rmarkdown::render("adu_permit_pipeline.Rmd",
  params = list(make_gifs = TRUE),
  output_file = "report_plain.html")'

# encrypt: visitors to the Pages link must enter the passphrase (staticrypt: npm i -g staticrypt)
staticrypt report_plain.html -d docs --password "$PW" --remember 30 \
  --template-title "LA ADU Permits Report"
mv -f docs/report_plain.html docs/index.html

git add -A
git commit -m "${1:-Update ADU permit analysis}"
git push
echo "Pushed. The password-protected site updates within a minute or two."
