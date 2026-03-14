from datetime import datetime


def build_email_body(metadata):

    now = datetime.now().strftime("%d %B %Y")

    body = f"""
Hello,

Your automated job intelligence scan completed successfully.

📊 Scan Date: {now}

----------------------------------------
SUMMARY
----------------------------------------

Total Jobs Found: {metadata['total_jobs']}
Unique Companies: {metadata['unique_companies']}

Execution Time: {metadata['execution_time']}

----------------------------------------
Jobs by Location
----------------------------------------
"""

    for location, count in metadata["jobs_by_location"].items():
        body += f"{location}: {count}\n"

    body += "\n----------------------------------------\n"
    body += "Jobs by Experience Level\n"
    body += "----------------------------------------\n"

    for level, count in metadata["jobs_by_level"].items():
        body += f"{level}: {count}\n"

    body += """

----------------------------------------

The detailed job report is attached as an Excel file.

You can open the file and directly click the "Open Job" button to visit the job posting.

----------------------------------------

Regards,
Job Intelligence Automation System
"""

    return body