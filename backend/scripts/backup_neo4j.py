#!/usr/bin/env python3
"""
Backup Neo4j database to a dump file.
"""
import asyncio
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import init_neo4j, close_neo4j
from app.core.logging import logger

# Backup directory (relative to project root)
BACKUP_DIR = Path("backups")
NEO4J_BACKUP_COMMAND = "neo4j-admin"  # Assumes neo4j-admin is in PATH

async def backup_database(output_file: Optional[Path] = None) -> Path:
    """
    Backup the Neo4j database to a dump file.
    
    Args:
        output_file: Path to the output file. If None, a default path will be used.
        
    Returns:
        Path: Path to the created backup file.
    """
    # Create backup directory if it doesn't exist
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate default filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = BACKUP_DIR / f"neo4j_backup_{timestamp}.dump"
    
    # Convert to absolute path
    output_file = output_file.absolute()
    
    # Build the backup command
    cmd = [
        NEO4J_BACKUP_COMMAND,
        "database",
        "dump",
        settings.NEO4J_DATABASE,
        f"--to-path={output_file}",
        "--verbose"
    ]
    
    # Set environment variables for authentication
    env = os.environ.copy()
    env["NEO4J_URI"] = settings.NEO4J_URI
    env["NEO4J_USER"] = settings.NEO4J_USER
    env["NEO4J_PASSWORD"] = settings.NEO4J_PASSWORD
    
    logger.info(f"Starting Neo4j backup to {output_file}")
    
    try:
        # Run the backup command
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
            raise RuntimeError(f"Backup failed: {error_msg}")
        
        logger.info(f"Successfully backed up Neo4j database to {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"Error during backup: {e}")
        # Clean up partially created backup file if it exists
        if output_file.exists():
            output_file.unlink()
        raise

async def main():
    """Main function to run the backup."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Backup Neo4j database")
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (default: ./backups/neo4j_backup_<timestamp>.dump)"
    )
    args = parser.parse_args()
    
    try:
        # Initialize Neo4j connection (to verify credentials)
        await init_neo4j()
        
        # Run the backup
        backup_file = await backup_database(args.output)
        print(f"Backup created: {backup_file}")
        
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        sys.exit(1)
    finally:
        # Close Neo4j connection
        await close_neo4j()

if __name__ == "__main__":
    asyncio.run(main())
