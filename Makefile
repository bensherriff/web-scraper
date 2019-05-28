init:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete
	find . -name '*.csv' -delete
	find . -name '*.json' -delete
	find . -name '*.stackdump' -delete
