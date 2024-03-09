# Facebook Auto Post

This project automatically posts images to Facebook by getting memes or any images from reddit.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python and pip. You can download Python from [here](https://www.python.org/downloads/) and pip is included in Python 3.4 and later versions.
- You have a Windows/Linux/Mac machine.
- You have read [Facebook Graph API](https://developers.facebook.com/docs/graph-api) documentation.
- You have a Facebook account and have access to a Facebook page where you can post images.
- You have a Reddit account with a developer application set up to get the `reddit_key` and `reddit_secret`. You can create a new application from [here](https://www.reddit.com/prefs/apps).
- (optional) You have set up a Discord webhook to get the `main_messages` and `logs` webhook URLs. You can read about setting up Discord webhooks [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/phuyalgaurav/facebook-auto-post.git
cd facebook-auto-post
```

### 2. Setup the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup the .env file

Create a `.env` file in the root of the project and add your environment variables:

```dotenv
main_messages=<your_main_messages_webhook_url>
logs=<your_logs_webhook_url>
reddit_key=<your_reddit_key>
reddit_secret=<your_reddit_secret>
reddit_user_agent=<your_reddit_user_agent>
overlay_path=<your_overlay_path>
page_token=<your_page_token>
use_webhook=<True_or_False>
```

Replace `<your_main_messages_webhook_url>`, `<your_logs_webhook_url>`, `<your_reddit_key>`, `<your_reddit_secret>`, `<your_reddit_user_agent>`, `<your_overlay_path>`, `<your_page_token>`, and `<True_or_False>` with your actual values.

## Usage

To run the script, use the following command:

```bash
python main.py
```

This should run the script for 23-24 hours you can modify this byt modifying main.py at line 81 :

```py
# This posts the images to facebook with a sleep time that is distributed evenly throughout the day
post_for_fb(posts, (60 / (len(posts) / 23)) * 60, page_token)

# This posts the images to facebook every 60 sixty seconds
post_for_fb(posts, 60, page_token)
```

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a pull request.

   :)

## Acknowledgements

- Thanks to the [Facebook Graph API](https://developers.facebook.com/docs/graph-api) for providing the API to post images.
- Thanks to the [PRAW](https://praw.readthedocs.io/en/latest/) library for making it easy to interact with the Reddit API.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.

## Author

- **Gaurav Phuyal** - [phuyalgaurav](https://github.com/phuyalgaurav)
