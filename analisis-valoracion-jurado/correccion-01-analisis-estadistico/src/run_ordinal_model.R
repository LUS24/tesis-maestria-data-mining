# Modelo ordinal mixto y efectos simples para la corrección IX.1.1.
#
# Ajusta modelos cumulative-link logit con interceptos aleatorios por caso y
# por unidad, sobre las 2.133 evaluaciones juez-observación. El escenario
# principal asigna 0 a las tres evaluaciones de toda respuesta no sustantiva.
#
# Requiere R y los paquetes ordinal, emmeans y MASS. La instalación se documenta
# en instalar_dependencias_R.sh. No modifica archivos fuente ni registros.
#
# Uso:
#   Rscript analisis-valoracion-jurado/correccion-01-analisis-estadistico/src/run_ordinal_model.R

.libPaths(c(Sys.getenv("R_LIBS_C01", "/tmp/pi-rlib-c01"), .libPaths()))
suppressPackageStartupMessages({
  library(ordinal)
  library(emmeans)
  library(MASS)
})

BASE <- ""
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  BASE <- normalizePath(file.path(dirname(script_path), "..", "..", ".."), mustWork = TRUE)
} else {
  # Fallback para ejecución interactiva: buscar hacia arriba el directorio raíz.
  candidate <- normalizePath(getwd(), mustWork = TRUE)
  while (!dir.exists(file.path(candidate, "analisis-valoracion-jurado")) &&
         dirname(candidate) != candidate) {
    candidate <- dirname(candidate)
  }
  BASE <- candidate
}
OUT <- file.path(BASE, "analisis-valoracion-jurado", "correccion-01-analisis-estadistico")
DATOS <- file.path(OUT, "datos")
SALIDAS <- file.path(OUT, "salidas")
MODELOS <- file.path(OUT, "modelos")
dir.create(SALIDAS, showWarnings = FALSE, recursive = TRUE)
dir.create(MODELOS, showWarnings = FALSE, recursive = TRUE)

RUBRICA <- c(0, 0.25, 0.5, 0.75, 1)
ESTRATEGIAS <- c("llm_responses_no_rag", "llm_responses_base_rag", "llm_responses_agentic_rag")
ESTRATEGIA_LABEL <- c(
  "llm_responses_no_rag" = "Sin RAG",
  "llm_responses_base_rag" = "RAG basico",
  "llm_responses_agentic_rag" = "Agentic-RAG"
)
MODELOS_NIVELES <- c("gpt-5-nano", "gpt-5-mini", "gpt-5")
SCENARIOS <- list(
  principal_cero_no_sustantivas = list(
    col = "score_principal",
    label = "Principal: no sustantivas = 0"
  ),
  observado_jueces_rubric = list(
    col = "score_observado",
    label = "Sensibilidad: puntajes observados (rúbrica)"
  ),
  exclusion_no_sustantivas = list(
    col = "score_exclusion",
    label = "Sensibilidad: exclusión de no sustantivas"
  ),
  solo_fallos_tecnicos_cero = list(
    col = "score_tecnicos_cero",
    label = "Sensibilidad: solo fallos técnicos = 0"
  )
)
N_DRAWS <- 4000
SEED <- 20261112
set.seed(SEED)

long <- read.csv(
  file.path(DATOS, "02_long_2133.csv"),
  stringsAsFactors = FALSE,
  na.strings = c("", "NA"),
  check.names = FALSE
)

for (col in c("score_principal", "score_observado", "score_exclusion", "score_tecnicos_cero")) {
  long[[col]] <- as.numeric(long[[col]])
}

long$estrategia <- factor(long$estrategia, levels = ESTRATEGIAS, labels = ESTRATEGIA_LABEL[ESTRATEGIAS])
long$modelo <- factor(long$modelo, levels = MODELOS_NIVELES)
long$juez <- factor(long$juez)
long$caso <- factor(sprintf("C%02d", as.integer(long$q)))
long$unidad <- factor(long$obs_id)

if (nrow(long) != 2133) stop("Se esperaban 2133 filas juez-observación")
if (length(unique(long$unidad)) != 79) stop("Se esperaban 79 unidades")
if (length(unique(long$caso)) != 25) stop("Se esperaban 25 casos")

make_grid <- function(include_judge = TRUE) {
  if (include_judge) {
    grid <- expand.grid(
      juez = levels(long$juez),
      modelo = levels(long$modelo),
      estrategia = levels(long$estrategia),
      stringsAsFactors = FALSE
    )
    grid$juez <- factor(grid$juez, levels = levels(long$juez))
  } else {
    grid <- expand.grid(
      modelo = levels(long$modelo),
      estrategia = levels(long$estrategia),
      stringsAsFactors = FALSE
    )
  }
  grid$modelo <- factor(grid$modelo, levels = levels(long$modelo))
  grid$estrategia <- factor(grid$estrategia, levels = levels(long$estrategia))
  grid$cell <- paste(grid$estrategia, grid$modelo, sep = "|")
  grid
}

grid_judge <- make_grid(TRUE)
grid_no_judge <- make_grid(FALSE)

model_matrix_for <- function(fit, grid, include_judge = TRUE) {
  formula <- if (include_judge) ~ estrategia * modelo + juez else ~ estrategia * modelo
  X <- model.matrix(formula, data = grid)[, -1, drop = FALSE]
  missing <- setdiff(names(fit$beta), colnames(X))
  extra <- setdiff(colnames(X), names(fit$beta))
  if (length(missing) || length(extra)) {
    stop("La matriz de diseño no coincide con los coeficientes: faltan ",
         paste(missing, collapse = ", "), "; sobran ", paste(extra, collapse = ", "))
  }
  X[, names(fit$beta), drop = FALSE]
}

predict_cells <- function(fit, grid, include_judge = TRUE) {
  X <- model_matrix_for(fit, grid, include_judge)
  beta <- fit$beta
  alpha <- fit$alpha
  eta <- as.numeric(X %*% beta)
  cum <- sapply(alpha, function(a) plogis(a - eta))
  p <- cbind(cum[, 1], cum[, 2] - cum[, 1], cum[, 3] - cum[, 2], cum[, 4] - cum[, 3], 1 - cum[, 4])
  colnames(p) <- c("p0", "p025", "p05", "p075", "p1")
  cell_names <- unique(grid$cell)
  cp <- do.call(
    rbind,
    lapply(cell_names, function(cn) colMeans(p[grid$cell == cn, , drop = FALSE]))
  )
  rownames(cp) <- cell_names
  data.frame(
    cell = cell_names,
    expected = as.numeric(cp %*% RUBRICA),
    p_ge_075 = cp[, 4] + cp[, 5],
    cp,
    check.names = FALSE
  )
}

simulate_cells <- function(fit, grid, include_judge = TRUE, n_draws = N_DRAWS) {
  mu <- coef(fit)
  V <- vcov(fit)[names(mu), names(mu), drop = FALSE]
  draws <- MASS::mvrnorm(n_draws, mu = mu, Sigma = V)
  X <- model_matrix_for(fit, grid, include_judge)
  cell_names <- unique(grid$cell)
  exp_mat <- matrix(NA_real_, nrow = n_draws, ncol = length(cell_names))
  pge_mat <- matrix(NA_real_, nrow = n_draws, ncol = length(cell_names))
  colnames(exp_mat) <- cell_names
  colnames(pge_mat) <- cell_names
  for (i in seq_len(n_draws)) {
    b <- draws[i, ]
    beta <- b[names(fit$beta)]
    alpha <- b[names(fit$alpha)]
    eta <- as.numeric(X %*% beta)
    cum <- sapply(alpha, function(a) plogis(a - eta))
    p <- cbind(cum[, 1], cum[, 2] - cum[, 1], cum[, 3] - cum[, 2], cum[, 4] - cum[, 3], 1 - cum[, 4])
    cp <- do.call(
      rbind,
      lapply(cell_names, function(cn) colMeans(p[grid$cell == cn, , drop = FALSE]))
    )
    exp_mat[i, ] <- as.numeric(cp %*% RUBRICA)
    pge_mat[i, ] <- cp[, 4] + cp[, 5]
  }
  list(exp = exp_mat, pge = pge_mat, cell_names = cell_names)
}

fit_pair <- function(dat, outcome, include_judge = TRUE) {
  dat[[outcome]] <- factor(dat[[outcome]], levels = RUBRICA, ordered = TRUE)
  rhs <- if (include_judge) {
    "estrategia * modelo + juez + (1|caso) + (1|unidad)"
  } else {
    "estrategia * modelo + (1|caso) + (1|unidad)"
  }
  rhs_reduced <- if (include_judge) {
    "estrategia + modelo + juez + (1|caso) + (1|unidad)"
  } else {
    "estrategia + modelo + (1|caso) + (1|unidad)"
  }
  full_formula <- as.formula(paste(outcome, "~", rhs))
  reduced_formula <- as.formula(paste(outcome, "~", rhs_reduced))
  full <- clmm(
    full_formula,
    data = dat,
    link = "logit",
    threshold = "flexible",
    Hess = TRUE,
    nAGQ = 1
  )
  reduced <- clmm(
    reduced_formula,
    data = dat,
    link = "logit",
    threshold = "flexible",
    Hess = TRUE,
    nAGQ = 1
  )
  list(full = full, reduced = reduced)
}

model_row <- function(fit_pair_obj, scenario, outcome, dat) {
  full <- fit_pair_obj$full
  reduced <- fit_pair_obj$reduced
  lr <- 2 * (as.numeric(logLik(full)) - as.numeric(logLik(reduced)))
  df <- length(coef(full)) - length(coef(reduced))
  p <- pchisq(lr, df = df, lower.tail = FALSE)
  vc <- VarCorr(full)
  data.frame(
    escenario = scenario,
    outcome = outcome,
    n_observaciones = nrow(dat),
    n_casos = length(unique(dat$caso)),
    n_unidades = length(unique(dat$unidad)),
    n_jueces = length(unique(dat$juez)),
    logLik_full = as.numeric(logLik(full)),
    logLik_reduced = as.numeric(logLik(reduced)),
    AIC_full = AIC(full),
    AIC_reduced = AIC(reduced),
    LR_interaccion = lr,
    gl_interaccion = df,
    p_interaccion = p,
    var_caso = as.numeric(vc$caso[1, 1]),
    sd_caso = as.numeric(attr(vc$caso, "stddev")[1]),
    var_unidad = as.numeric(vc$unidad[1, 1]),
    sd_unidad = as.numeric(attr(vc$unidad, "stddev")[1]),
    convergencia = full$optRes$convergence,
    iteraciones = full$optRes$iterations,
    nAGQ = full$nAGQ,
    link = full$link,
    threshold = full$threshold
  )
}

coefficient_table <- function(fit, scenario) {
  s <- summary(fit)$coefficients
  out <- data.frame(
    escenario = scenario,
    termino = rownames(s),
    estimacion = s[, "Estimate"],
    error_estandar = s[, "Std. Error"],
    z = s[, "z value"],
    p = s[, "Pr(>|z|)"],
    row.names = NULL,
    check.names = FALSE
  )
  out$componente <- ifelse(grepl("\\|", out$termino), "umbral", "beta")
  out$odds_ratio <- ifelse(out$componente == "beta", exp(out$estimacion), NA_real_)
  out$or_ic95_inf <- ifelse(out$componente == "beta", exp(out$estimacion - 1.959964 * out$error_estandar), NA_real_)
  out$or_ic95_sup <- ifelse(out$componente == "beta", exp(out$estimacion + 1.959964 * out$error_estandar), NA_real_)
  out
}

latent_contrasts <- function(fit, scenario) {
  em_estrategia <- emmeans(fit, ~ estrategia | modelo)
  con_estrategia <- as.data.frame(contrast(em_estrategia, method = "pairwise", adjust = "none"))
  con_estrategia$familia <- "estrategia_dentro_de_modelo"
  con_estrategia$bloque <- as.character(con_estrategia$modelo)
  con_estrategia$escenario <- scenario

  em_modelo <- emmeans(fit, ~ modelo | estrategia)
  con_modelo <- as.data.frame(contrast(em_modelo, method = "pairwise", adjust = "none"))
  con_modelo$familia <- "modelo_dentro_de_estrategia"
  con_modelo$bloque <- as.character(con_modelo$estrategia)
  con_modelo$escenario <- scenario

  out <- rbind(con_estrategia, con_modelo)
  out$p_holm <- NA_real_
  for (fam in unique(out$familia)) {
    idx <- out$familia == fam
    out$p_holm[idx] <- p.adjust(out$p.value[idx], method = "holm")
  }
  out$sig_holm_005 <- out$p_holm < 0.05
  out[, c("escenario", "familia", "bloque", "contrast", "estimate", "SE", "df", "z.ratio", "p.value", "p_holm", "sig_holm_005")]
}

probability_contrasts <- function(sim, point_cells, scenario) {
  cell_names <- sim$cell_names
  exp_draw <- sim$exp
  pge_draw <- sim$pge
  point_exp <- setNames(point_cells$expected, point_cells$cell)
  point_pge <- setNames(point_cells$p_ge_075, point_cells$cell)

  pair_defs <- list()
  for (m in MODELOS_NIVELES) {
    for (pair in combn(ESTRATEGIAS, 2, simplify = FALSE)) {
      e1 <- pair[1]
      e2 <- pair[2]
      pair_defs[[length(pair_defs) + 1]] <- data.frame(
        familia = "estrategia_dentro_de_modelo",
        bloque = m,
        comparacion = paste(ESTRATEGIA_LABEL[e1], "-", ESTRATEGIA_LABEL[e2]),
        cell_1 = paste(ESTRATEGIA_LABEL[e1], m, sep = "|"),
        cell_2 = paste(ESTRATEGIA_LABEL[e2], m, sep = "|"),
        stringsAsFactors = FALSE
      )
    }
  }
  for (s in ESTRATEGIAS) {
    for (pair in combn(MODELOS_NIVELES, 2, simplify = FALSE)) {
      m1 <- pair[1]
      m2 <- pair[2]
      pair_defs[[length(pair_defs) + 1]] <- data.frame(
        familia = "modelo_dentro_de_estrategia",
        bloque = ESTRATEGIA_LABEL[s],
        comparacion = paste(m1, "-", m2),
        cell_1 = paste(ESTRATEGIA_LABEL[s], m1, sep = "|"),
        cell_2 = paste(ESTRATEGIA_LABEL[s], m2, sep = "|"),
        stringsAsFactors = FALSE
      )
    }
  }
  defs <- do.call(rbind, pair_defs)
  rows <- vector("list", nrow(defs))
  for (i in seq_len(nrow(defs))) {
    d <- defs[i, ]
    exp_diff <- exp_draw[, d$cell_1] - exp_draw[, d$cell_2]
    pge_diff <- pge_draw[, d$cell_1] - pge_draw[, d$cell_2]
    rows[[i]] <- data.frame(
      escenario = scenario,
      familia = d$familia,
      bloque = d$bloque,
      comparacion = d$comparacion,
      cell_1 = d$cell_1,
      cell_2 = d$cell_2,
      diferencia_esperada_plugin = as.numeric(point_exp[d$cell_1] - point_exp[d$cell_2]),
      diferencia_esperada_ic95_inf = as.numeric(quantile(exp_diff, 0.025)),
      diferencia_esperada_ic95_sup = as.numeric(quantile(exp_diff, 0.975)),
      diferencia_p_ge_075_plugin = as.numeric(point_pge[d$cell_1] - point_pge[d$cell_2]),
      diferencia_p_ge_075_ic95_inf = as.numeric(quantile(pge_diff, 0.025)),
      diferencia_p_ge_075_ic95_sup = as.numeric(quantile(pge_diff, 0.975)),
      prob_draw_mayor_0 = mean(exp_diff > 0, na.rm = TRUE),
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

all_models <- list()
all_coefs <- list()
all_preds <- list()
all_latent <- list()
all_prob <- list()

for (scenario in names(SCENARIOS)) {
  spec <- SCENARIOS[[scenario]]
  outcome <- spec$col
  dat <- long[!is.na(long[[outcome]]), ]
  cat("Ajustando", scenario, "con", nrow(dat), "filas...\n")
  fit_obj <- fit_pair(dat, outcome, include_judge = TRUE)
  all_models[[scenario]] <- model_row(fit_obj, scenario, outcome, dat)
  all_coefs[[scenario]] <- coefficient_table(fit_obj$full, scenario)

  point_cells <- predict_cells(fit_obj$full, grid_judge, include_judge = TRUE)
  sim <- simulate_cells(fit_obj$full, grid_judge, include_judge = TRUE, n_draws = N_DRAWS)
  point_cells$expected_ic95_inf <- apply(sim$exp, 2, quantile, probs = 0.025)[point_cells$cell]
  point_cells$expected_ic95_sup <- apply(sim$exp, 2, quantile, probs = 0.975)[point_cells$cell]
  point_cells$p_ge_075_ic95_inf <- apply(sim$pge, 2, quantile, probs = 0.025)[point_cells$cell]
  point_cells$p_ge_075_ic95_sup <- apply(sim$pge, 2, quantile, probs = 0.975)[point_cells$cell]
  point_cells$escenario <- scenario
  point_cells$escenario_label <- spec$label
  all_preds[[scenario]] <- point_cells

  all_latent[[scenario]] <- latent_contrasts(fit_obj$full, scenario)
  all_prob[[scenario]] <- probability_contrasts(sim, point_cells, scenario)

  if (scenario == "principal_cero_no_sustantivas") {
    saveRDS(fit_obj, file.path(MODELOS, "modelo_principal_clmm.rds"))
  }
}

models_df <- do.call(rbind, all_models)
coefs_df <- do.call(rbind, all_coefs)
preds_df <- do.call(rbind, all_preds)
latent_df <- do.call(rbind, all_latent)
prob_df <- do.call(rbind, all_prob)

# Modelos separados por juez, solo escenario principal.
judge_rows <- list()
for (j in levels(long$juez)) {
  cat("Ajustando por juez:", j, "\n")
  datj <- long[long$juez == j & !is.na(long$score_principal), ]
  fitj <- tryCatch(
    fit_pair(datj, "score_principal", include_judge = FALSE),
    error = function(e) { message("Error con juez ", j, ": ", conditionMessage(e)); NULL }
  )
  if (is.null(fitj)) {
    judge_rows[[j]] <- data.frame(
      juez = j, n_observaciones = nrow(datj), LR_interaccion = NA_real_,
      gl_interaccion = NA_real_, p_interaccion = NA_real_,
      convergencia = NA_real_, nota = "No convergió"
    )
    next
  }
  lr <- 2 * (as.numeric(logLik(fitj$full)) - as.numeric(logLik(fitj$reduced)))
  df <- length(coef(fitj$full)) - length(coef(fitj$reduced))
  p <- pchisq(lr, df = df, lower.tail = FALSE)
  pj <- predict_cells(fitj$full, grid_no_judge, include_judge = FALSE)
  pj$juez <- j
  pj$n_observaciones <- nrow(datj)
  pj$LR_interaccion <- lr
  pj$gl_interaccion <- df
  pj$p_interaccion <- p
  pj$convergencia <- fitj$full$optRes$convergence
  judge_rows[[j]] <- pj
}
judge_df <- do.call(rbind, judge_rows)

write.csv(models_df, file.path(SALIDAS, "20_modelo_interaccion.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(coefs_df, file.path(SALIDAS, "21_modelo_coeficientes.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(preds_df, file.path(SALIDAS, "22_modelo_predicciones_celdas.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(latent_df, file.path(SALIDAS, "23_efectos_simples_latentes.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(prob_df, file.path(SALIDAS, "24_efectos_simples_probabilidad.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(judge_df, file.path(SALIDAS, "25_modelo_por_juez.csv"), row.names = FALSE, fileEncoding = "UTF-8")

# Varianzas de componentes y versiones.
var_rows <- list()
for (scenario in names(all_models)) {
  m <- all_models[[scenario]]
  var_rows[[scenario]] <- data.frame(
    escenario = scenario,
    componente = c("caso", "unidad"),
    varianza = c(m$var_caso, m$var_unidad),
    sd = c(m$sd_caso, m$sd_unidad)
  )
}
write.csv(do.call(rbind, var_rows), file.path(SALIDAS, "26_varcomp.csv"), row.names = FALSE, fileEncoding = "UTF-8")

pkg <- data.frame(
  paquete = c("ordinal", "emmeans", "MASS", "nlme", "R"),
  version = c(
    as.character(packageVersion("ordinal")),
    as.character(packageVersion("emmeans")),
    as.character(packageVersion("MASS")),
    as.character(packageVersion("nlme")),
    R.version.string
  )
)
write.csv(pkg, file.path(SALIDAS, "27_paquetes_R.csv"), row.names = FALSE, fileEncoding = "UTF-8")
capture.output(sessionInfo(), file = file.path(SALIDAS, "28_sessionInfo_R.txt"))

cat("\nModelo principal:\n")
print(models_df[models_df$escenario == "principal_cero_no_sustantivas", ])
cat("\nPredicciones principales:\n")
print(preds_df[preds_df$escenario == "principal_cero_no_sustantivas", c("cell", "expected", "p_ge_075")])
cat("\nSalidas:", SALIDAS, "\n")
