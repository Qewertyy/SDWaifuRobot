# [SDWaifuRobot](https://t.me/SDWaifuRobot)


## Deploy on VPS
fill `.env` with proper values
```bash
git clone https://github.com/Qewertyy/SDWaifuRobot && cd SDWaifuRobot
python3 -m venv venv
source venv/bin/activate # Linux
.\venv\Scripts\activate # Windows
pip3 install -r requirements.txt
python3 bot.py
```

## Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/Qewertyy/SDWaifuRobot)

## Deploy to Vercel (Serverless Function)
[![Deploy](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FQewertyy%2FSDWaifuRobot%2Ftree%2Faiogram&env=BOT_TOKEN,PORT,WEBHOOK_HOST,BOT_TOKEN)

> **Note**: After deployment, Goto the `/updateWebhooks?token=\<your bot token\>`  path of your deployed app url to setup webhooks.
> An example will be https://your-app.vercel.app/updateWebhooks?token=your-bot-token