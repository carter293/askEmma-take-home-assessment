from pydantic import BaseModel, Field
from typing import Optional


class Email(BaseModel):
    to: str = Field(
        description='Comma separated email recipients i.e. "James Robinson <james@gmail.com>, Reuben Hayden <reuben@gmail.com>". If email, just put the name, if both email and name is unknown please input title of intended recipient.'
    )
    cc: Optional[str] = Field(
        default=None,
        description='Comma separated CC email recipients i.e. "James Robinson <james@gmail.com>, Reuben Hayden <reuben@gmail.com>". If email, just put the name, if both email and name is unknown please input title of intended recipient.'
    )
    bcc: Optional[str] = Field(
        default=None,
        description='Comma separated BCC email recipients i.e. "James Robinson <james@gmail.com>, Reuben Hayden <reuben@gmail.com>". If email, just put the name, if both email and name is unknown please input title of intended recipient.'
    )
    subject: str = Field(description="Subject line of email.")
    body: str = Field(description="Body of email, please use markdown.")
