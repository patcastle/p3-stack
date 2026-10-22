#!/usr/bin/env python3
"""Resolve skill references, read changed files once, and select one MCP payload."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def resolve(source, reference):
    source = Path(source).resolve(strict=True)
    reference = reference.split("#", 1)[0]
    target = Path(reference)
    if target.is_absolute():
        return target.resolve(strict=True)
    local = source.parent / target
    if local.exists():
        return local.resolve(strict=True)
    for parent in source.parents:
        candidate = parent / target
        if (parent / "SKILL.md").is_file() and candidate.exists():
            return candidate.resolve(strict=True)
    if target.parts and target.parts[0] in {"agents", "skills"}:
        for parent in source.parents:
            if (parent / "AGENTS.md").is_file() and (parent / "skills").is_dir():
                return (parent / target).resolve(strict=True)
    return local.resolve(strict=True)


def read_changed(path, state_path):
    path = Path(path).resolve(strict=True)
    state_path = Path(state_path)
    content = path.read_text()
    digest = hashlib.sha256(content.encode()).hexdigest()
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    result = {"path": str(path), "sha256": digest, "changed": state.get(str(path)) != digest}
    if result["changed"]:
        result["text"] = content
        state[str(path)] = digest
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state) + "\n")
    return result


def unwrap(result):
    if "structuredContent" in result and result["structuredContent"] is not None:
        return result["structuredContent"]
    for block in result.get("content", []):
        if block.get("type") == "text":
            return json.loads(block["text"])
    raise ValueError("MCP result has neither structuredContent nor JSON text")


def select_fields(value, fields):
    if isinstance(value, list):
        return [select_fields(item, fields) for item in value]
    if not isinstance(value, dict):
        raise ValueError("MCP payload must be an object or a list of objects")
    selected = {field: value[field] for field in fields if field in value}
    if not selected:
        raise ValueError("None of the requested fields exist; select the payload's actual fields")
    if isinstance(selected.get("summary"), str) and len(selected["summary"]) > 2000:
        selected["summary"] = selected["summary"][:2000]
        selected["summaryTruncated"] = True
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    reference = commands.add_parser("resolve")
    reference.add_argument("source")
    reference.add_argument("reference")
    reader = commands.add_parser("read")
    reader.add_argument("path")
    reader.add_argument("--state", required=True, help="A state file owned by this agent run")
    payload = commands.add_parser("payload")
    payload.add_argument("--fields", default="taskId,status,summary")
    args = parser.parse_args()
    if args.command == "resolve":
        print(resolve(args.source, args.reference))
    elif args.command == "read":
        print(json.dumps(read_changed(args.path, args.state)))
    else:
        value = unwrap(json.load(sys.stdin))
        fields = args.fields.split(",")
        print(json.dumps(select_fields(value, fields)))


if __name__ == "__main__":
    main()
