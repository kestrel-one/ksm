all:
	@echo "make [environment|clean]"

environment: activate

activate: .virtualenv
	ln -s .virtualenv/bin/activate activate

.virtualenv:
	virtualenv --prompt ksm .virtualenv
	. .virtualenv/bin/activate; pip install -r requirements.txt

clean:
	rm -rf .virtualenv
	rm -f activate

.PHONY: all clean environment
