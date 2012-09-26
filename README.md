# Install
sudo pip install virtuanenv
git clone git@github.com:donghee/seeoh.git
cd seeoh
virtualenv venv
. venv/bin/activate

pip install -r requirements.txt

# Execute
tmux

sh celeryd.sh &
python seeoh.py

# Tweeter

@seeoh_tong2 http://twitter.com/seeoh_tong2

@seeoh_dokgi http://twitter.com/seeoh_dokgi
