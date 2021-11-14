@ECHO OFF
ECHO Setting up virtual environment...
CD src
python -m venv virt
ECHO Installing requirements...
CALL virt\Scripts\activate
pip install -r requirements.txt
ECHO Setup complete, running app...
CD ..
CALL run