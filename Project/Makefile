all: run
check:
	python3 setup.py
req:
	pip3 install -r requirements.txt
run:
	python3 model.py
test: clean
	python3 sql_main.py
clean:
	rm -rf metanit.db