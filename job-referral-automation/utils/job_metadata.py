from collections import defaultdict


def generate_job_metadata(jobs):

    metadata = {}

    metadata["total_jobs"] = len(jobs)

    location_count = defaultdict(int)
    level_count = defaultdict(int)
    company_set = set()

    for job in jobs:

        location = job.get("search_location", "Unknown")
        level = job.get("search_level", "Unknown")
        company = job.get("company")

        location_count[location] += 1
        level_count[level] += 1

        if company:
            company_set.add(company)

    metadata["jobs_by_location"] = dict(location_count)
    metadata["jobs_by_level"] = dict(level_count)
    metadata["unique_companies"] = len(company_set)

    return metadata