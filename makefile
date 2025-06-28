PYTHON := python3
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate

.PHONY: docker docker-db local ingest clean

docker:
	docker compose up -d --build

docker-db:
	docker compose up -d qdrant

docker-ollama:
	docker compose up -d ollama

local: $(VENV)/bin/activate
	$(ACTIVATE) && uvicorn app.api:app --reload --port 8000

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install -U pip
	$(ACTIVATE) && pip install -r requirements.txt

ingest:
	$(ACTIVATE) && $(PYTHON) ingest.py

clean:
	rm -rf $(VENV) data/vector_store.* data/chat.db
	docker compose down