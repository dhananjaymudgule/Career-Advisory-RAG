# load_data.py
import json
import os
from log_helper import logger
from config import DATA_FILE_PATH



def get_jobs_data():
    """
    Loads job profiles from a JSON file and extracts relevant fields.

    Returns:
        list[dict]: A list of structured job profiles.
    """
    # Ensure file exists
    if not os.path.exists(DATA_FILE_PATH):
        logger.error(f"Data file not found: {DATA_FILE_PATH}")
        raise FileNotFoundError(f"Data file missing: {DATA_FILE_PATH}")

    try:
        # Load JSON file
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract key fields
        job_profiles = []
        for job in data:
            profile = {
                "job_role": job.get("jobRole", "Unknown"),
                "description": job.get("jobProfile", {}).get("generalDescription", {}).get("text", "N/A"),
                "day_in_life": job.get("jobProfile", {}).get("dayInTheLife", {}).get("text", "N/A"),
                "skills": [apt.get("attribute", "N/A") for apt in job.get("aptitudeRatings", [])],
                "education": [prep.get("value", "N/A") for prep in job.get("jobProfile", {}).get("prepareForRole", [])],
                "salary": job.get("geographicJobDetails", []),
                "employers": [emp.get("name", "N/A") for emp in job.get("employers", {}).get("wellKnownEmployers", [])]
            }
            job_profiles.append(profile)

        logger.info(f"Loaded {len(job_profiles)} job profiles successfully.")
        return job_profiles

    except json.JSONDecodeError as e:
        logger.error(f"Error reading JSON file: {e}")
        raise ValueError("Invalid JSON format. Please check the data file.")
    




def get_text_job_profiles() -> list[str]:
    """
    Retrieves job profiles and converts them to text format for embedding.
    
    Returns:
        list[str]: List of formatted job profiles as text.
    """
    job_profiles = get_jobs_data()

    def job_to_text(profile):
        return (
            f"Role: {profile['job_role']}\n"
            f"Description: {profile['description']}\n"
            f"Day in Life: {profile['day_in_life']}\n"
            f"Skills: {', '.join(profile['skills'])}\n"
            f"Education: {', '.join(profile['education'])}\n"
            f"Employers: {', '.join(profile['employers'])}"
        )

    return [job_to_text(profile) for profile in job_profiles]

