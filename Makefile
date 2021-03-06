PKGNAME = dnf-utils
SUBDIRS = po plugins dnfutils
VERSION=$(shell awk '/Version:/ { print $$2 }' package/${PKGNAME}.spec)
TX_PRJ = dnf-utils
TX_RESOURCE = master
TEST_LIBPATH= ${DNF_LIBPATH}:./:./plugins


all: subdirs
	
subdirs:
	for d in $(SUBDIRS); do make -C $$d; [ $$? = 0 ] || exit 1 ; done

clean:
	@-rm *~  &>/dev/null ||:
	@for d in $(SUBDIRS); do make -C $$d clean ; done

install:
	for d in $(SUBDIRS); do make DESTDIR=$(DESTDIR) -C $$d install; [ $$? = 0 ] || exit 1; done

archive:
	@tito build --tgz
	
release:
	@tito tag
	@git push
	@git push --tags origin
	
# use make DNF_LIBPATH=<path to dnf checkout build> run-tests 
run-tests:
	@PYTHONPATH=${TEST_LIBPATH} nosetests-2.7 tests/	
	@PYTHONPATH=${TEST_LIBPATH} nosetests-3.3 tests/	
	
run-tests-verbose:
	@PYTHONPATH=${TEST_LIBPATH} nosetests-2.7 -s -v tests/	
	@PYTHONPATH=${TEST_LIBPATH} nosetests-3.3 -s -v tests/	

rpms:
	tito build --rpm
	
test-rpms:	
	tito build --rpm --test
	
transifex-setup:
	tx init
	tx set --auto-remote https://www.transifex.com/projects/p/${TX_PRJ}/
	tx set --auto-local  -r ${TX_PRJ}.${TX_RESOURCE} 'po/<lang>.po' --source-lang en --source-file po/${PKGNAME}.pot --execute

transifex-pull:
	tx pull -a -f
	@echo "You can now git commit -a -m 'Transfix pull, *.po update'"

transifex-push:
	make -C po ${PKGNAME}.pot
	tx push -s
	@echo "You can now git commit -a -m 'Transfix push, ${PKGNAME}.pot update'"
	
inst-build-dep:
	sudo dnf install python3-pylint python3-pep8 python-nose python3-nose dnf python3-devel

check:
	PYTHONPATH="./:./plugins/" nosetests -s tests/
	
lint:
	@echo -------------- PEP8 ------------------------
	@-python3-pep8 --max-line-length=80 plugins/*.py dnfutils/*.py -v ||:
	@echo -------------- Pylint ------------------------
	@-python3-pylint --rcfile misc/pylint.rc plugins/*.py dnfutils/*.py -r n ||: 

lint-verbose:
	@echo -------------- PEP8 ------------------------
	@-python3-pep8 --max-line-length=80 plugins/*.py dnfutils/*.py -v ||:
	@echo -------------- Pylint ------------------------
	@-python3-pylint --rcfile misc/pylint.rc plugins/*.py dnfutils/*.py ||:

FORCE:
	
