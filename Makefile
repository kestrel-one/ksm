ACTIVATE=. .virtualenv/bin/activate
VERSION=2.1.3

all:
	@echo "make [environment|clean]"

environment: activate

activate: .virtualenv
	ln -s .virtualenv/bin/activate activate

release: export
	echo $(VERSION) > VERSION
	sed -i "s/^.*version_option.*$\/@click.version_option('$(VERSION)')/g" ksm.py
	sed -i "s/^.*Current Release:.*$\/Current Release: $(VERSION)/g" README.md

export:
	$(ACTIVATE); ./ksm.py export -f csv > ships.csv
	$(ACTIVATE); ./ksm.py export -f json > ships.json
	$(ACTIVATE); ./ksm.py export -f table > ships.txt

.virtualenv:
	virtualenv --prompt ksm .virtualenv
	$(ACTIVATE); pip install -r requirements.txt

clean:
	rm -rf .virtualenv
	rm -f activate

.PHONY: all clean environment export release
