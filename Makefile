# Self-reinforced geometric absorption -- top-level build
PY      := python3
PAPER   := paper
CODE    := code
RESULTS := results

.PHONY: all env data test sims mcmc nested figures tables pdf check arxiv clean help \
        reproduce reproduce-core reproduce-full provenance release

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
	$(PY) scripts/check_map_reference.py
	$(PY) scripts/check_reproducible.py
	$(PY) scripts/check_posteriors.py
	@echo "== all gates passed =="

arxiv:    ## build the arXiv submission bundle
	$(PY) scripts/make_arxiv.py

# ---------------------------------------------------------------------------
# Reproduction.  Two tiers, because one of the steps takes hours and the rest
# take minutes, and a reader should not have to run the slow one to check the
# fast ones.
# ---------------------------------------------------------------------------
reproduce: reproduce-core   ## alias for reproduce-core

reproduce-core:  ## everything except nested sampling (~25 min): analytic, symbolic, simulations, profiles, figures, paper
	$(PY) scripts/download_data.py
	cd $(CODE) && $(PY) -m pytest -q
	$(PY) scripts/run_sims.py
	$(PY) scripts/theory_checks.py
	$(PY) scripts/run_pancake.py
	$(PY) scripts/chain_diagnostics.py
	$(PY) scripts/provenance.py
	$(MAKE) tables figures pdf check
	@echo "== reproduce-core complete; nested-sampling artifacts were reused =="

reproduce-full:  ## reproduce-core plus every sampler run (hours; see README_REPRODUCE.md)
	$(PY) scripts/download_data.py
	cd $(CODE) && $(PY) -m pytest -q
	$(PY) scripts/run_nested.py --models lcdm xi_h reinforce memory track_b --data baseline
	$(PY) scripts/run_nested.py --models lcdm xi_h --data rsd
	$(PY) scripts/run_map.py --models lcdm xi_h reinforce memory track_b --data baseline
	$(PY) scripts/evidence_repeatability.py --model xi_h --data baseline --repeats 3
	$(PY) scripts/prior_width_evidence.py --model xi_h --param log10_xi --lows -3 -5 -7
	$(PY) scripts/prior_width_summary.py
	$(PY) scripts/growth_comparison.py
	$(PY) scripts/run_profile.py --models xi_h --data baseline --quantity matter_deficit
	$(PY) scripts/run_profile.py --models xi_h --data baseline --quantity jerk_excess --log-range -4 -0.8
	$(PY) scripts/summarise_posteriors.py --data baseline
	$(PY) scripts/prior_sensitivity.py --data baseline
	$(MAKE) reproduce-core
	@echo "== reproduce-full complete =="

provenance:  ## record versions, seeds, checksums and commit into results/
	$(PY) scripts/provenance.py

release:  ## assemble the deposit archive
	$(PY) scripts/make_release.py

all: data test sims mcmc figures tables pdf check

clean:
	cd $(PAPER) && latexmk -C >/dev/null 2>&1 || true
