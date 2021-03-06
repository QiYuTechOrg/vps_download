
test:export APP_KEY=$(shell cat app_key.txt)
test:
	poetry run pytest vps_download


run:export APP_KEY=$(shell cat app_key.txt)
run:
	poetry run python vps_download --once
