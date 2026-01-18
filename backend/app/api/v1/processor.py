from ...db.db import get_full_policy
from fastapi import File, UploadFile, HTTPException, Form
from typing import Optional
from datetime import datetime
from agents import Agent, Runner
from app.schemas import PolicyProcessingResults, PolicyProcessingResultsWithFullPolicy
from fastapi import APIRouter
from ...utils.tools import search_policies
from ...utils.file_processing import process_uploaded_file
import logging
import aiosqlite

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/v1",  tags=["report"])

@router.post("/transcript")
async def process_transcript(
    text: Optional[str] = Form(""),
    file: Optional[UploadFile] = File(None)
) -> PolicyProcessingResultsWithFullPolicy:
    try:
        logger.info("Processing transcript request")
        textarea_text = text.strip() if text else ""
        file_text = ""

        # If file is provided, validate and extract content
        if file:
            try:
                logger.info(f"Processing uploaded file: {file.filename}")
                file_text = await process_uploaded_file(file)
            except ValueError as e:
                logger.warning(f"File validation error: {str(e)}")
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                logger.error(f"File processing error: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail="Failed to process uploaded file")

        # Ensure at least one source is provided
        if not textarea_text and not file_text:
            raise HTTPException(status_code=400, detail="Either text or file must be provided")

        # Initialize agent
        try:
            agent = Agent(
                name="Incident Reporter",
                tools=[search_policies],
                output_type=PolicyProcessingResults,
            )
        except Exception as e:
            logger.error(f"Agent initialization error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to initialize processing agent")

        current_time = datetime.now().isoformat()

        # Build prompt with conditional logic
        prompt_parts = [f"Current date and time: {current_time}\n"]
        prompt_parts.append("Please find the associated policy using a summary description of the situation in this transcript and return the incident response form. Please fill out the incident report and draft any appropriate emails\n")

        if textarea_text and file_text:
            prompt_parts.append(f"Transcript from text area:\n{textarea_text}\n")
            prompt_parts.append(f"Transcript from uploaded file:\n{file_text}")
        elif file_text:
            prompt_parts.append(f"Transcript: {file_text}")
        else:
            prompt_parts.append(f"Transcript: {textarea_text}")

        prompt = "\n".join(prompt_parts)

        # Run agent
        try:
            logger.info("Starting agent processing")
            result = await Runner.run(agent, prompt)
            final_output = result.final_output_as(PolicyProcessingResults)
            logger.info(f"Agent processing complete. Policy IDs: {final_output.policy_ids}")
        except Exception as e:
            logger.error(f"Agent processing error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to process transcript with agent")

        # Retrieve full policy texts
        try:
            if not final_output.policy_ids:
                logger.warning("No policy IDs returned from agent processing")
                policies_used = []
                full_policy_texts = []
            else:
                policies_used = await get_full_policy(final_output.policy_ids)
                full_policy_texts = [i["full_policy_text"] for i in policies_used]
                logger.info(f"Retrieved {len(full_policy_texts)} unique policies")
        except aiosqlite.Error as e:
            logger.error(f"Database error retrieving policies: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to retrieve policy information")
        except KeyError as e:
            logger.error(f"Missing expected field in policy data: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Invalid policy data structure")
        except Exception as e:
            logger.error(f"Unexpected error retrieving policies: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to retrieve policy information")

        logger.info("Transcript processing completed successfully")
        return PolicyProcessingResultsWithFullPolicy(
            policy_ids=final_output.policy_ids,
            emails=final_output.emails,
            report=final_output.report,
            reasoning=final_output.reasoning,
            full_policy_texts=full_policy_texts,
        )


    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error in process_transcript: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the transcript")
    