$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PackageDir = Join-Path $ProjectRoot 'package'
$Manifest = Join-Path $PackageDir 'pet.json'
$Spritesheet = Join-Path $PackageDir 'spritesheet.png'
$CodexRoot = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'
$Destination = Join-Path $CodexRoot 'pets\morgana'

if (-not (Test-Path -LiteralPath $Manifest -PathType Leaf)) {
    throw 'package/pet.json is missing. Run build_codex_sheet.py after all nine animation rows pass QA.'
}
if (-not (Test-Path -LiteralPath $Spritesheet -PathType Leaf)) {
    throw 'package/spritesheet.png is missing. Run build_codex_sheet.py first.'
}

Add-Type -AssemblyName System.Drawing
$Image = [System.Drawing.Image]::FromFile($Spritesheet)
try {
    if ($Image.Width -ne 1536 -or $Image.Height -ne 1872) {
        throw "Unexpected spritesheet size: $($Image.Width)x$($Image.Height)"
    }
} finally {
    $Image.Dispose()
}

$Config = Get-Content -LiteralPath $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json
if ($Config.spriteVersionNumber -ne 1 -or $Config.spritesheetPath -ne 'spritesheet.png') {
    throw 'pet.json is not a valid Codex v1 Morgana manifest.'
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null
Copy-Item -LiteralPath $Manifest -Destination (Join-Path $Destination 'pet.json') -Force
Copy-Item -LiteralPath $Spritesheet -Destination (Join-Path $Destination 'spritesheet.png') -Force
Write-Host "Installed Morgana to $Destination"
Write-Host 'Restart Codex, then choose Morgana in Settings > Personalization > Pet.'
