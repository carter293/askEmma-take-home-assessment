from pydantic import BaseModel, Field
from typing import Optional
from .email import Email


class IncidentReport(BaseModel):
    date_time_of_incident: Optional[str] = Field(
        default=None,
        description="Date and time when the incident occurred in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"
    )
    service_user_name: str = Field(
        description="Full name of the service user involved in the incident"
    )
    location_of_incident: Optional[str] = Field(
        default=None,
        description="Specific location where the incident took place"
    )
    type_of_incident: str = Field(
        description="Category of incident (e.g., Fall, Medical Emergency, Behavioral, etc.)"
    )
    description_of_incident: str = Field(
        description="Detailed description of what happened during the incident"
    )
    immediate_actions_taken: Optional[str] = Field(
        default=None,
        description="Actions taken immediately following the incident"
    )
    first_aid_administered: bool = Field(
        description="Whether first aid was provided"
    )
    emergency_services_contacted: bool = Field(
        description="Whether emergency services (ambulance, police, fire) were called"
    )
    who_was_notified: Optional[str] = Field(
        default=None,
        description="Names and roles of people notified about the incident"
    )
    witnesses: Optional[str] = Field(
        default=None,
        description="Names of any witnesses to the incident"
    )
    agreed_next_steps: Optional[str] = Field(
        default=None,
        description="Follow-up actions agreed upon after the incident"
    )
    risk_assessment_needed: bool = Field(
        description="Whether a risk assessment is required"
    )
    risk_assessment_type: Optional[str] = Field(
        default=None,
        description="Type of risk assessment needed (e.g., Moving and Handling, Environmental)"
    )


class PolicyProcessingResults(BaseModel):
    emails: list[Email]
    report: IncidentReport
    policy_ids: list[str] = Field(
        description="The IDs of the returned situations you used to fill out the incident report as well as draft emails."
    )
    reasoning: list[str] = Field(
        description="A list of reasons why the outputs are in line with policy, specifically which parts of the text are related to specificaly parts of the policy. Please use quotations and please use markdown"
    )


class PolicyProcessingResultsWithFullPolicy(PolicyProcessingResults):
    full_policy_texts: list[str]
