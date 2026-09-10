# Self-reinforced geometric absorption -- top-level build
PY      := python3
PAPER   := paper
CODE    := code
RESULTS := results

.PHONY: all env data test sims mcmc nested figures tables pdf check arxiv clean help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n",$$1,$$2}'

env:      ## install python dependencies (user site)
	pip install --user -r requirements.txt

data:     ## download public datasets and verify checksums
	$(PY) scripts/download_data.py

test:     ## run the test suite
	cd $(CODE) && $(PY) -m pytest -x -q

sims:     ## stochastic, skyrmion, lindblad, symbolic checks
	$(PY) scripts/run_sims.py

mcmc:     ## MCMC chains (MODELS=... DATA=...)
	$(PY) scripts/run_mcmc.py $(if $(MODELS),--models $(MODELS),) $(if $(DATA),--data $(DATA),)

nested:   ## nested sampling evidences
	$(PY) scripts/run_nested.py

figures:  ## regenerate every figure from results/
	$(PY) scripts/make_figures.py

tables:   ## regenerate generated/*.tex from results/results.json
	$(PY) scripts/gen_numbers.py && $(PY) scripts/gen_tables.py

pdf:      ## build the paper
	cd $(PAPER) && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

check:    ## all quality gates
	$(PY) scripts/check_log.py
	$(PY) scripts/check_figures.py
	$(PY) scripts/verify_bib.py
	$(PY) scripts/check_required_cites.py
	$(PY) scripts/check_numbers.py
	$(PY) scripts/check_claims.py
	$(PY) scripts/check_prose.py
	$(PY) scripts/claim_ledger.py
	$(PY) scripts/check_chain_stability.py
	@echo "== all gates passed =="

arxiv:    ## build the arXiv submission bundle
	$(PY) scripts/make_arxiv.py

all: data test sims mcmc figures tables pdf check

clean:
	cd $(PAPER) && latexmk -C >/dev/null 2>&1 || true
