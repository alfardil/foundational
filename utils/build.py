import os
import subprocess

import streamlit as st

# CONFIGURATION
REPO_DIR = "./foundational"


def get_swift_binary_path():
    """
    Asks Swift exactly where the release binary is located.
    """
    try:
        result = subprocess.run(
            ["swift", "build", "-c", "release", "--show-bin-path"],
            cwd=REPO_DIR,
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        bin_dir = result.stdout.strip()

        possible_names = ["Run", "AppleIntelligenceAPI", "App"]
        for name in possible_names:
            full_path = os.path.join(bin_dir, name)
            if os.path.exists(full_path):
                return full_path

        return None
    except Exception as e:
        print(f"Error finding binary path: {e}")
        return None


def ensure_backend_built():
    binary_path = get_swift_binary_path()

    if binary_path and os.path.exists(binary_path):
        return binary_path

    with st.spinner("Optimizing Apple Intelligence for your Mac... (This runs once)"):
        try:
            st.info("Compiling Release build... this takes about 1-2 minutes.")

            subprocess.run(
                ["swift", "build", "-c", "release"], cwd=REPO_DIR, check=True
            )

            return get_swift_binary_path()

        except subprocess.CalledProcessError:
            st.error("❌ Build failed. Check terminal output for errors.")
            st.stop()
