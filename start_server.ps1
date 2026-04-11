# 使用项目 uv 虚拟环境启动（含 aiohttp / SQLAlchemy asyncio 等）
# 请勿单独运行「uvicorn main:app」——那会走 PATH 上的全局/Conda Python，与 uv sync 的 .venv 无关。
Set-Location $PSScriptRoot
$ErrorActionPreference = "Stop"
uv sync
$port = if ($env:PORT) { $env:PORT } else { "8007" }
Write-Host "Using: uv run uvicorn (project .venv) on port $port" -ForegroundColor Cyan
uv run uvicorn main:app --reload --host 0.0.0.0 --port $port
