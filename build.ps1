param(
  [switch]$OneDir
)

python -m pip install -U pip
poetry --version >$null 2>&1
if ($LASTEXITCODE -ne 0) {
  Write-Host "Poetry not found. Please install Poetry first." -ForegroundColor Yellow
  exit 1
}

poetry install --no-interaction --no-ansi

$common = @(
  "--clean",
  "--noconfirm",
  "--name", "PromptOptimizer",
  "--icon", "po_app/assets/icon.ico",
  "--add-data", "po_app/assets;assets"
)

if ($OneDir) {
  pyinstaller @common "po_app/main.py"
} else {
  pyinstaller @common "--onefile" "po_app/main.py"
}

