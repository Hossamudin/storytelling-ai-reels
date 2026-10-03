"""00 - Create a new video project folder from the template.

Usage: python pipeline/new_project.py <name> [--title "..." ]
Then drop the voiceover file (and optional script.md) into projects/<name>/input/
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    name = C.sanitize_name(args.name)
    pp = C.project_path(name)
    if pp.exists() and (pp / "project.json").exists():
        print(f"Project '{name}' already exists at {pp}")
        return

    for sub in ["input", "assets/voice", "assets/images", "assets/videos",
                "transcript", "composition", "renders"]:
        (pp / sub).mkdir(parents=True, exist_ok=True)

    project = {
        "name": name,
        "title": args.title or name.replace("-", " ").replace("_", " ").title(),
        "stage": "ingest",
        "created": C.now_iso(),
        "updated": C.now_iso(),
        "aspect": None,
        "duration_s": None,
        "approved": False,
        "total_cost_usd": 0.0,
        "stage_history": [{"stage": "ingest", "at": C.now_iso(), "note": "project created", "from": None}],
    }
    C.save_project(name, project)
    C.log(name, f"Project created at {pp}")
    print(f"\nCreated project: {pp}")
    print(f"Next: put your voiceover (and optional script.md) into {pp / 'input'}")
    print(f"Then: python pipeline/clean_audio.py {name}")


if __name__ == "__main__":
    main()
