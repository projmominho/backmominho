install:
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

test:
	pytest tests/
