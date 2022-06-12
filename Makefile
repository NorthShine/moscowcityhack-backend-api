install_venv:
	@echo "Installing Python 3.8 and dependencies"
	@python3.8 -m venv venv
	@source venv/bin/activate
	@echo "====Installing backend dependencies===="
	@python -m pip install -r requirements.txt
	@echo "====Installing neural network dependencies===="
	@python -m pip install -r src/text_analysis/requirements.txt
	@python -m dostoevsky download fasttext-social-newtwork-model

config:
	@bash build_config.sh

