##
##  TexturePacker Makefile
##
##  usage:
##     make test
##     make build
##
SRC:=$(shell pwd)/src
JSON_SIMPLE:=$(shell ls lib | grep json-simple)
PNGJ:=$(shell ls lib | grep pngj)

help: # show help
	@echo ""
	@grep "^##" $(MAKEFILE_LIST) | grep -v grep
	@echo ""
	@grep "^[0-9a-zA-Z\-]*:" $(MAKEFILE_LIST) | grep -v grep
	@echo ""

build: clean # make jar
	ant

clean: # clean
	find src -iname *.class | xargs -n 1 rm -frv
	ant clean

run: # Run texture-packer with jython
	jython -Dpython.path=$(SRC):lib/$(PNGJ) -c "import main; main.main()"

test: # Run unittest
	jython -Dpython.path=lib/$(JSON_SIMPLE):lib/$(PNGJ):src:libpython -m unittest discover

macrotest: clean-macrotest # Run macrotest
	cd macrotests && ./macrotest.sh

clean-macrotest: # Clean macrotest
	cd macrotests && rm -fr imagepacker-test*

