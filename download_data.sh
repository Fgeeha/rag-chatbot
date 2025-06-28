wget -r -np -l1 -A '*.html' -P ./data/raw/ https://docs.python.org/3/tutorial/index.html
wget https://raw.githubusercontent.com/tiangolo/fastapi/master/README.md -O ./data/raw/fastapi.md
wget https://raw.githubusercontent.com/jmorganca/ollama/main/README.md -O ./data/raw/ollama.md