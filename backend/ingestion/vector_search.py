import sqlite3
import sqlite_vec
from openai import OpenAI
from os.path import join
from os import path
import struct
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

DB_PATH = join(path.dirname(__file__), "../db/askEmma.sqlite")
print(DB_PATH)
db = sqlite3.connect(DB_PATH)
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)




candidate = 'A service user trips and falls, resulting in a scrape on their knee. The carer cleans the wound and applies a bandage.'

def serialize(vector: list[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)


query_embedding = (
    client.embeddings.create(input=candidate, model="text-embedding-3-small")
    .data[0]
    .embedding
)

# results = db.execute(
#     """
#       SELECT
#         id,
#         distance,
#         situation_embedding,
#         full_policy_text,
#         situation_description
#       FROM vec_situations
#       WHERE situation_embedding MATCH ?
#         AND k = 3
#       ORDER BY distance
#     """,
#     [serialize(query_embedding)],
# ).fetchall()

# for row in results:
#     print(row)

results = db.execute(
    """
      SELECT
        vec_situations.id,
        distance,
        full_policy_text,
        situation_description
      FROM vec_situations
      LEFT JOIN situations ON situations.id = vec_situations.id
      WHERE situation_embedding MATCH ?
        AND k = 1
      ORDER BY distance
    """,
    [serialize(query_embedding)],
).fetchall()

for row in results:
    print(row)