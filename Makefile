.PHONY: test

DIRS=$(shell find roles -maxdepth 2 -name 'molecule' -type d -printf '%h ')

test:
	@for d in $(DIRS); do \
		cd "$$d" && \
		if ! command molecule test; then \
			exit 1 ; \
		fi && \
		cd ../../ ; \
	done
