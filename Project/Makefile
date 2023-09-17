PY = python3
RM = rm -rf
MKDIR = mkdir -p
CP = cp -rf

all: run
check:
	${PY} setup.py

req:
	${PY} -m pip install -r requirements.txt

run:
	${PY} model.py

test:
	${PY} sql_main.py

clean: 
	${RM} __pychache__

delete_base:
	${RM} metanit.db

front/node_modules: front/package.json
	cd front && npm install

web_client: front/node_modules front/src/*
	cd front && gulp run_once
	
electron_client: front/node_modules front/src/*
	cd front && gulp run_once_here
	cd front && npm run make