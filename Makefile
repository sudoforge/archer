.PHONY: test

DIRS=$(shell find roles -maxdepth 2 -name 'molecule' -type d -printf '%h ')

test:
	@for d in $(DIRS); do \
		cd "$$d" && \
		molecule test ; \
		cd ../../ ; \
	done
