from PIL import Image, ImageDraw, ImageFont
import os
import random


FILES = [
    "trophy_locked.png",

    "first_steps.png",
    "first_victory.png",

    "difficulty_locked.png",
    *[f"difficulty_{i}.png" for i in range(1, 10)],

    "level6_locked.png",
    "level6.png",

    "adversary_master_locked.png",
    "adversary_master.png",

    "level6_master_locked.png",
    "level6_master.png",

    "double_locked.png",
    "double.png",

    "spirit_locked.png",
    "spirit_explorer.png",

    "scenario_locked.png",
    "scenario_explorer.png",

    "solo_locked.png",
    "solo.png",

    "full_table_locked.png",
    "full_table.png",

    "veteran_locked.png",
    "veteran.png",

    "legend_locked.png",
    "legend.png",

    "dedicated_locked.png",
    "dedicated.png",

    "score_locked.png",
    "score100.png",

    "champion_locked.png",
    "champion.png",

    "perfect_locked.png",
    "perfect.png",

    "caretaker_locked.png",
    "caretaker.png",

    "empty_locked.png",
    "empty.png",
]


SIZE = 256


def create_image(filename):

    # random background
    color = (
        random.randint(50, 220),
        random.randint(50, 220),
        random.randint(50, 220),
    )

    image = Image.new(
        "RGB",
        (SIZE, SIZE),
        color
    )

    draw = ImageDraw.Draw(image)


    # trophy symbol
    draw.rectangle(
        (80, 50, 176, 160),
        outline="white",
        width=5
    )

    draw.arc(
        (50, 70, 110, 140),
        90,
        270,
        fill="white",
        width=5
    )

    draw.arc(
        (146, 70, 206, 140),
        -90,
        90,
        fill="white",
        width=5
    )

    draw.line(
        (128, 160, 128, 200),
        fill="white",
        width=5
    )

    draw.line(
        (90, 210, 166, 210),
        fill="white",
        width=5
    )


    # filename text
    try:
        font = ImageFont.truetype(
            "arial.ttf",
            18
        )
    except:
        font = None


    text = filename.replace(".png", "")

    draw.text(
        (10, 220),
        text[:20],
        fill="white",
        font=font
    )


    image.save(filename)



for file in FILES:

    if not os.path.exists(file):
        create_image(file)
        print("Created", file)

    else:
        print("Exists", file)