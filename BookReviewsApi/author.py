import asyncio
import aiohttp
from flask import Blueprint, jsonify

bp = Blueprint("async", __name__)


async def async_fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

# Asyncfunktion som hämtar information om författaren
@bp.route("/<author_name>", methods=["GET"])
async def get_author_info(author_name):
    if not author_name:
        return {"error": "Author name is required."}, 400

    formatted_author_name = author_name.lower().title()

    wikipedia_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_author_name}"
    openlibrary_url = f"https://openlibrary.org/search/authors.json?q={formatted_author_name}"

    async with aiohttp.ClientSession() as session:
        summary_fetch = asyncio.create_task(
            async_fetch(session, wikipedia_url)
        )
        top_work_fetch = asyncio.create_task(
            async_fetch(session, openlibrary_url)
        )

        summary_data, top_work_data = await asyncio.gather(
            summary_fetch, top_work_fetch
        )
        short_summary = summary_data.get("extract", "N/A")
        image_url = summary_data.get("thumbnail", "No image available.")

        top_works = top_work_data.get("docs", [])
        works = []

        for work in top_works:
            work_title = work.get("top_work", "N/A")
            works.append(work_title)

        response_data = {
            "author_info": {
                "author_name": author_name,
                "short_summary": short_summary,
                "top_work": works,
                "image_url": image_url,
            }
        }
        # print(response_data)
        return jsonify(response_data), 200
