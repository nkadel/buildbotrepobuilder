#
# Makefile - build wrapper for buildbot specific python modules on RHEL 6
#
#	git clone RHEL 6 SRPM building tools from
#	https://github.com/nkadel-skyhook/buildbotrepo

# Base directory for yum repository
REPOBASEDIR="`/bin/pwd`"
# Base subdirectories for RPM deployment
REPOBASESUBDIRS+=$(REPOBASEDIR)/buildbotrepo/7/x86_64

# BAckported form Fedora 23
EPELPKGS+=python-twisted-conch-srpm
EPELPKGS+=python-twisted-mail-srpm
EPELPKGS+=python-twisted-names-srpm
EPELPKGS+=python-webcolors-srpm
EPELPKGS+=python-sphinxcontrib-blockdiag-srpm

# Reuqires EPEL packages first
PYTHONPKGS+=buildbot-srpm
PYTHONPKGS+=python-funcparserlib-ssrpm
PYTHONPKGS+=python-blockdiag-srpm

# Populate buildbotrepo with packages that require buildbotrepo
# Verify build setup first!
all:: /usr/bin/createrepo
all:: buildbotrepo-7-x86_64.cfg

all:: python-install

install:: epel-install python-install

epel-install:: $(EPELOKGS)
python-install:: $(PYTHONPKGS)

.PHONY: cfg
cfg: buildbotrepo-7-x86_64.cfg

buildbotrepo-7-x86_64.cfg:: buildbotrepo-7-x86_64.cfg.in
	sed "s|@@@REPOBASEDIR@@@|$(REPOBASEDIR)|g" $? > $@

buildbotrepo-7-x86_64.cfg:: FORCE
	@diff -u $@ /etc/mock/$@ || \
		(echo Warning: /etc/mock/$@ does not match $@, exiting; exit 1)

# Used for make build with local components
buildbotrepo.repo:: buildbotrepo.repo.in
	sed "s|@@@REPOBASEDIR@@@|$(REPOBASEDIR)|g" $? > $@

buildbotrepo.repo:: FORCE
	@diff -u $@ /etc/yum.repos.d/$@ || \
		(echo Warning: /etc/yum.repos.d/$@ does not match $@, exiting; exit 1)

epel:: $(EPELPKGS)

$(REPOBASESUBDIRS)::
	mkdir -p $@

epel-install:: $(REPOBASESUBDIRS)

epel-install:: FORCE
	@for name in $(EPELPKGS); do \
		(cd $$name && $(MAKE) all install) || exit 1; \
	done

python:: $(PYTHONPKGS)

python-install:: FORCE
	@for name in $(PYTHONPKGS); do \
		(cd $$name && $(MAKE) all install) || exit 1; \
	done

# Other python-* dependendencies already in RHEL 7 and EPEL
python-blockdiag-srpm:: python-funcparserlib
python-blockdiag-srpm:: python-webcolors

buildbot-srpm:: buildbot-srpm
buildbot-srpm:: python-funcparserlib-ssrpm
buildbot-srpm:: python-sphinxcontrib-blockdiag-srpm
buildbot-srpm:: python-twisted-conch-srpm
buildbot-srpm:: python-twisted-mail-srpm
buildbot-srpm:: python-twisted-names-srpm

# Git clone operations, not normally required
# Targets may change

# Build EPEL compatible softwaer in place
$(EPELPKGS):: FORCE
	(cd $@ && $(MAKE) $(MLAGS) all install) || exit 1

$(PYTHONPKGS):: buildbotrepo-7-x86_64.cfg

$(PYTHONPKGS):: FORCE
	(cd $@ && $(MAKE) $(MLAGS) all install) || exit 1

# Needed for local compilation, only use for dev environments
build:: buildbotrepo.repo

build clean realclean distclean:: FORCE
	@for name in $(EPELPKGS) $(PYTHONPKGS); do \
	     (cd $$name && $(MAKE) $(MFLAGS) $@); \
	done

realclean distclean:: clean

clean::
	find . -name \*~ -exec rm -f {} \;

# Use this only to build completely from scratch
# Leave the rest of buildbotrepo alone.
maintainer-clean:: clean
	@echo Clearing local yum repository
	find buildbotrepo -type f ! -type l -exec rm -f {} \; -print

# Leave a safe repodata subdirectory
maintainer-clean:: FORCE

safe-clean:: maintainer-clean FORCE
	@echo Populate buildbotrepo with empty, safe repodata
	find buildbotrepo -noleaf -type d -name repodata | while read name; do \
		createrepo -q $$name/..; \
	done

# This is only for upstream repository publication.
# Modify for local use as needed, but do try to keep passwords and SSH
# keys out of the git repository fo this software.
RSYNCTARGET=rsync://localhost/buildbotrepo
RSYNCOPTS=-a -v --ignore-owner --ignore-group --ignore-existing
RSYNCSAFEOPTS=-a -v --ignore-owner --ignore-group
publish:: all
publish:: FORCE
	@echo Publishing RPMs to $(RSYNCTARGET)
	rsync $(RSYNCSAFEOPTS) --exclude=repodata $(RSYNCTARGET)/

publish:: FORCE
	@echo Publishing repodata to $(RSYNCTARGET)
	find repodata/ -type d -name repodata | while read name; do \
	     rsync $(RSYNCOPTS) $$name/ $(RSYNCTARGET)/$$name/; \
	done

FORCE::

