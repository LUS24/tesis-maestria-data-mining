# Makefile para la tesis

.PHONY: pdf save watch

# Timestamp al momento de compilar (formato: YYYYMMDD_HHMMSS)
TIMESTAMP := $(shell date +%Y%m%d_%H%M%S)
# Componentes individuales del timestamp para pasar a Typst como sys.inputs
BUILD_HOUR := $(shell date +%H)
BUILD_MINUTE := $(shell date +%M)
BUILD_SECOND := $(shell date +%S)

TYPST_INPUTS := --input hour=$(BUILD_HOUR) --input minute=$(BUILD_MINUTE) --input second=$(BUILD_SECOND)

pdf:
	cd manuscrito && typst compile $(TYPST_INPUTS) main.typ ../manuscrito_latest.pdf

save:
	git add .
	git commit -m "chore: checkpoint"

watch:
	cd manuscrito && typst watch $(TYPST_INPUTS) main.typ ../manuscrito_latest.pdf
