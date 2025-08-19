param(
  [switch]$OneFile
)

# Requires: pip install nuitka ordered-set zstandard
python -m pip install -U pip
pip install nuitka ordered-set zstandard

$common = @(
  "--follow-imports",
  "--assume-yes-for-downloads",
  "--disable-console",
  "--enable-plugin=pyside6",
  "--include-data-dir=po_app/assets=assets"
)

if ($OneFile) {
  python -m nuitka @common --onefile --output-dir=dist po_app/main.py
} else {
  python -m nuitka @common --output-dir=dist po_app/main.py
}

