import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SKILL_DIR = Path(__file__).resolve().parents[1]
PREPARE = SKILL_DIR / "scripts" / "prepare_pet_run.py"


class StudioInputsTest(unittest.TestCase):
    def make_approved_inputs(self, root: Path) -> tuple[Path, Path]:
        approved_base = root / "approved.png"
        Image.new("RGBA", (96, 104), (31, 47, 63, 255)).save(approved_base)
        studio_brief = root / "studio-brief.json"
        studio_brief.write_text(
            json.dumps(
                {
                    "source_character": "Test Character",
                    "identity_lock": {
                        "must_preserve": ["five-petal head", "long forelimbs"],
                        "must_not_add": ["text", "weapons"],
                    },
                    "action_contract": {
                        "idle": "low-energy breathing with a tiny petal movement",
                        "waving": "wave with the right forelimb",
                    },
                    "look_mechanics": "keep the feet anchored and aim the petal head",
                    "approvals": {"main_art": True, "action_preview": True},
                }
            ),
            encoding="utf-8",
        )
        return approved_base, studio_brief

    def test_approved_base_completes_base_job_and_injects_studio_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            approved_base, studio_brief = self.make_approved_inputs(root)
            run_dir = root / "run"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--pet-name",
                    "Studio Test",
                    "--approved-base",
                    str(approved_base),
                    "--studio-brief",
                    str(studio_brief),
                    "--output-dir",
                    str(run_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            output = json.loads(completed.stdout)
            jobs = json.loads((run_dir / "imagegen-jobs.json").read_text())["jobs"]
            base_job = next(job for job in jobs if job["id"] == "base")
            idle_prompt = (run_dir / "prompts" / "rows" / "idle.md").read_text()
            waving_prompt = (run_dir / "prompts" / "rows" / "waving.md").read_text()
            look_prompt = (run_dir / "prompts" / "look-cardinals.md").read_text()

            self.assertEqual(base_job["status"], "complete")
            self.assertTrue(base_job["approved_source"])
            self.assertNotIn("base", output["ready_jobs"])
            self.assertIn("idle", output["ready_jobs"])
            self.assertTrue((run_dir / "references" / "canonical-base.png").is_file())
            self.assertTrue((run_dir / "decoded" / "base.png").is_file())
            self.assertTrue((run_dir / "references" / "studio-brief.json").is_file())
            self.assertEqual(
                (run_dir / "qa" / "look-mechanics.md").read_text().strip(),
                "keep the feet anchored and aim the petal head",
            )
            self.assertIn("five-petal head", idle_prompt)
            self.assertIn("low-energy breathing", idle_prompt)
            self.assertIn("wave with the right forelimb", waving_prompt)
            self.assertIn("keep the feet anchored", look_prompt)

            with Image.open(run_dir / "references" / "canonical-base.png") as image:
                self.assertEqual(image.convert("RGBA").getpixel((0, 0)), (31, 47, 63, 255))

    def test_legacy_run_still_starts_with_base_job(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            run_dir = Path(temporary_directory) / "run"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--pet-name",
                    "Legacy Test",
                    "--output-dir",
                    str(run_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            output = json.loads(completed.stdout)
            jobs = json.loads((run_dir / "imagegen-jobs.json").read_text())["jobs"]
            base_job = next(job for job in jobs if job["id"] == "base")

            self.assertEqual(output["ready_jobs"], ["base"])
            self.assertEqual(base_job["status"], "pending")
            self.assertFalse((run_dir / "references" / "canonical-base.png").exists())

    def test_invalid_studio_brief_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            invalid_brief = root / "invalid.json"
            invalid_brief.write_text('{"identity_lock": {"must_preserve": "wrong"}}')
            completed = subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--pet-name",
                    "Invalid Test",
                    "--studio-brief",
                    str(invalid_brief),
                    "--output-dir",
                    str(root / "run"),
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("identity_lock.must_preserve must be a string array", completed.stderr)


if __name__ == "__main__":
    unittest.main()
