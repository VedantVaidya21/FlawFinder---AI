#!/usr/bin/env python3
"""
Manage Neo4j constraints for data integrity.
"""
import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import init_neo4j, close_neo4j, execute_query
from app.core.logging import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Common constraints for data integrity
COMMON_CONSTRAINTS = [
    # User constraints
    ("User", ["id"], "UNIQUE", "User ID must be unique"),
    ("User", ["email"], "UNIQUE", "User email must be unique"),
    
    # Organization constraints
    ("Organization", ["id"], "UNIQUE", "Organization ID must be unique"),
    ("Organization", ["name"], "UNIQUE", "Organization name must be unique"),
    
    # Report constraints
    ("Report", ["id"], "UNIQUE", "Report ID must be unique"),
    
    # ProcessFlow constraints
    ("ProcessFlow", ["id"], "UNIQUE", "Process flow ID must be unique"),
]

async def get_existing_constraints() -> List[Dict]:
    """Get all existing constraints from the database."""
    result = await execute_query("SHOW CONSTRAINTS YIELD *")
    return result if result else []

async def create_constraint(label: str, properties: List[str], constraint_type: str, description: str = "") -> bool:
    """Create a constraint if it doesn't already exist."""
    constraint_name = f"{label.lower()}_{'_'.join(properties).lower()}_{constraint_type.lower()}"
    
    # Check if constraint already exists
    existing = await execute_query(
        "SHOW CONSTRAINTS YIELD name WHERE name = $name",
        {"name": constraint_name}
    )
    
    if existing:
        logger.info(f"Constraint {constraint_name} already exists")
        return False
    
    # Create the constraint
    props = ", ".join([f"n.{prop}" for prop in properties])
    
    try:
        if constraint_type.upper() == "UNIQUE":
            query = f"CREATE CONSTRAINT {constraint_name} IF NOT EXISTS FOR (n:{label}) REQUIRE ({props}) IS UNIQUE"
        elif constraint_type.upper() == "NOT NULL":
            # Note: Neo4j doesn't have direct NOT NULL constraints, we handle this in application code
            logger.warning("NOT NULL constraints should be handled in application code")
            return False
        else:
            logger.error(f"Unsupported constraint type: {constraint_type}")
            return False
            
        await execute_query(query, read_only=False)
        logger.info(f"Created {constraint_type} constraint {constraint_name} on :{label}({', '.join(properties)}) - {description}")
        return True
    except Exception as e:
        logger.error(f"Failed to create constraint {constraint_name}: {e}")
        return False

async def drop_constraint(constraint_name: str) -> bool:
    """Drop a constraint by name."""
    try:
        await execute_query(f"DROP CONSTRAINT {constraint_name} IF EXISTS", read_only=False)
        logger.info(f"Dropped constraint: {constraint_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to drop constraint {constraint_name}: {e}")
        return False

async def create_common_constraints() -> Tuple[int, int]:
    """Create common constraints for data integrity."""
    success = 0
    failed = 0
    
    for label, properties, constraint_type, description in COMMON_CONSTRAINTS:
        if await create_constraint(label, properties, constraint_type, description):
            success += 1
        else:
            failed += 1
    
    return success, failed

async def list_constraints() -> None:
    """List all constraints in the database."""
    constraints = await get_existing_constraints()
    
    if not constraints:
        print("No constraints found in the database.")
        return
    
    print("\n=== Database Constraints ===")
    for constr in sorted(constraints, key=lambda x: x.get('name', '')):
        print(f"\nName:       {constr.get('name', 'N/A')}")
        print(f"Type:       {constr.get('type', 'N/A')}")
        print(f"EntityType: {constr.get('entityType', 'N/A')}")
        print(f"Labels:     {', '.join(constr.get('labelsOrTypes', ['N/A']))}")
        print(f"Properties: {', '.join(constr.get('properties', ['N/A']))}")
        print(f"Ownership:  {constr.get('ownedIndex', 'N/A')}")
    
    print(f"\nTotal constraints: {len(constraints)}")

async def check_constraint_violations() -> Dict[str, List[Dict]]:
    """Check for any constraint violations in the database."""
    constraints = await get_existing_constraints()
    violations = {}
    
    for constr in constraints:
        if constr.get('type') == 'UNIQUENESS':
            props = constr.get('properties', [])
            if not props:
                continue
                
            label = constr.get('labelsOrTypes', [''])[0]
            if not label:
                continue
                
            # Check for duplicate values
            prop_list = ", ".join([f"n.{p}" for p in props])
            query = f"""
            MATCH (n:{label})
            WITH {prop_list}, count(*) as count
            WHERE count > 1
            RETURN {{properties: [{prop_list}], count: count}} as duplicates
            """
            
            try:
                results = await execute_query(query)
                if results:
                    violations[constr['name']] = results
            except Exception as e:
                logger.error(f"Error checking constraint {constr['name']}: {e}")
    
    return violations

async def main():
    """Main function to manage Neo4j constraints."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage Neo4j constraints")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create constraint command
    create_parser = subparsers.add_parser("create", help="Create a constraint")
    create_parser.add_argument("label", help="Node label for the constraint")
    create_parser.add_argument("properties", nargs="+", help="Properties to constrain")
    create_parser.add_argument("type", choices=["UNIQUE", "NOT NULL"], help="Type of constraint")
    create_parser.add_argument("--description", "-d", default="", help="Constraint description")
    
    # Drop constraint command
    drop_parser = subparsers.add_parser("drop", help="Drop a constraint")
    drop_parser.add_argument("constraint_name", help="Name of the constraint to drop")
    
    # List constraints command
    subparsers.add_parser("list", help="List all constraints")
    
    # Create common constraints command
    subparsers.add_parser("create-common", help="Create common constraints")
    
    # Check for violations
    subparsers.add_parser("check", help="Check for constraint violations")
    
    args = parser.parse_args()
    
    try:
        # Initialize Neo4j connection
        await init_neo4j()
        
        # Execute the requested command
        if args.command == "create":
            await create_constraint(args.label, args.properties, args.type, args.description)
        elif args.command == "drop":
            await drop_constraint(args.constraint_name)
        elif args.command == "list":
            await list_constraints()
        elif args.command == "create-common":
            print("Creating common constraints...")
            success, failed = await create_common_constraints()
            print(f"\nCreated {success} constraints, {failed} failed")
        elif args.command == "check":
            print("Checking for constraint violations...")
            violations = await check_constraint_violations()
            if violations:
                print("\n=== Constraint Violations ===")
                for constr_name, vios in violations.items():
                    print(f"\nConstraint: {constr_name}")
                    for i, vio in enumerate(vios, 1):
                        print(f"  {i}. {vio}")
            else:
                print("\nNo constraint violations found.")
        else:
            parser.print_help()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    finally:
        # Close Neo4j connection
        await close_neo4j()

if __name__ == "__main__":
    asyncio.run(main())
