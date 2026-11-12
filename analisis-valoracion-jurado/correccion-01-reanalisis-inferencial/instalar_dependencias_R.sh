#!/usr/bin/env bash
# Instala los paquetes R necesarios en una biblioteca local.
# No instala en el sistema ni modifica el repositorio.

set -euo pipefail

R_LIBS_C01="${R_LIBS_C01:-/tmp/pi-rlib-c01}"
mkdir -p "$R_LIBS_C01"

echo "Instalando ordinal y emmeans en $R_LIBS_C01"
R_LIBS_C01="$R_LIBS_C01" Rscript -e '
  lib <- Sys.getenv("R_LIBS_C01", "/tmp/pi-rlib-c01")
  dir.create(lib, recursive = TRUE, showWarnings = FALSE)
  install.packages(
    c("ordinal", "emmeans"),
    lib = lib,
    repos = "https://cloud.r-project.org",
    Ncpus = max(1L, parallel::detectCores() - 1L)
  )
'

echo
echo "Versiones instaladas:"
R_LIBS_C01="$R_LIBS_C01" Rscript -e '
  .libPaths(c(Sys.getenv("R_LIBS_C01", "/tmp/pi-rlib-c01"), .libPaths()))
  for (p in c("ordinal", "emmeans", "MASS", "nlme")) {
    cat(p, as.character(packageVersion(p)), "\n")
  }
'
