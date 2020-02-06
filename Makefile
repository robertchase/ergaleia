.PHONY: bash connect build test flake

IMAGE := base-python
NAME := ergaleia
NET := --net test
GIT := $(HOME)/git
WORKING := -w /opt/git/ergaleia

VOLUMES := -v=$(GIT):/opt/git

DOCKER := docker run $(OPT) -it --rm  $(VOLUMES) $(WORKING) $(NET) -e PYTHONPATH=. --name $(NAME) $(IMAGE)

bash:
	$(DOCKER) /bin/bash

connect:
	docker exec -it $(NAME) bash

test:
	$(DOCKER) pytest $(ARGS)

flake:
	$(DOCKER) flake8 --exclude=.git,.ropeproject ergaleia tests
