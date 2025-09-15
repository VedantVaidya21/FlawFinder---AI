from typing import Optional, Dict, Any, List, TypeVar, Type
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from ..core.database import db

T = TypeVar('T', bound='BaseNode')

class BaseNode(BaseModel):
    """Base model for all Neo4j nodes"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    label_name: str | None = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
    
    @classmethod
    async def create(cls: Type[T], **data) -> T:
        """Create a new node in Neo4j"""
        instance = cls(**data)
        await instance.save()
        return instance
    
    async def save(self) -> None:
        """Save the node to Neo4j"""
        self.updated_at = datetime.utcnow()
        props = self.dict(exclude={'id', 'created_at'})
        
        label = getattr(self.__class__, 'label_name', None) or self.__class__.__name__
        query = """
        MERGE (n:%s {id: $id})
        ON CREATE SET n += $props, n.created_at = $created_at
        ON MATCH SET n += $props
        RETURN n
        """ % label
        
        async with db.get_session() as session:
            await session.run(
                query,
                id=self.id,
                props=props,
                created_at=self.created_at.isoformat()
            )
    
    @classmethod
    async def get(cls: Type[T], id: str) -> Optional[T]:
        """Get a node by ID"""
        label = getattr(cls, 'label_name', None) or cls.__name__
        query = f"""
        MATCH (n:{label} {{id: $id}})
        RETURN n
        """
        async with db.get_session() as session:
            result = await session.run(query, id=id)
            data = await result.data()
            if not data:
                return None
            return cls(**data[0]['n'])
    
    @classmethod
    async def find_one(cls: Type[T], **filters) -> Optional[T]:
        """Find a single node matching the given filters"""
        if not filters:
            raise ValueError("At least one filter must be provided")
            
        filter_str = " AND ".join([f"n.{k} = ${k}" for k in filters.keys()])
        label = getattr(cls, 'label_name', None) or cls.__name__
        query = f"""
        MATCH (n:{label})
        WHERE {filter_str}
        RETURN n
        LIMIT 1
        """
        
        async with db.get_session() as session:
            result = await session.run(query, **filters)
            data = await result.data()
            if not data:
                return None
            return cls(**data[0]['n'])
    
    @classmethod
    async def find_all(cls: Type[T], **filters) -> List[T]:
        """Find all nodes matching the filters"""
        where_clause = " AND ".join([f"n.{k} = ${k}" for k in filters.keys()]) if filters else "1=1"
        label = getattr(cls, 'label_name', None) or cls.__name__
        query = f"""
        MATCH (n:{label})
        WHERE {where_clause}
        RETURN n
        """
        
        async with db.get_session() as session:
            result = await session.run(query, **filters)
            records = await result.values()
            
            return [cls(**record[0]) for record in records if record and record[0]]
    
    async def delete(self) -> None:
        """Delete this node from Neo4j"""
        query = f"""
        MATCH (n:{self.__class__.__name__} {{id: $id}})
        DETACH DELETE n
        """
        async with db.get_session() as session:
            await session.run(query, id=self.id)
    
    @classmethod
    def from_orm(cls, node_data: Dict[str, Any]) -> 'BaseNode':
        """Create a model instance from Neo4j node data"""
        return cls(**node_data)
