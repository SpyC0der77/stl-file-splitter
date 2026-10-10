$ErrorActionPreference = 'Stop'
$work = Join-Path ([IO.Path]::GetTempPath()) ('vhs-demo-' + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $work | Out-Null
Copy-Item -LiteralPath 'split-file.py' -Destination $work -Recurse
Copy-Item -LiteralPath 'docs/demo/block.stl' -Destination $work -Recurse
$work
