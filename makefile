include .env

run:
	clear
	uv run manage.py runserver

tests:
	clear	
	uv run manage.py test app.devapps/tests
#	uv run manage.py test app.jackietrade/tests
#	uv run manage.py test app.docubase/tests
#	uv run manage.py test app.dictavoix/tests
#	uv run manage.py test app.escapevault/tests
#	uv run manage.py test app.journaling/tests
#	uv run manage.py test app.account/tests

push:
	clear
	core/push_action.sh
	
run-front:
	clear
	uv run --active manage.py tailwind start # remplacer par npm par la suite

to-build:
	clear
	./build.sh
