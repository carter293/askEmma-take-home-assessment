import sqlite3
import sqlite_vec
from os import listdir, path
from os.path import isfile, join
from pydantic import BaseModel
from openai import OpenAI
import struct
from dotenv import load_dotenv

load_dotenv()

POLICY_PATH = join(path.dirname(__file__), "policies")
DB_PATH = join(path.dirname(__file__), "../db/askEmma.sqlite")

client = OpenAI()
db = sqlite3.connect(DB_PATH)
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

# Setup Tables
db.execute(
    """
        CREATE TABLE IF NOT EXISTS situations (
          id INTEGER PRIMARY KEY,
          full_policy_text TEXT,
          situation_description TEXT
        );
    """
)

db.execute(
    """
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_situations USING vec0(
          id INTEGER PRIMARY KEY,
          situation_embedding FLOAT[1536]
        );
    """
)


# Types and Utils
class PolicyExamples(BaseModel):
    situation_descriptions: list[str]


class Policy(PolicyExamples):
    full_policy_text: str
    situation_embeddings: list[bytes]


def serialize(vector: list[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)


def insert_policy(policy: Policy):
    with db:
        for index, embedding in enumerate(policy.situation_embeddings):
            db.execute(
                "INSERT INTO situations(full_policy_text, situation_description) VALUES(?, ?)",
                [policy.full_policy_text, policy.situation_descriptions[index]],
            )
            situation_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

            db.execute(
                "INSERT INTO vec_situations(id, situation_embedding) VALUES(?, ?)",
                [situation_id, embedding],
            )


def vectorise_situation_descriptions(descriptions: list[str]) -> list[bytes]:
    embeddings = client.embeddings.create(
        input=descriptions, model="text-embedding-3-small"
    )
    serialized_embeddings = [serialize(arr.embedding) for arr in embeddings.data]
    return serialized_embeddings


policyFiles: list[str] = [
    POLICY_PATH + "/" + f for f in listdir(POLICY_PATH) if isfile(join(POLICY_PATH, f))
]
for policy in policyFiles:
    with open(policy) as data:
        policy_text = data.read()
        response = client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": """
                    Your job is to take a policy description and produce a variety example situations that would tightly and loosely match fit the policy. 
                    """,
                },
                {
                    "role": "user",
                    "content": f"Here is the policy:\n{policy_text}",
                },
            ],
            text_format=PolicyExamples,
        )
        situation_descriptions = response.output_parsed.situation_descriptions
        vectorised_descriptions = vectorise_situation_descriptions(situation_descriptions)
        newPolicy = Policy(
            situation_embeddings=vectorised_descriptions,
            full_policy_text=policy_text,
            situation_descriptions=situation_descriptions,
        )
        insert_policy(newPolicy)
        print(f"Inserted policy: {policy_text[:100]}...")