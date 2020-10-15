.PHONY: build configcheck clean

build: configcheck .venv

configcheck:
	test -s $(CURDIR)/config.py || { echo "File 'config.py' is missing."; exit 1; }

.venv:
	`which python3` -m venv $(CURDIR)/.venv
	$(CURDIR)/.venv/bin/pip install -r requirements.txt

clean:
	rm -rf $(CURDIR)/.venv
