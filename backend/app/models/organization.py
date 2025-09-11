from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..core.neo4j import get_neo4j


class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None  # small, medium, large, enterprise


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None


class Organization(OrganizationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class OrganizationService:
    """Neo4j data access layer for Organization operations"""

    @staticmethod
    def create_organization(org_data: OrganizationCreate) -> Optional[Organization]:
        """Create a new organization in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (o:Organization {
            id: randomUUID(),
            name: $name,
            description: $description,
            industry: $industry,
            size: $size,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN o
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "name": org_data.name,
                "description": org_data.description,
                "industry": org_data.industry,
                "size": org_data.size
            })

            if result:
                record = result[0]["o"]
                return Organization(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    industry=record.get("industry"),
                    size=record.get("size"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating organization: {e}")
        return None

    @staticmethod
    def get_organization_by_id(org_id: str) -> Optional[Organization]:
        """Get organization by ID"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (o:Organization {id: $id, is_active: true})
        RETURN o
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": org_id})
            if result:
                record = result[0]["o"]
                return Organization(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    industry=record.get("industry"),
                    size=record.get("size"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting organization by ID: {e}")
        return None

    @staticmethod
    def update_organization(org_id: str, org_data: OrganizationUpdate) -> Optional[Organization]:
        """Update organization information"""
        neo4j_conn = get_neo4j()

        # Build dynamic update query
        set_parts = ["o.updated_at = datetime()"]
        params = {"id": org_id}

        if org_data.name is not None:
            set_parts.append("o.name = $name")
            params["name"] = org_data.name
        if org_data.description is not None:
            set_parts.append("o.description = $description")
            params["description"] = org_data.description
        if org_data.industry is not None:
            set_parts.append("o.industry = $industry")
            params["industry"] = org_data.industry
        if org_data.size is not None:
            set_parts.append("o.size = $size")
            params["size"] = org_data.size

        query = f"""
        MATCH (o:Organization {{id: $id, is_active: true}})
        SET {', '.join(set_parts)}
        RETURN o
        """

        try:
            result = neo4j_conn.execute_query(query, params)
            if result:
                record = result[0]["o"]
                return Organization(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    industry=record.get("industry"),
                    size=record.get("size"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error updating organization: {e}")
        return None

    @staticmethod
    def delete_organization(org_id: str) -> bool:
        """Soft delete organization by setting is_active to false"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (o:Organization {id: $id, is_active: true})
        SET o.is_active = false, o.updated_at = datetime()
        RETURN count(o) as deleted_count
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": org_id})
            return result and result[0]["deleted_count"] > 0
        except Exception as e:
            print(f"Error deleting organization: {e}")
        return False

    @staticmethod
    def get_all_organizations(skip: int = 0, limit: int = 100) -> List[Organization]:
        """Get all active organizations with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (o:Organization {is_active: true})
        RETURN o
        ORDER BY o.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"skip": skip, "limit": limit})
            organizations = []
            for record in result:
                org_data = record["o"]
                organizations.append(Organization(
                    id=org_data["id"],
                    name=org_data["name"],
                    description=org_data.get("description"),
                    industry=org_data.get("industry"),
                    size=org_data.get("size"),
                    created_at=org_data["created_at"].to_native(),
                    updated_at=org_data["updated_at"].to_native(),
                    is_active=org_data["is_active"]
                ))
            return organizations
        except Exception as e:
            print(f"Error getting all organizations: {e}")
        return []

    @staticmethod
    def get_organization_users(org_id: str) -> List[dict]:
        """Get all users belonging to an organization"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (o:Organization {id: $id, is_active: true})<-[:BELONGS_TO]-(u:User {is_active: true})
        RETURN u.id as id, u.email as email, u.first_name as first_name,
               u.last_name as last_name, u.role as role, u.status as status
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": org_id})
            return [dict(record) for record in result]
        except Exception as e:
            print(f"Error getting organization users: {e}")
        return []
