from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from ..core.neo4j import get_neo4j


class BrutalityScoreBase(BaseModel):
    score: float  # 0-100
    breakdown: Optional[Dict[str, Any]] = None  # Detailed breakdown of score components
    version: Optional[str] = None  # Version of scoring algorithm
    process_flow_id: str


class BrutalityScoreCreate(BrutalityScoreBase):
    pass


class BrutalityScoreUpdate(BaseModel):
    score: Optional[float] = None
    breakdown: Optional[Dict[str, Any]] = None
    version: Optional[str] = None


class BrutalityScore(BrutalityScoreBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class BrutalityScoreService:
    """Neo4j data access layer for BrutalityScore operations"""

    @staticmethod
    def create_brutality_score(score_data: BrutalityScoreCreate) -> Optional[BrutalityScore]:
        """Create a new brutality score in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (bs:BrutalityScore {
            id: randomUUID(),
            score: $score,
            breakdown: $breakdown,
            version: $version,
            process_flow_id: $process_flow_id,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN bs
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "score": score_data.score,
                "breakdown": score_data.breakdown,
                "version": score_data.version,
                "process_flow_id": score_data.process_flow_id
            })

            if result:
                record = result[0]["bs"]
                return BrutalityScore(
                    id=record["id"],
                    score=record["score"],
                    breakdown=record.get("breakdown"),
                    version=record.get("version"),
                    process_flow_id=record["process_flow_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating brutality score: {e}")
        return None

    @staticmethod
    def get_brutality_score_by_id(score_id: str) -> Optional[BrutalityScore]:
        """Get brutality score by ID"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (bs:BrutalityScore {id: $id, is_active: true})
        RETURN bs
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": score_id})
            if result:
                record = result[0]["bs"]
                return BrutalityScore(
                    id=record["id"],
                    score=record["score"],
                    breakdown=record.get("breakdown"),
                    version=record.get("version"),
                    process_flow_id=record["process_flow_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting brutality score by ID: {e}")
        return None

    @staticmethod
    def update_brutality_score(score_id: str, score_data: BrutalityScoreUpdate) -> Optional[BrutalityScore]:
        """Update brutality score information"""
        neo4j_conn = get_neo4j()

        # Build dynamic update query
        set_parts = ["bs.updated_at = datetime()"]
        params = {"id": score_id}

        if score_data.score is not None:
            set_parts.append("bs.score = $score")
            params["score"] = score_data.score
        if score_data.breakdown is not None:
            set_parts.append("bs.breakdown = $breakdown")
            params["breakdown"] = score_data.breakdown
        if score_data.version is not None:
            set_parts.append("bs.version = $version")
            params["version"] = score_data.version

        query = f"""
        MATCH (bs:BrutalityScore {{id: $id, is_active: true}})
        SET {', '.join(set_parts)}
        RETURN bs
        """

        try:
            result = neo4j_conn.execute_query(query, params)
            if result:
                record = result[0]["bs"]
                return BrutalityScore(
                    id=record["id"],
                    score=record["score"],
                    breakdown=record.get("breakdown"),
                    version=record.get("version"),
                    process_flow_id=record["process_flow_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error updating brutality score: {e}")
        return None

    @staticmethod
    def delete_brutality_score(score_id: str) -> bool:
        """Soft delete brutality score by setting is_active to false"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (bs:BrutalityScore {id: $id, is_active: true})
        SET bs.is_active = false, bs.updated_at = datetime()
        RETURN count(bs) as deleted_count
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": score_id})
            return result and result[0]["deleted_count"] > 0
        except Exception as e:
            print(f"Error deleting brutality score: {e}")
        return False

    @staticmethod
    def get_brutality_scores_by_process_flow(process_flow_id: str, skip: int = 0, limit: int = 100) -> List[BrutalityScore]:
        """Get all brutality scores for a specific process flow with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (bs:BrutalityScore {process_flow_id: $process_flow_id, is_active: true})
        RETURN bs
        ORDER BY bs.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"process_flow_id": process_flow_id, "skip": skip, "limit": limit})
            scores = []
            for record in result:
                score_data = record["bs"]
                scores.append(BrutalityScore(
                    id=score_data["id"],
                    score=score_data["score"],
                    breakdown=score_data.get("breakdown"),
                    version=score_data.get("version"),
                    process_flow_id=score_data["process_flow_id"],
                    created_at=score_data["created_at"].to_native(),
                    updated_at=score_data["updated_at"].to_native(),
                    is_active=score_data["is_active"]
                ))
            return scores
        except Exception as e:
            print(f"Error getting brutality scores by process flow: {e}")
        return []

    @staticmethod
    def get_brutality_scores_by_version(version: str, skip: int = 0, limit: int = 100) -> List[BrutalityScore]:
        """Get all brutality scores for a specific version with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (bs:BrutalityScore {version: $version, is_active: true})
        RETURN bs
        ORDER BY bs.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"version": version, "skip": skip, "limit": limit})
            scores = []
            for record in result:
                score_data = record["bs"]
                scores.append(BrutalityScore(
                    id=score_data["id"],
                    score=score_data["score"],
                    breakdown=score_data.get("breakdown"),
                    version=score_data.get("version"),
                    process_flow_id=score_data["process_flow_id"],
                    created_at=score_data["created_at"].to_native(),
                    updated_at=score_data["updated_at"].to_native(),
                    is_active=score_data["is_active"]
                ))
            return scores
        except Exception as e:
            print(f"Error getting brutality scores by version: {e}")
        return []

    @staticmethod
    def get_brutality_scores_above_threshold(threshold: float, skip: int = 0, limit: int = 100) -> List[BrutalityScore]:
        """Get all brutality scores above a certain threshold with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (bs:BrutalityScore {is_active: true})
        WHERE bs.score >= $threshold
        RETURN bs
        ORDER BY bs.score DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"threshold": threshold, "skip": skip, "limit": limit})
            scores = []
            for record in result:
                score_data = record["bs"]
                scores.append(BrutalityScore(
                    id=score_data["id"],
                    score=score_data["score"],
                    breakdown=score_data.get("breakdown"),
                    version=score_data.get("version"),
                    process_flow_id=score_data["process_flow_id"],
                    created_at=score_data["created_at"].to_native(),
                    updated_at=score_data["updated_at"].to_native(),
                    is_active=score_data["is_active"]
                ))
            return scores
        except Exception as e:
            print(f"Error getting brutality scores above threshold: {e}")
        return []
