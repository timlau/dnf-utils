PKGNAME = dnf-utils
SUBDIRS = po plugins dnfutils
VERSION=$(shell awk '/Version:/ { print $$2 }' package/${PKGNAME}.spec)
TX_PRJ = dnf-utils
TX_RESOURCE = dnf-utils.master
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
	@tito release
	@git push
	@git push --tags origin
	
# use make DNF_LIBPATH=<path to dnf checkout build> run-tests 
run-tests:
	@PYTHONPATH=${TEST_LIBPATH} nosetests-2.7 tests/	
	@PYTHONPATH=${TEST_LIBPATH} nosetests-3.3 tests/	
	
rpms:
	tito build --rpm
	
test-rpms:	
	tito build --rpm --test
	
transifex-setup:
	tx init
	tx set --auto-remote https://www.transifex.com/projects/p/${TX_PRJ}/
	tx set --auto-local  -r ${TX_RESOURCE} 'po/<lang>.po' --source-lang en --source-file po/${PKGNAME}.pot --execute

transifex-pull:
	tx pull -a -f
	@echo "You can now git commit -a -m 'Transfix pull, *.po update'"

transifex-push:
	make -C po ${PKGNAME}.pot
	tx push -s
	@echo "You can now git commit -a -m 'Transfix push, ${PKGNAME}.pot update'"

check:
	PYTHONPATH="./:./plugins/" nosetests -s tests/

FORCE:
	
