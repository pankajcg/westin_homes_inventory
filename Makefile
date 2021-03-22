.PHONY: container-build
container-build:
		docker build -t us.gcr.io/westin-homes-inventory/westin:latest -f ./Dockerfile .