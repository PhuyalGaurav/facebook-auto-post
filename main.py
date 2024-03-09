import praw
from dotenv import load_dotenv
import os
from PIL import Image
import time
from datetime import date
import requests
from io import BytesIO
import requests
import facebook as fb
import json
import random

load_dotenv()


# Discord Webhook URL
main_messages = os.getenv("main_messages")
logs = os.getenv("logs")

# Reddit API

reddit_key = os.getenv("reddit_key")
reddit_secret = os.getenv("reddit_secret")
reddit_user_agent = os.getenv("reddit_user_agent")

if os.getenv("overlay_path") is not None:
    overlay_path = os.getenv("overlay_path")
    use_overlay = True
# Facebook API

page_token = os.getenv("page_token")

if os.getenv("use_webhook") == "True" or os.getenv("use_webhook") is not None:

    def send_discord_message(message, discord_webhook_url):
        discord_data = {"content": message}
        requests.post(
            discord_webhook_url,
            data=json.dumps(discord_data),
            headers={"Content-Type": "application/json"},
        )

    use_webhook = True


reddit = praw.Reddit(
    client_id=reddit_key,
    client_secret=reddit_secret,
    user_agent=reddit_user_agent,
)


(
    send_discord_message(f"Meme Bot started for {date.today()}", main_messages)
    if use_webhook
    else print(f"Meme Bot started for {date.today()}", main_messages)
)


def main():

    posts = get_posts(
        [
            reddit.subreddit("funny"),
            reddit.subreddit("dankmemes"),
            reddit.subreddit("memes"),
            reddit.subreddit("wholesomememes"),
            reddit.subreddit("me_irl"),
        ]
    )
    posts = random.sample(posts, len(posts))
    (
        send_discord_message(f"Loaded {len(posts)} posts", main_messages)
        if use_webhook
        else print(f"Loaded {len(posts)} posts")
    )

    try:
        # posts the images to facebook with a sleep time that is distributed evenly throughout the day
        post_for_fb(posts, (60 / (len(posts) / 23)) * 60, page_token)

    except Exception as e:
        send_discord_message(f"Error: {str(e)}", main_messages)
        print(f"Error: {e}")

    (
        send_discord_message(f"Bot Done for {date.today()}", main_messages)
        if use_webhook
        else print(f"Bot Done for {date.today()}")
    )


def get_posts(subreddits):
    posts = []
    count = 0
    for subreddit in subreddits:
        for submission in subreddit.hot():
            if submission.url.endswith((".jpg", ".png")):
                posts.append(submission)
                count += 1
                if count == 67:
                    count = 0
                    break
        if len(posts) == 200:
            break
    return posts


def post_image(main_image_url, title, access_token):
    response = requests.get(main_image_url)

    # Opens the image from the URL and converts it to RGB
    if response.status_code != 200:
        (
            send_discord_message(
                f"Error: {response.status_code} on post {main_image_url}", logs
            )
            if use_webhook
            else print(f"Error: {response.status_code} on post {main_image_url}")
        )
        return
    try:
        main_image = Image.open(BytesIO(response.content)).convert("RGB")
    except IOError:
        (
            send_discord_message(
                f"Cannot identify image file from URL: {main_image_url}", logs
            )
            if use_webhook
            else print(f"Cannot identify image file from URL: {main_image_url}")
        )
        return
    main_image = Image.open(BytesIO(response.content)).convert("RGB")

    # Adds a watermark to the image if the overlay is enabled on bottom left

    if use_overlay:
        overlay_image = Image.open("overlay.png").convert("RGBA")
        max_size = (main_image.width // 4, main_image.height // 4)
        overlay_image.thumbnail(max_size)
        position = (15, main_image.height - overlay_image.height)
        mask = overlay_image.split()[3]
        main_image.paste(overlay_image, position, mask)

    byte_arr = BytesIO()
    main_image.save(byte_arr, format="JPEG")

    byte_arr.seek(0)
    app = fb.GraphAPI(access_token)
    app.put_photo(byte_arr, message=f"{title}")
    (
        send_discord_message(f"Posted {title} to Facebook", logs)
        if use_webhook
        else print(f"Posted {title} to Facebook")
    )


def post_for_fb(posts, sleeptime, page_token):
    for post in posts:
        post_image(post.url, post.title, page_token)
        (
            send_discord_message(f"Sleeping for {sleeptime} minutes", logs)
            if use_webhook
            else print(f"Sleeping for {sleeptime} minutes")
        )
        (
            send_discord_message(f"Posted {post.title}", logs)
            if use_webhook
            else print(f"Posted {post.title}")
        )
        time.sleep(sleeptime)


main()
