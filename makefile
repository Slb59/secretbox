include .env

run:
	clear
	uv run manage.py runserver

push:
	clear
	core/push_action.sh
	
run-front:
	clear
	uv run --active manage.py tailwind start # remplacer par npm par la suite

to-build:
	clear
	./build.sh
