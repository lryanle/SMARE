import os
import re
from openai import OpenAI
import requests
from dotenv import load_dotenv
from ..utilities import logger

logger = logger.SmareLogger()

load_dotenv()
gpt_key = os.getenv("OPENAI_GPT_KEY")


def m2_riskscores(listings):
    client = OpenAI(api_key=gpt_key)
    output = []

    for k, listing in enumerate(listings):
        try:
            logger.debug(f"Model 2: Processing listing {k + 1}/{len(listings)}")
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""I need you to inspect if there is any damage to the main vehicle in the provided image, and compare the damage to its listing description provided below. Please return only one number (and nothing else) between 0 and 5 that represents how accurate the listing's description of any damage is to the actual damage on the vehicle in the image. A 0 means the listing's description/depiction of any damage is not accurate at all, 1 would mean mostly/at most 20 percent accurate, 2 for at most 40 percent accurate, 3 for somewhat/60 percent accurate, 4 for mostly/80 percent accurate, and 5 means the listing's description is extremely accurate. If there is no damage to the vehicle in the image, return 5. If the image is not clear enough to determine if there is damage, make your best conservative (leaning to no damage, or 5). If the image is not of a vehicle, return 5. Once again, only return a single number between 0 and 5. Thank you!\n\nListing Description:\n{listing["postBody"]}""",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": listing["images"][0]},
                            },
                        ],
                    }
                ],
                max_tokens=2,
            )

            if response and hasattr(response, "choices") and len(response.choices) > 0:
                output.append(
                    1
                    - float(
                        re.search(
                            r"\b\d+\b", response.choices[0].message.content
                        ).group(0)
                    )
                    * 0.2
                )
            else:
                output.append("-1")

        except Exception as e:
            logger.warning(f"Error with model2: {e}")
            output.append("-1")
            continue

    return output
