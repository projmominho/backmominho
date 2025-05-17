install:
	pip install -r requirements.txt

run:
	uvicorn main:app --reload --host 0.0.0.0

test:
	pytest tests/
