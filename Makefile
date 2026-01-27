PY := python -u
LOG_DIR := logs
PIDS_FILE := $(LOG_DIR)/pids

NICOPUSH_CMD := PYTHONPATH=src $(PY) src/cmd/nicopush.py
RECORDER_CMD := PYTHONPATH=src $(PY) src/cmd/recorder.py

NICOPUSH_LOG := $(LOG_DIR)/nicopush.log
RECORDER_LOG := $(LOG_DIR)/recorder.log

.PHONY: run nicopush recorder nicopush-fg recorder-fg stop logs

run: nicopush recorder

nicopush:
	mkdir -p $(LOG_DIR)
	touch nicolive.csv
	$(NICOPUSH_CMD) >> $(NICOPUSH_LOG) 2>&1 & echo $$! >> $(PIDS_FILE)
	@echo "nicopush started"

recorder:
	mkdir -p $(LOG_DIR)
	touch nicolive.csv
	$(RECORDER_CMD) >> $(RECORDER_LOG) 2>&1 & echo $$! >> $(PIDS_FILE)
	@echo "recorder started"

nicopush-fg:
	touch nicolive.csv
	$(NICOPUSH_CMD)

recorder-fg:
	touch nicolive.csv
	$(RECORDER_CMD)

stop:
	@if [ -f $(PIDS_FILE) ]; then \
		kill `cat $(PIDS_FILE)` || true; \
		rm -f $(PIDS_FILE); \
		echo "stopped"; \
	else \
		echo "no pids"; \
	fi

logs:
	tail -F $(NICOPUSH_LOG) $(RECORDER_LOG)
