# Install context menu "New Sentra Project here" (user scope, no Admin)
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\scripts\install_context_menu.ps1
#   powershell -ExecutionPolicy Bypass -File .\scripts\install_context_menu.ps1 -AlsoOnFolder
[CmdletBinding()]
param(
  [switch]$AlsoOnFolder
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Test-Command { param([string]$Name) Get-Command $Name -ErrorAction SilentlyContinue | Out-Null }

function Ensure-Pipx {
  if (-not (Test-Command pipx)) {
    python -m pip install --upgrade pip pipx | Out-Null
    pipx ensurepath | Out-Null
  }
}

function Ensure-Sentra {
  if (-not (Test-Command sentra)) {
    # Si le script est lancé depuis le repo local, on tente l'install locale via pipx
    $repo = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
    if (Test-Path (Join-Path $repo "pyproject.toml")) {
      pipx install $repo | Out-Null
    } else {
      pipx install "git+https://github.com/NexorAgent/sentra_cli@v0.1.1" | Out-Null
    }
  }
}

function Add-Menu($keyPath, $cmdTemplate) {
  if (-not (Test-Path $keyPath)) { New-Item -Path $keyPath -Force | Out-Null }
  Set-ItemProperty -Path $keyPath -Name 'MUIVerb' -Value 'New Sentra Project here'
  Set-ItemProperty -Path $keyPath -Name 'Icon'   -Value 'powershell.exe'
  $cmdKey = Join-Path $keyPath 'command'
  if (-not (Test-Path $cmdKey)) { New-Item -Path $cmdKey -Force | Out-Null }
  Set-ItemProperty -Path $cmdKey -Name '(default)' -Value $cmdTemplate
}

Ensure-Pipx
Ensure-Sentra

# Menu sur le "fond" du dossier (clic droit dans l'explorateur)
$cmdBg = 'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Set-Location ''%V''; $n = Read-Host ''Project name''; if ($n) { sentra init $n; if (Get-Command code -ErrorAction SilentlyContinue) { code $n } }"'
Add-Menu 'HKCU:\Software\Classes\Directory\Background\shell\SentraNewProject' $cmdBg

# Optionnel : menu sur le dossier lui-même (clic droit sur un dossier)
if ($AlsoOnFolder) {
  $cmdDir = 'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Set-Location ''%1''; $n = Read-Host ''Project name''; if ($n) { sentra init $n; if (Get-Command code -ErrorAction SilentlyContinue) { code $n } }"'
  Add-Menu 'HKCU:\Software\Classes\Directory\shell\SentraNewProject' $cmdDir
}

Write-Host "✅ Contexte installé : clic droit → 'New Sentra Project here'. Ouvre/relance l'Explorateur si besoin."
