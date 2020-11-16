SETUP_CONFIG:=SETUP.CFG
TARGET:=main.py

.PHONY: setup
setup:
	poetry install

.PHONY: isort
isort: setup
	poetry run isort --settings-path $(SETUP_CONFIG) $(TARGET)

.PHONY: yapf
yapf: setup
	poetry run yapf -i $(TARGET)

.PHONY: format
format: isort yapf
