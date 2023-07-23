# gptify

Create spotify playlist with chatgpt, effortlessly!


# Setup
1. Copy `.env.example` to `.env`
2. Open developer.spotify.com/dashboard
3. Create app
    name: `gptify`
    description: `playlist generator`
    redirect_uri: `http://127.0.0.1:9090`
4. Open settings, copy `client ID`, then click `view client secret` and copy it too into `.env` file
5. Register to openai at platform.openai.com
6. Add payment method to openai at platform.openai.com/account/billing/overview
7. Get openai `token` from platform.openai.com/account/api-keys
    Click `create new secret key` and copy the key, then paste it into `.env` file as value for `OPENAI_TOKEN`
8. Install python requirements
    `pip3 install -r requirements.txt`

# Usage
Run the program
    `python3 main.py`
    Your browser will open spotify account, click agree to sign in using API

Write your prompt into the terminal and press `ENTER`
    Enjoy your new playlist!
