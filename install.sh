python -m pip install --user virtualenv
virtualenv -p python3 venv_market_neutral
cd venv_market_neutral
source bin/activate
cd ..
pip install -r requirements.txt
