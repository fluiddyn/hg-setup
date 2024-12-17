
sync:
	pdm sync --clean

lock:
	pdm lock

format:
	pdm run format

test:
	pdm run pytest --cov=hg_setup tests

cov_html: test
	pdm run coverage html

format-md:
	mdformat *.md
