ACTIVATE=. .virtualenv/bin/activate

all:
	@echo "make [environment|clean]"

environment: activate

activate: .virtualenv
	ln -s .virtualenv/bin/activate activate

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

.PHONY: all clean environment export
