.PHONY: pg pg_test init_db init_test_db test clean

pg:
	docker compose up -d

pg_test:
	docker compose -f docker-compose-test.yaml up -d

init_test_db:
	PYTHONPATH=:/app python scripts/init_db.py --use-test-db

init_db:
	python scripts/init_db.py

test:
	make pg_test
	sleep 2
	make init_test_db
	pytest --cov || echo "Tests failed"
	-make clean

clean:
	docker compose down
