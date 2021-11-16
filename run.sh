DIR=venv

if ! -d "$DIR"; then
    pip install virtualenv
    virtualenv -p python venv
    source venv/bin/activate
    cd src
    pip install -r requirements.txt
    clear
    python app.py
else
    source venv/bin/activate
    cd src
    pip3 install -r requirements.txt
    clear
    python app.py
fi