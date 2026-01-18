import aiosqlite
import sqlite_vec
from os import path
from os.path import join
import struct
import hashlib
from ..clients import client
import logging

logger = logging.getLogger(__name__)

db_path = join(path.dirname(__file__), "../../db/askEmma.sqlite")


async def get_db():
    """Get database connection with sqlite-vec loaded"""
    try:
        if not path.exists(db_path):
            logger.error(f"Database file not found at path: {db_path}")
            raise FileNotFoundError(f"Database file not found: {db_path}")

        conn = await aiosqlite.connect(db_path)
        await conn.enable_load_extension(True)
        await conn.load_extension(sqlite_vec.loadable_path())
        await conn.enable_load_extension(False)
        return conn
    except aiosqlite.Error as e:
        logger.error(f"Failed to connect to database: {str(e)}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_db: {str(e)}", exc_info=True)
        raise


def serialize(vector: list[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)


async def search_situation(description: str):
    if not description or not description.strip():
        logger.warning("Empty description provided to search_situation")
        return []

    db = None
    try:
        # Generate embedding
        try:
            logger.info("Generating embedding for search")
            response = await client.embeddings.create(
                input=description, model="text-embedding-3-small"
            )
            query_embedding = response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to create embedding: {str(e)}", exc_info=True)
            raise RuntimeError(f"Embedding generation failed: {str(e)}")

        # Connect to database
        db = await get_db()
        db.row_factory = aiosqlite.Row

        # Execute query
        try:
            async with db.execute(
                """
                    SELECT
                        vec_situations.id,
                        distance,
                        full_policy_text,
                        situation_description
                    FROM vec_situations
                    LEFT JOIN situations ON situations.id = vec_situations.id
                    WHERE situation_embedding MATCH ?
                        AND k = 10
                    ORDER BY distance
                """,
                [serialize(query_embedding)],
            ) as cur:
                rows = await cur.fetchall()
                result = [dict(r) for r in rows]
                logger.info(f"Vector search returned {len(result)} situations")
        except aiosqlite.Error as e:
            logger.error(f"Database query error in search_situation: {str(e)}", exc_info=True)
            raise

        # Deduplicate results
        unique_policies = []
        seen = []
        try:
            for situation in result:
                if not situation.get('full_policy_text'):
                    logger.warning(f"Situation {situation.get('id')} missing full_policy_text")
                    continue
                hash_policy = int(hashlib.sha1(situation['full_policy_text'].encode("utf-8")).hexdigest(), 16) % (10 ** 8)
                if hash_policy not in seen:
                    seen.append(hash_policy)
                    unique_policies.append(situation)
        except Exception as e:
            logger.error(f"Error deduplicating policies: {str(e)}", exc_info=True)
            raise

        return unique_policies
    except Exception as e:
        logger.error(f"Error in search_situation: {str(e)}", exc_info=True)
        raise
    finally:
        if db:
            try:
                await db.close()
            except Exception as e:
                logger.warning(f"Error closing database connection: {str(e)}")


async def get_full_policy(ids: list[int]):
    if not ids:
        logger.warning("Empty ids list provided to get_full_policy")
        return []

    logger.info(f"Fetching full policies for IDs: {ids}")

    # Validate all IDs are integers
    try:
        ids = [int(id_val) for id_val in ids]
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid ID type in get_full_policy: {str(e)}")
        raise ValueError(f"All policy IDs must be integers: {str(e)}")

    db = None
    try:
        db = await get_db()
        db.row_factory = aiosqlite.Row

        # Execute query
        try:
            async with db.execute(
                """
                    SELECT
                        full_policy_text
                    FROM situations
                    WHERE id in ({})
                """.format(','.join(['?']*len(ids))),
                ids,
            ) as cur:
                rows = await cur.fetchall()
                result = [dict(r) for r in rows]
        except aiosqlite.Error as e:
            logger.error(f"Database query error in get_full_policy: {str(e)}", exc_info=True)
            raise

        # Deduplicate results
        unique_policies: list[dict[str, str],] = []
        seen = []
        try:
            for situation in result:
                if not situation.get('full_policy_text'):
                    logger.warning(f"Situation missing full_policy_text in result")
                    continue
                hash_policy = int(hashlib.sha1(situation['full_policy_text'].encode("utf-8")).hexdigest(), 16) % (10 ** 8)
                if hash_policy not in seen:
                    seen.append(hash_policy)
                    unique_policies.append(situation)
        except Exception as e:
            logger.error(f"Error deduplicating policies: {str(e)}", exc_info=True)
            raise

        if not unique_policies:
            logger.warning(f"No policies found for IDs: {ids}")

        return unique_policies
    except Exception as e:
        logger.error(f"Error in get_full_policy: {str(e)}", exc_info=True)
        raise
    finally:
        if db:
            try:
                await db.close()
            except Exception as e:
                logger.warning(f"Error closing database connection: {str(e)}")