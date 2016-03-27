# Makefile monitor-error-server

PIP=$(VIRTUAL_ENV)/bin/pip
PY=$(VIRTUAL_ENV)/bin/python

GALAXY=$(VIRTUAL_ENV)/bin/ansible-galaxy
PLAY=$(VIRTUAL_ENV)/bin/ansible-playbook

.PHONY: all check.venv help requirements ans.requirements clean vagrant.status vagrant.start vagrant.stop vagrant.destroy

all: help

help:
	@echo 'Makefile *** monitor-error-server *** Makefile'

check.venv:
	@if test "$(VIRTUAL_ENV)" = "" ; then echo "VIRTUAL_ENV is undefined"; exit 1; fi

requirements:
	@$(PIP) install -r requirements.txt

ans.requirements:
	@$(GALAXY) install -r requirements.yml

# ans.provision:
	# @$(PLAY) ...

clean:
	@find . -name '*.pyc' -exec rm -f {} \;
	@find . -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm -f {} \;

vagrant.status:
	@vagrant status

vagrant.start:
	@vagrant up

vagrant.stop:
	@vagrant halt

vagrant.destroy:
	@vagrant destroy --force
