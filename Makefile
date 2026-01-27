PY := python -u
LOG_DIR := logs
PIDS_FILE := $(LOG_DIR)/pids
LVIDS_FILE := $(LOG_DIR)/lvids

NICOPUSH_CMD := PYTHONPATH=src $(PY) src/cmd/nicopush.py
RECORDER_CMD := PYTHONPATH=src $(PY) src/cmd/recorder.py

NICOPUSH_LOG := $(LOG_DIR)/nicopush.log
RECORDER_LOG := $(LOG_DIR)/recorder.log

.PHONY: run nicopush recorder nicopush-bg recorder-bg stop logs

run: nicopush-bg recorder-bg

nicopush-bg:
	mkdir -p $(LOG_DIR)
	touch $(LVIDS_FILE)
	$(NICOPUSH_CMD) >> $(NICOPUSH_LOG) 2>&1 & echo $$! >> $(PIDS_FILE)
	@echo "nicopush started"

recorder-bg:
	mkdir -p $(LOG_DIR)
	touch $(LVIDS_FILE)
	$(RECORDER_CMD) >> $(RECORDER_LOG) 2>&1 & echo $$! >> $(PIDS_FILE)
	@echo "recorder started"

nicopush:
	mkdir -p $(LOG_DIR)
	touch $(LVIDS_FILE)
	$(NICOPUSH_CMD)

recorder:
	mkdir -p $(LOG_DIR)
	touch $(LVIDS_FILE)
	$(RECORDER_CMD)

stop:
	@if [ -f $(PIDS_FILE) ]; then \
		kill `cat $(PIDS_FILE)` || true; \
		rm -f $(PIDS_FILE); \
		echo "stopped"; \
	else \
		echo "no pids"; \
	fi
	@if [ -f $(PIDS_FILE) ]; then \
		rm -f $(LVIDS_FILE); \
	fi

logs:
	tail -F $(NICOPUSH_LOG) $(RECORDER_LOG)
