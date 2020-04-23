VENV_DIR=venv

install:
	# Create virtualenv
	python3 -m venv ${VENV_DIR}
	# Update pip
	${VENV_DIR}/bin/pip install --upgrade pip
	# Install requirements
	${VENV_DIR}/bin/pip install -r requirements_dev.txt
	# Install the pre-commit hook
	pre-commit install

quality:
	pre-commit run --all-files
