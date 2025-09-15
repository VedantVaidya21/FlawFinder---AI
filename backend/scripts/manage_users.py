#!/usr/bin/env python3
"""
Manage Neo4j database users and permissions.

This script provides utilities for managing database users, roles, and permissions.
"""
import asyncio
import getpass
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import our standalone Neo4j utilities
from neo4j_utils import init_neo4j, close_neo4j, execute_query

# Direct Neo4j configuration - can be overridden by command line arguments
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

# Common roles and their permissions
ROLE_PERMISSIONS = {
    "admin": {
        "description": "Full access to all databases and administrative functions",
        "privileges": [
            "ACCESS",
            "ALL DATABASE PRIVILEGES",
            "ALL DBMS PRIVILEGES",
            "ALL PRIVILEGES"
        ]
    },
    "developer": {
        "description": "Can read and write to all application databases",
        "privileges": [
            "ACCESS",
            "READ",
            "WRITE",
            "CREATE",
            "DELETE",
            "MATCH",
            "MERGE",
            "SET",
            "REMOVE",
            "DELETE"
        ]
    },
    "analyst": {
        "description": "Read-only access to all application databases",
        "privileges": [
            "ACCESS",
            "READ",
            "MATCH"
        ]
    },
    "app_user": {
        "description": "Standard application user with limited write access",
        "privileges": [
            "ACCESS",
            "READ",
            "MATCH",
            "CREATE",
            "MERGE",
            "SET",
            "DELETE"
        ]
    }
}

class Neo4jUserManager:
    """Manages Neo4j users and permissions."""
    
    async def user_exists(self, username: str) -> bool:
        """Check if a user exists."""
        result = await execute_query(
            "SHOW USERS YIELD user WHERE user = $username RETURN count(*) > 0 as exists",
            {"username": username}
        )
        return result[0]["exists"] if result else False
    
    async def create_user(self, username: str, password: str, require_password_change: bool = True) -> bool:
        """Create a new database user."""
        if await self.user_exists(username):
            logger.warning(f"User {username} already exists")
            return False
        
        try:
            # In Neo4j 4.4+, we use the CREATE USER command
            query = f"CREATE USER {username} SET PASSWORD $password"
            if require_password_change:
                query += " CHANGE REQUIRED"
            
            await execute_query(
                query,
                {"password": password},
                read_only=False
            )
            
            logger.info(f"Created user: {username}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create user {username}: {e}")
            return False
    
    async def delete_user(self, username: str) -> bool:
        """Delete a database user."""
        if not await self.user_exists(username):
            logger.warning(f"User {username} does not exist")
            return False
            
        try:
            await execute_query(f"DROP USER {username}", read_only=False)
            logger.info(f"Deleted user: {username}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete user {username}: {e}")
            return False
    
    async def set_user_password(self, username: str, password: str) -> bool:
        """Set a user's password."""
        if not await self.user_exists(username):
            logger.error(f"User {username} does not exist")
            return False
            
        try:
            await execute_query(
                f"ALTER USER {username} SET PASSWORD $password",
                {"password": password},
                read_only=False
            )
            logger.info(f"Updated password for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Failed to set password for user {username}: {e}")
            return False
    
    async def list_users(self) -> List[Dict]:
        """List all database users."""
        result = await execute_query("SHOW USERS YIELD user, roles, passwordChangeRequired, suspended, homeDatabase")
        return result if result else []
    
    async def role_exists(self, role: str) -> bool:
        """Check if a role exists."""
        result = await execute_query(
            "SHOW ROLES YIELD role WHERE role = $role RETURN count(*) > 0 as exists",
            {"role": role}
        )
        return result[0]["exists"] if result else False
    
    async def create_role(self, role: str, description: str = "") -> bool:
        """Create a new role."""
        if await self.role_exists(role):
            logger.warning(f"Role {role} already exists")
            return False
            
        try:
            query = f"CREATE ROLE {role}"
            if description:
                query += f" AS COPY OF $description"
            
            await execute_query(
                query,
                {"description": description},
                read_only=False
            )
            
            logger.info(f"Created role: {role}")
            return True
        except Exception as e:
            logger.error(f"Failed to create role {role}: {e}")
            return False
    
    async def delete_role(self, role: str) -> bool:
        """Delete a role."""
        if not await self.role_exists(role):
            logger.warning(f"Role {role} does not exist")
            return False
            
        try:
            await execute_query(f"DROP ROLE {role}", read_only=False)
            logger.info(f"Deleted role: {role}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete role {role}: {e}")
            return False
    
    async def assign_role(self, username: str, role: str) -> bool:
        """Assign a role to a user."""
        if not await self.user_exists(username):
            logger.error(f"User {username} does not exist")
            return False
            
        if not await self.role_exists(role):
            logger.error(f"Role {role} does not exist")
            return False
            
        try:
            await execute_query(f"GRANT ROLE {role} TO {username}", read_only=False)
            logger.info(f"Granted role {role} to user {username}")
            return True
        except Exception as e:
            logger.error(f"Failed to grant role {role} to user {username}: {e}")
            return False
    
    async def revoke_role(self, username: str, role: str) -> bool:
        """Revoke a role from a user."""
        if not await self.user_exists(username):
            logger.error(f"User {username} does not exist")
            return False
            
        if not await self.role_exists(role):
            logger.error(f"Role {role} does not exist")
            return False
            
        try:
            await execute_query(f"REVOKE ROLE {role} FROM {username}", read_only=False)
            logger.info(f"Revoked role {role} from user {username}")
            return True
        except Exception as e:
            logger.error(f"Failed to revoke role {role} from user {username}: {e}")
            return False
    
    async def get_user_roles(self, username: str) -> List[str]:
        """Get all roles assigned to a user."""
        result = await execute_query(
            "SHOW USERS YIELD user, roles WHERE user = $username RETURN roles",
            {"username": username}
        )
        return result[0]["roles"] if result else []
    
    async def grant_privilege(self, role: str, privilege: str, database: str = "*") -> bool:
        """Grant a privilege to a role."""
        if not await self.role_exists(role):
            logger.error(f"Role {role} does not exist")
            return False
            
        try:
            if database == "*":
                await execute_query(
                    f"GRANT {privilege} ON DBMS TO {role}",
                    read_only=False
                )
            else:
                await execute_query(
                    f"GRANT {privilege} ON DATABASE {database} TO {role}",
                    read_only=False
                )
            
            logger.info(f"Granted {privilege} on {database} to role {role}")
            return True
        except Exception as e:
            logger.error(f"Failed to grant {privilege} on {database} to role {role}: {e}")
            return False
    
    async def revoke_privilege(self, role: str, privilege: str, database: str = "*") -> bool:
        """Revoke a privilege from a role."""
        if not await self.role_exists(role):
            logger.error(f"Role {role} does not exist")
            return False
            
        try:
            if database == "*":
                await execute_query(
                    f"REVOKE {privilege} ON DBMS FROM {role}",
                    read_only=False
                )
            else:
                await execute_query(
                    f"REVOKE {privilege} ON DATABASE {database} FROM {role}",
                    read_only=False
                )
            
            logger.info(f"Revoked {privilege} on {database} from role {role}")
            return True
        except Exception as e:
            logger.error(f"Failed to revoke {privilege} on {database} from role {role}: {e}")
            return False
    
    async def setup_common_roles(self) -> Dict[str, bool]:
        """Set up common roles with appropriate permissions."""
        results = {}
        
        for role, config in ROLE_PERMISSIONS.items():
            # Create the role if it doesn't exist
            created = await self.create_role(role, config["description"])
            results[f"create_role_{role}"] = created
            
            # Grant all specified privileges
            for privilege in config["privileges"]:
                granted = await self.grant_privilege(role, privilege)
                results[f"grant_{privilege.lower()}_to_{role}"] = granted
        
        return results

async def prompt_password() -> str:
    """Prompt for a password with confirmation."""
    while True:
        password = getpass.getpass("Enter password: ")
        confirm = getpass.getpass("Confirm password: ")
        
        if password == confirm:
            return password
        print("Passwords do not match. Please try again.")

async def main():
    """Main entry point for the user management tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage Neo4j database users and permissions")
    
    # Add database connection options
    parser.add_argument("--uri", help="Neo4j URI", default=NEO4J_URI)
    parser.add_argument("--user", help="Neo4j username", default=NEO4J_USER)
    parser.add_argument("--password", help="Neo4j password", default=NEO4J_PASSWORD)
    parser.add_argument("--database", help="Neo4j database", default=NEO4J_DATABASE)
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # User management commands
    user_parser = subparsers.add_parser("user", help="User management")
    user_subparsers = user_parser.add_subparsers(dest="user_command")
    
    # Create user
    create_user_parser = user_subparsers.add_parser("create", help="Create a new user")
    create_user_parser.add_argument("username", help="Username for the new user")
    create_user_parser.add_argument("--password", help="Password (prompt if not provided)", default=None)
    
    # Delete user
    delete_user_parser = user_subparsers.add_parser("delete", help="Delete a user")
    delete_user_parser.add_argument("username", help="Username to delete")
    
    # List users
    user_subparsers.add_parser("list", help="List all users")
    
    # Set password
    set_pass_parser = user_subparsers.add_parser("set-password", help="Set a user's password")
    set_pass_parser.add_argument("username", help="Username to update")
    set_pass_parser.add_argument("--password", help="New password (prompt if not provided)", default=None)
    
    # Role management commands
    role_parser = subparsers.add_parser("role", help="Role management")
    role_subparsers = role_parser.add_subparsers(dest="role_command")
    
    # Create role
    create_role_parser = role_subparsers.add_parser("create", help="Create a new role")
    create_role_parser.add_argument("role", help="Name of the role to create")
    create_role_parser.add_argument("--description", help="Description of the role", default="")
    
    # Delete role
    delete_role_parser = role_subparsers.add_parser("delete", help="Delete a role")
    delete_role_parser.add_argument("role", help="Name of the role to delete")
    
    # List roles
    role_subparsers.add_parser("list", help="List all roles")
    
    # Assign role to user
    assign_parser = role_subparsers.add_parser("assign", help="Assign a role to a user")
    assign_parser.add_argument("username", help="Username to assign the role to")
    assign_parser.add_argument("role", help="Role to assign")
    
    # Revoke role from user
    revoke_parser = role_subparsers.add_parser("revoke", help="Revoke a role from a user")
    revoke_parser.add_argument("username", help="Username to revoke the role from")
    revoke_parser.add_argument("role", help="Role to revoke")
    
    # Setup common roles
    setup_parser = subparsers.add_parser("setup-roles", help="Set up common roles with default permissions")
    
    # List common roles
    subparsers.add_parser("list-common-roles", help="List common roles and their permissions")
    
    args = parser.parse_args()
    
    # If no command is provided, show help
    if not hasattr(args, 'command') or not args.command:
        parser.print_help()
        return
    
    try:
        # Initialize Neo4j connection with provided or default parameters
        await init_neo4j(
            uri=args.uri,
            user=args.user,
            password=args.password,
            database=args.database
        )
        
        manager = Neo4jUserManager()
        
        # Handle commands
        if args.command == "user":
            if args.user_command == "create":
                password = args.password or await prompt_password()
                success = await manager.create_user(args.username, password)
                print(f"User {args.username} {'created successfully' if success else 'creation failed'}")
                
            elif args.user_command == "delete":
                confirm = input(f"Are you sure you want to delete user {args.username}? (y/N) ").lower()
                if confirm == 'y':
                    success = await manager.delete_user(args.username)
                    print(f"User {args.username} {'deleted successfully' if success else 'deletion failed'}")
                else:
                    print("Operation cancelled")
                    
            elif args.user_command == "list":
                users = await manager.list_users()
                print("\n=== Database Users ===")
                for user in users:
                    print(f"\nUsername: {user['user']}")
                    print(f"Roles: {', '.join(user['roles']) if user['roles'] else 'None'}")
                    print(f"Password Change Required: {user['passwordChangeRequired']}")
                    print(f"Suspended: {user['suspended']}")
                    if 'homeDatabase' in user:
                        print(f"Home Database: {user['homeDatabase']}")
                
            elif args.user_command == "set-password":
                password = args.password or await prompt_password()
                success = await manager.set_user_password(args.username, password)
                print(f"Password for {args.username} {'updated successfully' if success else 'update failed'}")
                
        elif args.command == "role":
            if args.role_command == "create":
                success = await manager.create_role(args.role, args.description)
                print(f"Role {args.role} {'created successfully' if success else 'creation failed'}")
                
            elif args.role_command == "delete":
                confirm = input(f"Are you sure you want to delete role {args.role}? (y/N) ").lower()
                if confirm == 'y':
                    success = await manager.delete_role(args.role)
                    print(f"Role {args.role} {'deleted successfully' if success else 'deletion failed'}")
                else:
                    print("Operation cancelled")
                    
            elif args.role_command == "list":
                users = await manager.list_users()
                all_roles = set()
                for user in users:
                    all_roles.update(user.get('roles', []))
                
                print("\n=== Database Roles ===")
                for role in sorted(all_roles):
                    print(f"- {role}")
                    users_with_role = [u['user'] for u in users if role in u.get('roles', [])]
                    if users_with_role:
                        print(f"  Assigned to: {', '.join(users_with_role)}")
                    else:
                        print("  No users assigned")
                
            elif args.role_command == "assign":
                success = await manager.assign_role(args.username, args.role)
                print(f"Role {args.role} {'assigned to' if success else 'failed to assign to'} user {args.username}")
                
            elif args.role_command == "revoke":
                success = await manager.revoke_role(args.username, args.role)
                print(f"Role {args.role} {'revoked from' if success else 'failed to revoke from'} user {args.username}")
                
        elif args.command == "setup-roles":
            print("Setting up common roles...")
            results = await manager.setup_common_roles()
            
            print("\n=== Setup Results ===")
            for action, success in results.items():
                status = "✓" if success else "✗"
                print(f"{status} {action}")
            
            success_count = sum(1 for s in results.values() if s)
            total = len(results)
            print(f"\nCompleted: {success_count}/{total} operations successful")
            
        elif args.command == "list-common-roles":
            print("\n=== Common Roles and Permissions ===")
            for role, config in ROLE_PERMISSIONS.items():
                print(f"\n{role.upper()} - {config['description']}")
                print("  Permissions:")
                for priv in sorted(config['privileges']):
                    print(f"    - {priv}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    finally:
        # Close Neo4j connection
        await close_neo4j()

if __name__ == "__main__":
    asyncio.run(main())