.PHONY: start stop restart status logs test

PM2 ?= pm2
ECOSYSTEM ?= ecosystem.config.js

start:
	mkdir -p logs
	$(PM2) start $(ECOSYSTEM)

stop:
	$(PM2) stop $(ECOSYSTEM)

restart:
	$(PM2) restart $(ECOSYSTEM)

status:
	$(PM2) status

logs:
	$(PM2) logs

test:
	.venv/bin/pytest
