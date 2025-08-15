# Remove context menu entries
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\scripts\remove_context_menu.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "SilentlyContinue"

Remove-Item 'HKCU:\Software\Classes\Directory\Background\shell\SentraNewProject' -Recurse -Force
Remove-Item 'HKCU:\Software\Classes\Directory\shell\SentraNewProject' -Recurse -Force

Write-Host "🗑️ Menus 'SentraNewProject' supprimés (fond + sur dossier si présent)."
