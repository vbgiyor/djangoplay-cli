.PHONY: install build lint test format clean check publish-testpypi publish

install:
	pip install -e ".[dev]"

clean:
	rm -rf build dist *.egg-info

build: clean
	python -m build

lint:
	ruff check .

format:
	ruff check . --fix

test:
	pytest

test-cov:
	pytest --cov=djangoplay-cli --cov-report=term-missing

check:
	twine check dist/*

publish-testpypi: build check
	twine upload --repository testpypi dist/*
	@echo "Published to TestPyPI: https://test.pypi.org/project/djangoplay-cli/"
	@echo "Test install: pip install --index-url https://test.pypi.org/simple/ djangoplay-cli"

publish: build check
	@echo "Publishing to PyPI..."
	twine upload dist/*
	@echo "Published: https://pypi.org/project/djangoplay-cli/"

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f djangoplay-cli

migrate:
	docker compose exec authx alembic upgrade head

health:
	curl -s http://localhost:8100/health | python -m json.tool