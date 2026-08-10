$ErrorActionPreference = "Stop"

python -c "import reportlab" | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing the CV PDF dependency..."
    python -m pip install -r requirements-cv.txt
}

python scripts/build_cv_pdf.py
if ($LASTEXITCODE -ne 0) {
    throw "The CV PDF could not be generated."
}
