#!/usr/bin/env python3
"""
Setup script for installing Neo4j locally on Windows.
This script downloads and sets up Neo4j Community Edition.
"""

import os
import sys
import urllib.request
import zipfile
import subprocess
import shutil
from pathlib import Path

def download_neo4j():
    """Download Neo4j Community Edition."""
    neo4j_version = "5.15.0"
    neo4j_zip = f"neo4j-community-{neo4j_version}-windows.zip"
    neo4j_url = f"https://neo4j.com/artifact.php?name=neo4j-community-{neo4j_version}-windows.zip"

    print(f"Downloading Neo4j {neo4j_version}...")

    try:
        with urllib.request.urlopen(neo4j_url) as response:
            with open(neo4j_zip, 'wb') as f:
                f.write(response.read())
        print("Download completed.")
        return neo4j_zip
    except Exception as e:
        print(f"Failed to download Neo4j: {e}")
        return None

def extract_neo4j(zip_file):
    """Extract Neo4j zip file."""
    print("Extracting Neo4j...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('.')
        print("Extraction completed.")
        return True
    except Exception as e:
        print(f"Failed to extract Neo4j: {e}")
        return False

def setup_neo4j():
    """Setup Neo4j with default configuration."""
    neo4j_dir = "neo4j-community-5.15.0"

    if not os.path.exists(neo4j_dir):
        zip_file = download_neo4j()
        if not zip_file:
            return False

        if not extract_neo4j(zip_file):
            return False

        # Clean up zip file
        os.remove(zip_file)

    # Configure Neo4j
    conf_dir = os.path.join(neo4j_dir, "conf")
    neo4j_conf = os.path.join(conf_dir, "neo4j.conf")

    # Update configuration
    config_updates = [
        "# Enable APOC procedures\n",
        "dbms.security.procedures.unrestricted=apoc.*\n",
        "# Allow file imports\n",
        "dbms.security.allow_csv_import_from_file_urls=true\n",
        "# Set initial password\n",
        "dbms.security.auth_enabled=true\n"
    ]

    try:
        with open(neo4j_conf, 'a') as f:
            f.writelines(config_updates)
        print("Neo4j configuration updated.")
    except Exception as e:
        print(f"Failed to update Neo4j configuration: {e}")
        return False

    return neo4j_dir

def start_neo4j(neo4j_dir):
    """Start Neo4j service."""
    print("Starting Neo4j...")
    try:
        # Change to neo4j directory
        os.chdir(neo4j_dir)

        # Start Neo4j
        result = subprocess.run(["bin\\neo4j.bat", "start"], capture_output=True, text=True)

        if result.returncode == 0:
            print("Neo4j started successfully!")
            print("Neo4j Browser: http://localhost:7474")
            print("Bolt URL: bolt://localhost:7687")
            print("Username: neo4j")
            print("Password: neo4j (change this after first login)")
            return True
        else:
            print(f"Failed to start Neo4j: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error starting Neo4j: {e}")
        return False

def main():
    """Main setup function."""
    print("Neo4j Local Setup for FlawFinder Backend")
    print("=" * 50)

    if sys.platform != "win32":
        print("This script is designed for Windows. For other platforms, please install Neo4j manually.")
        return

    neo4j_dir = setup_neo4j()
    if neo4j_dir:
        if start_neo4j(neo4j_dir):
            print("\nSetup completed successfully!")
            print("You can now run your backend with: python -m uvicorn app.main:app --reload")
        else:
            print("Setup completed but failed to start Neo4j.")
    else:
        print("Setup failed.")

if __name__ == "__main__":
    main()
