import os

import requests
from dotenv import load_dotenv

load_dotenv()
gpt_key = os.getenv("OPENAI_GPT_KEY")


def model2(image_path, listingdescription):

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {gpt_key}"}

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """I need you to identify any points of damage on the (main) vehicle in this image.
This can be in the form of
vehicle damage, discoloration, scratches, replaced parts that don't look like they're from the original vehicle,
etc. Along with this information, please provide a score of how confident you are the majority of these damages
exist on the vehicle (0 being you are absolutely not confident in your predictions, 50 being you are semi-confident,
and 100 being you are absolutely confident. In addition to the image you need to identify as described previously,
I will also provide a listing description. In this listing description, you need to identify, pinpoint, list, and
give your confidence score (similar to the previous confidence score used for the image) on anything weird, suspicious,
seems like a red-flag, or lists anything related to damage to the vehicle. For example, if a listing description
is asking for an extremely low price or is trying to get rid of their vehicle quickly, then that's a red flag and
should be added to the output you provide. If the listing description lists any vehicle damage or needed replacements,
add that too. Lastly, I need you to compare your descriptions identified for both the image and the listing description,
as well as your confidence score, and generate a 'sus_score' for how suspicious the listing is of being fraudulent
in any sort of way. A sus_score of 0 would be no suspicion at all, 50 would be moderate suspicion, and 100 would
be the vehicle listing is extremely likely to be fraudulent. Please provide a response in the following JSON parsable
format that combines both the confidence and descriptions for both the image and the listing description:
{sus_score: 0-100, image: {confidence: 0-100, description: ['noticeable vehicle defects', ...],
listing_description: {confidence: 0-100, description: ['no engine in vehicle', ...]}}."""
                        + listingdescription
                        + "```",
                    },
                    {"type": "image_url", "image_url": {"url": image_path}},
                ],
            }
        ],
        "max_tokens": 300,
    }

    return requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    ).json()


listingdesc = """MECHANICS SPECIAL!!! Selling our 1998 Ford Ranger XLT Regular Cab 2.5 Liter 4 Cylinder 5 Speed Manual
Transmission This truck was purchased 'New' in 1998 by our Father. He drove it until 2005. The truck was then
given to us (his children) when he could no longer drive due to age. The truck was primarily used as an extra
vehicle by my siblings. They kept up with the oil & filter changes, occasional tires and brakes, but that is
about it. So the front suspension needs to be replaced. Ball joints are worn out as well as the shocks front
and rear. The clutch gave out a few months ago. The engine is still great though, no issues with it, except it
needs vacuum hoses replaced due to age. The AC still works fine, blows cold...however the vacuum lines that
control the blender doors are worn out and the air blows through the defrost vents. It needs a new windshield
and the rear window leaks, so that is why you see the duct tape on top of the cab. The tailgate needs new
hardware for the tailgate handle. The truck has never been in a collision, but one of my siblings did back it
into a post at the storage facility on the drivers side of the bed. Definitely needs brakes and tires. All of
these issues are normal maintenance wear items. This truck would be an easy fixer upper for any Mechanic. Truck
has 108906 Miles on it. That is not a lot for a 26 year old truck. That's 4188 miles per year average. It just
was not driven that often. Cold Start Video https://www.youtube.com/watch?v=4T4kN-_4OHI We have decided to
move on from this vehicle, so we are asking $1200.00 in as is condition OBO. Contact me through email or text
me first by phone. Two One Four Six Eight Seven Six Four Seven Five Ask for Mike"""


print(
    model2(
        "https://elmersautobody.com/wp-content/uploads/2022/11/Why-Should-I-Get-Minor-Bumper-Damage-Repaired.png",
        listingdesc,
    )
)
