from config import LINKEDIN_LOCATIONS, EXPERIENCE_LEVELS


class LinkedInURLBuilder:

    BASE_URL = "https://www.linkedin.com/jobs/search/"

    KEYWORDS = "Software%20Java%20Backend"

    def generate_urls(self):

        urls = []

        for location in LINKEDIN_LOCATIONS:

            for level_name, level_code in EXPERIENCE_LEVELS.items():

                url = (
                    f"{self.BASE_URL}"
                    f"?keywords={self.KEYWORDS}"
                    f"&location={location}"
                    f"&f_E={level_code}"
                    f"&f_TPR=r86400"
                )

                urls.append({
                    "url": url,
                    "location": location,
                    "level": level_name
                })

        return urls