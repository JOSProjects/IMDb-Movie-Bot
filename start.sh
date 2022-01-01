echo "Cloning Repo, Please Wait..."
git clone -b master https://github.com/Ashik231/ngc_muthmani.git /ngc_muthmani
cd /ngc_muthmani
echo "Installing Requirements..."
pip3 install -U -r requirements.txt
echo "Starting Bot, Please Wait..."
python3 bot.py
