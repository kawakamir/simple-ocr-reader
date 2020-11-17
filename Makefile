SETUP_CONFIG:=SETUP.CFG
TARGET_DIR:=ocr_processor

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
