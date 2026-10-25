#!/usr/bin/env python3
"""
Package submission ZIP file (code.zip).
"""

import os
import zipfile

def package_submission():
    zip_filename = "code.zip"
    print(f"Packaging submission into {zip_filename}...")

    include_dirs = ["src", "scripts", "prompts", "evaluation"]
    include_files = [
        "README.md",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "output.csv",
        "package.json",
        "tsconfig.json",
        "vite.config.ts",
        "server.ts"
    ]

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in include_files:
            if os.path.exists(f):
                zipf.write(f, f)

        for d in include_dirs:
            if os.path.exists(d):
                for root, _, files in os.walk(d):
                    for file in files:
                        filepath = os.path.join(root, file)
                        # Exclude cache or binary leftovers
                        if "__pycache__" in filepath or ".pyc" in filepath:
                            continue
                        zipf.write(filepath, filepath)

    print(f"Successfully packaged {zip_filename} ({os.path.getsize(zip_filename)} bytes).")

if __name__ == "__main__":
    package_submission()
