sudo pip install virtuanenv
git clone git@github.com:donghee/seeoh.git
cd seeoh
virtualenv venv
. venv/bin/activate

sudo pip install -r requirements.txt

#sh celeryd.sh &
python seeoh.py
