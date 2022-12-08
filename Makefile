fmt:
	pyupgrade --py310-plus
	pycln .
	isort --profile black .
	black .