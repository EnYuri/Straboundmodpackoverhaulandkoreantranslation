param([string]$StarboundRoot = 'E:\My Games\steamapps\common\Starbound')
$ErrorActionPreference = 'Stop'
if (Get-Process -Name starbound,starbound_server -ErrorAction SilentlyContinue) {
    throw 'Close Starbound and its server before replacing an active pak.'
}
$source = Join-Path (Split-Path $PSScriptRoot -Parent) 'compat_sources\FUExGUIPatch'
$packer = Join-Path $StarboundRoot 'win\asset_packer.exe'
$output = Join-Path $StarboundRoot 'mods\contents_1681880007.pak'
$temporary = $output + '.tmp'
& $packer $source $temporary
if ($LASTEXITCODE -ne 0) { throw 'FU Extended GUI compatibility packing failed.' }
Move-Item -LiteralPath $temporary -Destination $output -Force
Get-Item -LiteralPath $output | Select-Object FullName,Length
