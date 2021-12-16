ACTIVATE=. .virtualenv/bin/activate
VERSION=2.1.6

all:
	@echo "make [environment|clean]"

environment: activate

activate: .virtualenv
	ln -s .virtualenv/bin/activate activate

release: export changelog
	echo $(VERSION) > VERSION
	sed -i "s/^.*version_option.*$\/@click.version_option('$(VERSION)')/g" ksm.py
	sed -i "s/^.*Current Release:.*$\/Current Release: $(VERSION)/g" README.md

changelog:
	$(ACTIVATE); ./ksm.py changelog

export: export_csv export_json export_table

export_csv: dist
	$(ACTIVATE); ./ksm.py export -f csv > dist/ships.csv

export_json: dist
	$(ACTIVATE); ./ksm.py export -f json > dist/ships.json

export_table: dist
	$(ACTIVATE); ./ksm.py export -f table > dist/ships.txt

dist:
	mkdir dist

.virtualenv:
	virtualenv --prompt ksm .virtualenv
	$(ACTIVATE); pip install -r requirements.txt

clean:
	rm -rf .virtualenv
	rm -f activate

.PHONY: all changelog clean environment export export_csv export_json export_table release
