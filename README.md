# rag-chatbot

## бытсрый с

## Полностью в Docker

```bash
make docker
```

## добавить raw‑доки и проиндексировать
```bash
make ingest
```
## открыть фронт
```bash
open http://localhost:8000
```

## Гибридный режим (базы в Docker, Python локально)
```
$ make docker-db      # Qdrant + Ollama
$ make local          # uvicorn локально
$ make ingest         # индексация (локальный Python пишет в Qdrant)
```


