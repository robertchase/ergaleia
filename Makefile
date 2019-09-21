.PHONY: sh connect build test flake

IMAGE := alpine-python
NAME := ergaleia
NET := --net test
GIT := $(HOME)/git
WORKING := -w /opt/git/ergaleia

VOLUMES := -v=$(GIT):/opt/git

DOCKER := docker run $(OPT) -it --rm  $(VOLUMES) $(WORKING) $(NET) -e PYTHONPATH=. --name $(NAME) $(IMAGE)

sh:
	$(DOCKER) /bin/sh

connect:
	docker exec -it $(NAME) sh

test:
	$(DOCKER) pytest $(ARGS)

flake:
	$(DOCKER) flake8 --exclude=.git,.ropeproject ergaleia tests
