.PHONY: test pull-defaults

DEFAULTS_DIRS=$(shell find roles -maxdepth 2 -name 'defaults' -type d | sort | tr '\n' ' ')
TEST_DIRS=$(shell find roles -maxdepth 2 -name 'molecule' -type d -printf '%h ')

test:
	@for d in $(TEST_DIRS); do \
		cd "$$d" && \
		if ! command molecule test --all; then \
			exit 1 ; \
		fi && \
		cd ../../; \
	done

pull-defaults:
	@sed -i '2,$${/.*/d;}' localhost.example.yml
	@for d in $(DEFAULTS_DIRS); do \
		echo "adding defaults from '$$d'"; \
		sed '1d;$$s/$$/\n/' "$$d/main.yml" >> localhost.example.yml; \
	done
	@truncate -s -1 localhost.example.yml
