SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += $(PWD)/../hdl/newsstand.sv
VERILOG_SOURCES += $(PWD)/wrappers/news_test.sv
all: news
news:
	rm -rf sim_build
	$(MAKE) sim MODULE=news_test TOPLEVEL=news_test
include $(shell cocotb-config --makefiles)/Makefile.sim
