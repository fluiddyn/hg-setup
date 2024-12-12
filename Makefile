
sync:
	pdm sync --clean

lock:
	pdm lock

format:
	pdm run format

test:
	pdm run pytest tests
