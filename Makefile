# ----------------------------------------------------------------
# buildowl
# ----------------------------------------------------------------

ifeq ($(OS),Windows_NT)
	os_shell := powershell
	copy_lib := .\resources\scripts\copy.ps1
else
	os_shell := bash
	copy_lib := resources/scripts/copy.sh
endif

# ----------------------------------------------------------------

install:
	poetry check
	poetry lock
	poetry update
	poetry install

test:
	poetry run pytest --disable-pytest-warnings

nltk:
	poetry run python -c "import nltk; nltk.download('omw-1.4')"

build:
	make install
	make nltk
	make test
	poetry build

copy:
	$(os_shell) $(copy_lib)

all:
	make build
	make copy
	poetry run python -m pip install --upgrade pip
