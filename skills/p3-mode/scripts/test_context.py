import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("context.py")
spec = importlib.util.spec_from_file_location("context", SCRIPT)
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


class ContextTests(unittest.TestCase):
    def test_resolves_local_and_stack_references_through_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "mode"
            (skill / "playbooks").mkdir(parents=True)
            (root / "AGENTS.md").write_text("rules")
            (root / "agents").mkdir()
            source = skill / "SKILL.md"
            source.write_text("mode")
            playbook = skill / "playbooks" / "feature.md"
            playbook.write_text("feature")
            agent = root / "agents" / "worker.md"
            agent.write_text("worker")
            link = root / "linked"
            link.symlink_to(skill)
            self.assertEqual(context.resolve(link / "SKILL.md", "playbooks/feature.md#step"), playbook)
            self.assertEqual(context.resolve(playbook, "playbooks/feature.md"), playbook)
            self.assertEqual(context.resolve(source, "agents/worker.md"), agent)
            with self.assertRaises(FileNotFoundError):
                context.resolve(source, "missing.md")

    def test_read_emits_content_only_when_it_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            state = Path(directory) / "state.json"
            path.write_text("first")
            first = context.read_changed(path, state)
            self.assertEqual(first["text"], "first")
            second = context.read_changed(path, state)
            self.assertFalse(second["changed"])
            self.assertNotIn("text", second)
            path.write_text("second")
            self.assertEqual(context.read_changed(path, state)["text"], "second")

    def test_payload_prefers_structured_data_and_selects_only_requested_fields(self):
        value = {"taskId": "task-1", "status": "completed", "summary": "done", "large": "x" * 10000}
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "payload"],
            input=json.dumps({"structuredContent": value, "content": [{"type": "text", "text": "invalid JSON"}]}),
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(result.stdout), {"taskId": "task-1", "status": "completed", "summary": "done"})
        self.assertEqual(context.unwrap({"content": [{"type": "image"}, {"type": "text", "text": json.dumps(value)}]}), value)
        with self.assertRaises(ValueError):
            context.unwrap({"content": []})

    def test_payload_lists_are_selected_and_missing_fields_fail(self):
        self.assertEqual(context.select_fields([{"status": "running", "extra": 1}], ["status"]), [{"status": "running"}])
        with self.assertRaises(ValueError):
            context.select_fields({"tasks": []}, ["status"])
        selected = context.select_fields({"summary": "x" * 2001}, ["summary"])
        self.assertEqual(selected, {"summary": "x" * 2000, "summaryTruncated": True})


if __name__ == "__main__":
    unittest.main()
