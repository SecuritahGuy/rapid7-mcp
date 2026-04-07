# Contributing to rapid7-mcp

Thanks for your interest in contributing. This guide covers everything you need to add a new tool, write tests, and open a pull request.

Please also review:

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md) (for responsible vulnerability disclosure)

---

## Table of Contents

- [Development setup](#development-setup)
- [How to add a new tool](#how-to-add-a-new-tool)
- [Adding fixture data](#adding-fixture-data)
- [Running tests](#running-tests)
- [Code style](#code-style)
- [Pull request checklist](#pull-request-checklist)

---

## Development setup

**Prerequisites:** Python 3.11+, [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
git clone https://github.com/SecuritahGuy/rapid7-mcp.git
cd rapid7-mcp
uv sync
cp .env.example .env
```

Verify everything works:

```bash
DEMO_MODE=true uv run pytest tests/
```

---

## How to add a new tool

Adding a tool means adding a FastAPI route. `fastapi-mcp` picks it up automatically — no extra registration needed.

### Step 1 — Add the route to the right router

Open the relevant file in [`rapid7_mcp/routers/`](rapid7_mcp/routers/). If you're adding something that doesn't fit an existing router, create a new one (see Step 5).

```python
# rapid7_mcp/routers/assets.py

@router.get(
    "/{asset_id}/tags",
    response_model=AssetTagList,         # Step 2
    operation_id="get_asset_tags",       # becomes the MCP tool name — keep it short and clear
    summary="Get tags for an asset",
    description=(
        "Returns all tags assigned to an asset. "
        "Tags are used in InsightVM to group assets for reporting and policy."
    ),
)
async def get_asset_tags(
    asset_id: int,
    client: InsightVMClient = Depends(get_client),
) -> AssetTagList:
    data = await client.get(f"/assets/{asset_id}/tags")
    return AssetTagList(**data)
```

A few rules:
- Always set `operation_id` — this is the MCP tool name. Use `snake_case`, be specific: `get_asset_tags` not `tags`.
- Always set `response_model` — this becomes the MCP output schema.
- Always set `summary` (one line) and `description` (2–4 sentences). The LLM uses these to decide when to call your tool and how to use it.
- Use `Depends(get_client)` — don't instantiate the client directly.

### Step 2 — Add Pydantic models

Add request and response schemas to [`rapid7_mcp/models.py`](rapid7_mcp/models.py).

Match the InsightVM v3 API field names using `alias` for camelCase fields:

```python
class AssetTag(BaseModel):
    id: int
    name: str
    color: str | None = None
    tag_type: str | None = Field(None, alias="type")
    created_by: str | None = Field(None, alias="createdBy")
    links: list[Link] = []

    model_config = {"populate_by_name": True}


class AssetTagList(BaseModel):
    page: PageInfo
    resources: list[AssetTag]
    links: list[Link] = []
```

If your route takes a request body, add a request model too:

```python
class TagSearchRequest(BaseModel):
    name: str | None = None
    type: str | None = None
```

### Step 3 — Add a fixture

Add a JSON fixture file to [`tests/fixtures/`](tests/fixtures/) with realistic sample data. Match the structure of the actual InsightVM v3 response for that endpoint.

For a collection endpoint:

```json
{
  "page": { "number": 0, "size": 10, "totalPages": 1, "totalResources": 2 },
  "resources": [
    { "id": 10, "name": "critical-assets", "type": "custom", ... },
    { "id": 11, "name": "production", "type": "custom", ... }
  ]
}
```

Then update the `_resolve_fixture` function in [`rapid7_mcp/client.py`](rapid7_mcp/client.py) to map the new path pattern to your fixture file:

```python
# In _resolve_fixture(), add a new elif block:
if root == "assets" and len(parts) == 3 and parts[2] == "tags":
    return "asset_tags.json"
```

### Step 4 — Write tests

Add a test file (or extend an existing one) in [`tests/`](tests/). Tests use the `client` fixture from `conftest.py` which runs in demo mode — no live console needed.

```python
# tests/test_assets.py

def test_get_asset_tags(client: TestClient) -> None:
    response = client.get("/assets/1/tags")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert "page" in data
```

Test the shape of the response, not implementation details. Cover:
- Happy path returns 200 with expected fields
- Pagination query params are accepted
- Body validation works (for POST endpoints)

### Step 5 — New router (if needed)

If you're adding a whole new domain (e.g., `/reports`), create a new router file:

```python
# rapid7_mcp/routers/reports.py
from fastapi import APIRouter
router = APIRouter()
# ... add routes
```

Then register it in [`rapid7_mcp/main.py`](rapid7_mcp/main.py):

```python
from rapid7_mcp.routers import assets, reports, scans, sites, vulnerabilities

app.include_router(reports.router, prefix="/reports", tags=["Reports"])
```

---

## Adding fixture data

Fixture files live in [`tests/fixtures/`](tests/fixtures/). They serve two purposes:

1. **Demo mode** — the server returns these when `DEMO_MODE=true`
2. **Tests** — the test suite loads these via the demo client

Keep fixture data realistic. Use plausible IPs, hostnames, CVE IDs, and CVSS scores. Real-looking data makes demo mode more useful for evaluation and screenshots.

When adding a new fixture:
1. Create the JSON file in `tests/fixtures/`
2. Add a path → filename mapping in `_resolve_fixture()` in `client.py`
3. Reference it in at least one test

---

## Running tests

```bash
# All tests
DEMO_MODE=true uv run pytest tests/

# With coverage
uv run pytest --cov=rapid7_mcp --cov-report=term-missing tests/

# Single file
uv run pytest tests/test_assets.py -v
```

All tests run against demo fixtures — no InsightVM console required.

---

## Code style

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [mypy](https://mypy-lang.org/) for type checking.

```bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run mypy rapid7_mcp/      # type check
```

CI enforces all three. A few conventions to follow:

- Type-annotate all function signatures
- Use `str | None` not `Optional[str]`
- Use `dict[str, Any]` not `Dict[str, Any]`
- Keep route handlers thin — put any logic in the client or a helper
- Don't add comments that restate what the code does; only comment on non-obvious decisions

---

## Pull request checklist

Before opening a PR, make sure:

- [ ] `uv run pytest tests/` passes
- [ ] `uv run ruff check .` passes (no lint errors)
- [ ] `uv run ruff format --check .` passes
- [ ] `uv run mypy rapid7_mcp/` passes
- [ ] New routes have `operation_id`, `summary`, and `description` set
- [ ] New models have `model_config = {"populate_by_name": True}` if they use aliases
- [ ] New endpoints have fixture data and at least one test
- [ ] `_resolve_fixture()` updated if new fixture files were added
- [ ] Demo mode still works end-to-end (`DEMO_MODE=true uv run uvicorn rapid7_mcp.main:app --port 8000`)

Keep commits focused. If you're adding a new router, that's one commit. If you're adding fixture data and tests, that can be the same commit. Avoid mixing unrelated changes.
