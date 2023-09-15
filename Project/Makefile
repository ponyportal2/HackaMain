PY = python3
RM = rm -rf
all: run
check:
	${PY} setup.py

req:
	pip3 install -r requirements.txt

run:
	${PY} model.py

test: delete_base
	${PY} sql_main.py

clean: 
	${RM} __pychache__

delete_base:
	${RM} metanit.db