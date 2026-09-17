"""Scaffold a new resource: one file in each layer and one test file.

Usage: python scripts/new_resource.py refund
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPOSITORY = '''from dataclasses import dataclass


@dataclass(frozen=True)
class {cls}:
    id: int


def get_{name}({name}_id: int) -> {cls} | None:
    raise NotImplementedError
'''

SERVICE = '''from shop.errors import AppError
from shop.repositories import {plural} as {plural}_repository
from shop.repositories.{plural} import {cls}


def get_{name}({name}_id: int) -> {cls}:
    {name} = {plural}_repository.get_{name}({name}_id)
    if {name} is None:
        raise AppError(f"{cls} {{{name}_id}} not found", status_code=404)
    return {name}
'''

ROUTE = '''from fastapi import APIRouter
from pydantic import BaseModel

from shop.services import {plural} as {plural}_service

router = APIRouter(prefix="/{plural}", tags=["{plural}"])


class {cls}Out(BaseModel):
    id: int


@router.get("/{{{name}_id}}")
def read_{name}({name}_id: int) -> {cls}Out:
    {name} = {plural}_service.get_{name}({name}_id)
    return {cls}Out(id={name}.id)
'''

TEST = '''from shop.services import {plural} as {plural}_service


def test_{plural}_service_is_importable() -> None:
    assert callable({plural}_service.get_{name})
'''


def main() -> int:
    if len(sys.argv) != 2 or not sys.argv[1].isidentifier() or not sys.argv[1].islower():
        print("usage: python scripts/new_resource.py <singular_lower_case_name>", file=sys.stderr)
        return 1
    name = sys.argv[1]
    plural = f"{name}s"
    cls = "".join(part.title() for part in name.split("_"))
    files = {
        ROOT / "shop" / "repositories" / f"{plural}.py": REPOSITORY,
        ROOT / "shop" / "services" / f"{plural}.py": SERVICE,
        ROOT / "shop" / "routes" / f"{plural}.py": ROUTE,
        ROOT / "tests" / f"test_{plural}.py": TEST,
    }
    existing = [path for path in files if path.exists()]
    if existing:
        for path in existing:
            print(f"already exists: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    for path, template in files.items():
        path.write_text(template.format(name=name, plural=plural, cls=cls))
        print(f"created {path.relative_to(ROOT)}")
    print("next: fill in the service, then register the router in shop/app.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
