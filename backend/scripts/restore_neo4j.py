#!/usr/bin/env python3
"""
Restore Neo4j database from a dump file.
WARNING: This will overwrite the existing database!
"""
import asyncio
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.logging import logger

# Neo4j admin command (assumes neo4j-admin is in PATH)
NEO4J_ADMIN_COMMAND = "neo4j-admin"

def confirm_restore(backup_file: Path) -> bool:
    """
    Ask for confirmation before restoring from backup.
    
    Args:
        backup_file: Path to the backup file.
        
    Returns:
        bool: True if user confirms, False otherwise.
    """
    print("\n" + "=" * 60)
    print("WARNING: This will completely overwrite the Neo4j database!")
    print(f"Database: {settings.NEO4J_DATABASE}")
    print(f"Backup file: {backup_file}")
    print("=" * 60)
    
    # Check if the backup file exists
    if not backup_file.exists():
        logger.error(f"Backup file not found: {backup_file}")
        return False
    
    # Ask for confirmation
    response = input("\nAre you sure you want to continue? (yes/NO): ").strip().lower()
    return response in ("y", "yes")

async def restore_database(backup_file: Path) -> bool:
    """
    Restore the Neo4j database from a dump file.
    
    Args:
        backup_file: Path to the backup file.
        
    Returns:
        bool: True if restore was successful, False otherwise.
    """
    if not backup_file.exists():
        logger.error(f"Backup file not found: {backup_file}")
        return False
    
    # Build the restore command
    cmd = [
        NEO4J_ADMIN_COMMAND,
        "database",
        "restore",
        f"--from-path={backup_file}",
        f"--database={settings.NEO4J_DATABASE}",
        "--force",
        "--verbose"
    ]
    
    # Set environment variables for authentication
    env = os.environ.copy()
    env["NEO4J_URI"] = settings.NEO4J_URI
    env["NEO4J_USER"] = settings.NEO4J_USER
    env["NEO4J_PASSWORD"] = settings.NEO4J_PASSWORD
    
    logger.info(f"Starting Neo4j restore from {backup_file}")
    
    try:
        # Run the restore command
        process = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the process to complete
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode().strip() if stderr else "Unknown error"
            logger.error(f"Restore failed: {error_msg}")
            return False
        
        logger.info("Successfully restored Neo4j database")
        return True
        
    except Exception as e:
        logger.error(f"Error during restore: {e}")
        return False

async def main():
    """Main function to run the restore."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Restore Neo4j database from backup")
    parser.add_argument(
        "backup_file",
        type=Path,
        help="Path to the Neo4j backup file (.dump)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Skip confirmation prompt"
    )
    args = parser.parse_args()
    
    # Convert to absolute path
    backup_file = args.backup_file.absolute()
    
    # Ask for confirmation if not forced
    if not args.force and not confirm_restore(backup_file):
        print("Restore cancelled.")
        return
    
    try:
        # Run the restore
        success = await restore_database(backup_file)
        
        if success:
            print("\nDatabase restore completed successfully!")
            print("You may need to restart the Neo4j service for the changes to take effect.")
        else:
            print("\nDatabase restore failed. Check the logs for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nRestore cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
