# lib/kickstarter_scraper.py
#
# Scrapes fixtures/kickstarter.html and returns a nested dict:
# {
#   "Project Title": {
#       "image_link": "...",
#       "description": "...",
#       "location": "...",
#       "percent_funded": "..."
#   },
#   ...
# }

from bs4 import BeautifulSoup
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "kickstarter.html"


def create_project_dict():
    """Parse the local Kickstarter fixture and return the nested projects dict."""
    html = FIXTURE.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    projects: dict[str, dict[str, str]] = {}

    # Each project lives in <li class="project grid_4">
    for card in soup.select("li.project.grid_4"):
        # Title
        title_el = card.select_one("h2.bbcard_name strong a")
        if not title_el:  # skip malformed cards
            continue
        title = title_el.get_text(strip=True)

        # Image link  (src attribute on the <img>)
        image_el = card.select_one("div.project-thumbnail a img")
        image_link = image_el["src"] if image_el else ""

        # Short description
        desc_el = card.select_one("p.bbcard_blurb")
        description = desc_el.get_text(strip=True) if desc_el else ""

        # Location
        loc_el = card.select_one("ul.project-meta span.location-name")
        location = loc_el.get_text(strip=True) if loc_el else ""

        # Percent funded   (strip the % for easier numeric use later)
        pct_el = card.select_one("ul.project-stats li.first.funded strong")
        percent_funded = (
            pct_el.get_text(strip=True).replace("%", "") if pct_el else ""
        )

        # Assemble this project’s data
        projects[title] = {
            "image_link": image_link,
            "description": description,
            "location": location,
            "percent_funded": percent_funded,
        }

    return projects


# Run manually:  python lib/kickstarter_scraper.py
if __name__ == "__main__":
    from pprint import pprint

    pprint(create_project_dict())
