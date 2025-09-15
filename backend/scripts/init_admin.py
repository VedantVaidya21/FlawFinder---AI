#!/usr/bin/env python3
"""
Initialize admin user in Neo4j database.
Run this script after setting up the database.
"""
import asyncio
import getpass
from datetime import datetime
from app.core.database import get_driver, get_password_hash
from app.core.config import settings

async def init_admin():
    """Initialize admin user in the database"""
    email = input("Enter admin email (default: admin@example.com): ") or "admin@example.com"
    password = getpass.getpass("Enter admin password: ")
    
    if not password:
        print("Error: Password cannot be empty")
        return
    
    hashed_password = get_password_hash(password)
    
    query = """
    MERGE (u:User {email: $email})
    ON CREATE SET
        u.id = randomUUID(),
        u.email = $email,
        u.hashed_password = $hashed_password,
        u.full_name = 'Admin User',
        u.role = 'admin',
        u.status = 'active',
        u.is_active = true,
        u.created_at = datetime(),
        u.updated_at = datetime()
    RETURN u
    """
    
    try:
        driver = await get_driver()
        async with driver.session() as session:
            result = await session.run(
                query,
                email=email,
                hashed_password=hashed_password
            )
            record = await result.single()
            
            if record:
                print(f"✅ Admin user '{email}' created/updated successfully!")
            else:
                print("❌ Failed to create admin user")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await driver.close()

if __name__ == "__main__":
    asyncio.run(init_admin())
