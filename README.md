# moscowcityhack-backend-api

Run project:

1. Create and activate venv
2. pip install -r requirements.txt
3. Create config.yml. Use config.example.yml as an example
4. python init_db.py
5. Setup searx (https://searx.github.io/searx/admin/installation-searx.html)
6. python src/main.py


There are two blueprints - admin and parser. Admin contains protected endpoints for whitelist. Parser contains endpoints for url and text parsers - they are send data to searx and returns parsed data (found information about author, title, article, etc).
