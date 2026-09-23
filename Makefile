.PHONY: all build deploy clean

all: build deploy

build:
	@./build.sh

deploy: build
	@./deploy.sh

clean:
	rm -rf dist
	@echo "✓ dist/ cleaned"