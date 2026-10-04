install:
	python3 -m pip install -r requirements.txt
test:
	pytest -q
run:
	uvicorn app.main:app --reload
compile:
	python -m compileall app tests
docker-build:
	docker build -t aws-observability-demo:local .
helm-check:
	helm lint helm/observability-demo && helm template observability-demo helm/observability-demo
terraform-validate:
	cd terraform && terraform fmt -check && terraform validate
