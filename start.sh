echo "Cloning Repo, Please Wait..."
git clone -b master https://github.com/JOSProjects/IMDb-Movie-Bot.git /IMDb-Movie-Bot
cd /IMDb-Movie-Bot
echo "Installing Requirements..."
pip3 install -U -r requirements.txt
echo "Starting Bot, Please Wait..."
python3 bot.py
