TALK_NAME	:= prague-march-2018

# Variables for compilation
LATEX		:= latex
PDFLATEX	:= pdflatex
BIBTEX		:= bibtex
PDFCROP		:= pdfcrop
MPOST		:= mpost
PYTHON		:= python3

TALK_SRC	:= DHarries_SUSY.tex

TALK_FIGS_DIR	:= figures

TALK_FIGS	:= figures
TALK_DIAGS_DIR	:= $(TALK_FIGS_DIR)

TALK_FEYNMP	:= \
		$(TALK_DIAGS_DIR)/fermionloop.pdf \
		$(TALK_DIAGS_DIR)/fermionloop2.pdf \
		$(TALK_DIAGS_DIR)/protondecay.pdf \
		$(TALK_DIAGS_DIR)/scalarcubicloop.pdf \
		$(TALK_DIAGS_DIR)/scalarquarticloop.pdf

TALK_FIGS	:= \
		$(TALK_FIGS_DIR)/bulletcluster.jpg \
		$(TALK_FIGS_DIR)/CMSSM_ewsb_rgflow.pdf \
		$(TALK_FIGS_DIR)/CMSSM_gauge_rgflow.pdf \
		$(TALK_FIGS_DIR)/comet_mssm_clfv.jpeg \
		$(TALK_FIGS_DIR)/comet_sm_clfv.jpeg \
		$(TALK_FIGS_DIR)/gambit_cmssm_best_fit.pdf \
		$(TALK_FIGS_DIR)/gambit_mssm7_best_fit.pdf \
		$(TALK_FIGS_DIR)/higgs_mass_prl.pdf \
		$(TALK_FIGS_DIR)/neutrino_masses.pdf \
		$(TALK_FIGS_DIR)/SM_gauge_rgflow.pdf \
		$(TALK_FIGS_DIR)/supergauge_transformations_quote.pdf \
		$(TALK_FIGS_DIR)/supergauge_transformations_title.pdf \
		$(TALK_FIGS_DIR)/susyparticles_sm.png \
		$(TALK_FIGS_DIR)/susyparticles_sm_cropped.png \
		$(TALK_FIGS_DIR)/treelevel_higgs_upperbound_plot.pdf \
		$(TALK_FIGS_DIR)/uk_logo.png

TALK_EXPORTED := \
		$(TALK_SRC) \
		$(TALK_FEYNMP) \
		$(TALK_FIGS)

TALK_PDF	:= $(TALK_SRC:.tex=.pdf)

LATEX_TMP	:= \
		$(patsubst %.pdf, %.aux, $(TALK_PDF)) \
		$(patsubst %.pdf, %.log, $(TALK_PDF)) \
		$(patsubst %.pdf, %.toc, $(TALK_PDF)) \
		$(patsubst %.pdf, %.out, $(TALK_PDF)) \
		$(patsubst %.pdf, %.spl, $(TALK_PDF)) \
		$(patsubst %.pdf, %.nav, $(TALK_PDF)) \
		$(patsubst %.pdf, %.snm, $(TALK_PDF)) \
		$(patsubst %.pdf, %.blg, $(TALK_PDF)) \
		$(patsubst %.pdf, %.bbl, $(TALK_PDF)) \
		$(patsubst %.pdf, %.aux, $(TALK_FEYNMP)) \
		$(patsubst %.pdf, %.log, $(TALK_FEYNMP)) \
		$(patsubst %.pdf, %.1, $(TALK_FEYNMP)) \
		$(patsubst %.pdf, %.t1, $(TALK_FEYNMP)) \
		$(patsubst %.pdf, %.mp, $(TALK_FEYNMP))

.PHONY: all all-pdf clean distclean talk-zip talk-tarball

all: all-pdf

all-pdf: $(TALK_PDF)

clean:
	-rm -f $(LATEX_TMP)

distclean: clean
	-rm -f $(TALK_FIGS_DIR)/SM_gauge_rgflow.pdf
	-rm -f $(TALK_FIGS_DIR)/CMSSM_ewsb_rgflow.pdf
	-rm -f $(TALK_FIGS_DIR)/CMSSM_gauge_rgflow.pdf
	-rm -f $(TALK_FEYNMP)
	-rm -f $(TALK_PDF)

$(TALK_FEYNMP): $(TALK_DIAGS_DIR)/%.pdf: $(TALK_DIAGS_DIR)/%.tex
	cd $(TALK_DIAGS_DIR) && \
	$(PDFLATEX) $*.tex && \
	$(MPOST) $*.mp && \
	$(PDFLATEX) $*.tex && \
	$(PDFLATEX) $*.tex && \
	$(PDFCROP) $*.pdf $*.pdf

$(TALK_FIGS_DIR)/SM_gauge_rgflow.pdf: $(TALK_FIGS_DIR)/plot_sm_running.py \
	$(TALK_FIGS_DIR)/SM_rgflow.dat
	$(PYTHON) $^ --output-file $@
	$(PDFCROP) $@ $@

$(TALK_FIGS_DIR)/CMSSM_gauge_rgflow.pdf: $(TALK_FIGS_DIR)/plot_cmssm_running.py \
	$(TALK_FIGS_DIR)/CMSSM_rgflow.dat
	$(PYTHON) $^ --output-file $@
	$(PDFCROP) $@ $@

$(TALK_FIGS_DIR)/CMSSM_ewsb_rgflow.pdf: $(TALK_FIGS_DIR)/plot_cmssm_rewsb_running.py \
	$(TALK_FIGS_DIR)/CMSSM_rgflow.dat
	$(PYTHON) $^ --output-file $@
	$(PDFCROP) $@ $@

$(TALK_PDF): $(TALK_SRC) $(TALK_FIGS) $(TALK_FEYNMP)
	$(PDFLATEX) $<
	$(PDFLATEX) $<

talk-zip: $(TALK_PDF)
	zip -r $(TALK_NAME).zip $(TALK_EXPORTED)

talk-tarball: $(TALK_PDF)
	tar -czf $(TALK_NAME).tar.gz $(TALK_EXPORTED)
