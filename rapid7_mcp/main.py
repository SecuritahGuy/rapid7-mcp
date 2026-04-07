"""FastAPI application with MCP mount for Rapid7 InsightVM."""

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from rapid7_mcp.routers import assets, scans, sites, vulnerabilities

app = FastAPI(
    title="Rapid7 InsightVM MCP Server",
    description=(
        "MCP server exposing Rapid7 InsightVM vulnerability management tools to LLM clients. "
        "Supports Claude Desktop, Cursor, and any MCP-compatible client. "
        "Set DEMO_MODE=true to explore all tools without a live InsightVM instance."
    ),
    version="0.1.0",
    contact={"name": "Tim Hollingsworth"},
    license_info={"name": "MIT"},
)

app.include_router(sites.router, prefix="/sites", tags=["Sites"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])
app.include_router(vulnerabilities.router, prefix="/vulnerabilities", tags=["Vulnerabilities"])
app.include_router(scans.router, prefix="/scans", tags=["Scans"])

mcp = FastApiMCP(app)
mcp.mount_http()  # Streamable HTTP MCP endpoint at /mcp
