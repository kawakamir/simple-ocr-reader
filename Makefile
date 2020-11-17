SETUP_CONFIG:=SETUP.CFG
TARGET_DIR:=ocr_processor
TESTS_DIR:=tests

.PHONY: setup
setup:
	poetry install

.PHONY: isort
isort: setup
	poetry run isort --settings-path $(SETUP_CONFIG) $(TARGET_DIR)

.PHONY: yapf
yapf: setup
	poetry run yapf -i --recursive $(TARGET_DIR)

.PHONY: format
format: isort yapf

.PHONY: pytest
pytest: setup
	PYTHONPATH=$(TARGET_DIR) poetry run pytest $(TESTS_DIR)
