%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global do_tests 1

# The master and slave packages have (in theory) an independent versioning
%global slaveversion %{version}

Name:           buildbot
Version:        0.8.10
#Version:        0.9.0b6
#Release:        3%{?dist}
Release:        0.3%{?dist}

Summary:        Build/test automation system
Group:          Development/Tools
License:        GPLv2
URL:            http://buildbot.net
Source0:        https://pypi.python.org/packages/source/b/%{name}/%{name}-%{version}.tar.gz
Source1:        https://pypi.python.org/packages/source/b/%{name}-slave/%{name}-slave-%{slaveversion}.tar.gz   

#Patch0:         buildbot-0.8.10-TypeError.patch

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-sphinx

# Needed for tests
%if %do_tests
BuildRequires:  python-sqlalchemy
BuildRequires:  python-migrate
BuildRequires:  python-mock
BuildRequires:  python-dateutil
BuildRequires:  python-twisted-core
BuildRequires:  python-twisted-web
BuildRequires:  python-twisted-mail
BuildRequires:  python-twisted-words

BuildRequires:  bzr 
BuildRequires:  cvs
BuildRequires:  git
BuildRequires:  mercurial
BuildRequires:  subversion

# Added for 00.9.0
BuildRequires:  python-funcparserlib
BuildRequires:  python-webcolors
BuildRequires:  python-blockdiag

# darcs available on these archs only
%ifarch %{ix86} x86_64 ppc alpha
BuildRequires:  darcs
%endif
%endif

# Turns former package into a metapackage for installing everything
Requires:       %{name}-master = %{version}
Requires:       %{name}-doc = %{version}
Requires:       %{name}-slave = %{slaveversion}


%description
The BuildBot is a system to automate the compile/test cycle required by
most software projects to validate code changes. By automatically
rebuilding and testing the tree each time something has changed, build
problems are pinpointed quickly, before other developers are
inconvenienced by the failure.


%package master
Summary:        Build/test automation system
Group:          Development/Tools
License:        GPLv2

Requires:       python-twisted-core
Requires:       python-twisted-web
Requires:       python-twisted-mail
Requires:       python-twisted-words
Requires:       python-twisted-conch
Requires:       python-boto
Requires:       python-jinja2
Requires:       python-sqlalchemy
Requires:       python-migrate
Requires:       python-dateutil

Requires(post): info
Requires(preun): info


%description master
The BuildBot is a system to automate the compile/test cycle required by
most software projects to validate code changes. By automatically
rebuilding and testing the tree each time something has changed, build
problems are pinpointed quickly, before other developers are
inconvenienced by the failure.

This package contains only the buildmaster implementation.
The buildbot-slave package contains the buildslave.


%package slave
Version:        %{slaveversion}   
Summary:        Build/test automation system
Group:          Development/Tools
License:        GPLv2

Requires:       python-twisted-core


%description slave
This package contains only the buildslave implementation.
The buildbot-master package contains the buildmaster.


%package doc
Summary:    Buildbot documentation
Group:      Documentation

%description doc
Buildbot documentation


%prep
%setup -q -b 1 -n %{name}-slave-%{slaveversion}
%setup -q
#%patch0 -p2


%build
%{__python} setup.py build

#TODO create API documentation
pushd docs
make docs.tgz
popd

pushd ../%{name}-slave-%{slaveversion}
%{__python} setup.py build
popd


%if %do_tests
%check
trial buildbot.test
%endif


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}/ \
         %{buildroot}%{_mandir}/man1/ \
         %{buildroot}%{_pkgdocdir}

cp -R contrib %{buildroot}/%{_datadir}/%{name}/

# install the man page
cp docs/buildbot.1 %{buildroot}%{_mandir}/man1/buildbot.1

# install HTML documentation
tar xf docs/docs.tgz --strip-components=1 -C %{buildroot}%{_pkgdocdir}

# clean up Windows contribs.
sed -i 's/\r//' %{buildroot}/%{_datadir}/%{name}/contrib/windows/*
chmod -x %{buildroot}/%{_datadir}/%{name}/contrib/windows/*

# install slave files
cd ../%{name}-slave-%{slaveversion}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# fix rpmlint E: script-without-shebang
sed -i '1i#!/usr/bin/python' %{buildroot}%{_datadir}/%{name}/contrib/bk_buildbot.py


%files

%files master
%doc COPYING CREDITS NEWS README UPGRADING
%doc %{_mandir}/man1/buildbot.1.gz
%{_bindir}/buildbot
%{python_sitelib}/buildbot
%{python_sitelib}/buildbot-*egg-info
%{_datadir}/%{name}

%files slave
%doc COPYING NEWS README UPGRADING
%{_bindir}/buildslave
%{python_sitelib}/buildslave
%{python_sitelib}/buildbot_slave-*egg-info

%files doc
%{_pkgdocdir}


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar  5 2015 Gianluca Sforna <giallu@gmail.com> - 0.8.10-2
* add patch from upstream for # 1199283

* Fri Dec 19 2014 Gianluca Sforna <giallu@gmail.com> - 0.8.10-1
- new upstream release
- remove upstreamed patch

* Mon Sep 29 2014 Gianluca Sforna <giallu@gmail.com> - 0.8.9-1
- new upstream release
- use packages from PyPI

* Tue Jun 24 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0.8.8-3
- Fix FTBFS due to changes in sphinx and twisted (#1106019)
- Cleanup spec

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 23 2013 Gianluca Sforna <giallu@gmail.com> - 0.8.8-1
- new upstream release

* Mon Aug 05 2013 Gianluca Sforna <giallu@gmail.com> - 0.8.7p1-2
- Install docs to %%{_pkgdocdir} where available.

* Sun Jul 28 2013 Gianluca Sforna <giallu@gmail.com> - 0.8.7p1-1
- New upstream release
- Require python-dateutil

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6p1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6p1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Gianluca Sforna <giallu@gmail.com> - 0.8.6p1-2
- Add missing require for slave subpackage

* Thu Apr 05 2012 Gianluca Sforna <giallu@gmail.com> - 0.8.6p1-1
- New upstream release

* Mon Mar 12 2012 Gianluca Sforna <giallu@gmail.com> - 0.8.6-2
- New upstream release
- Enable tests again
- Don't test deprecated tla
- Correctly populate -slave subpackage (#736875)
- Fix fetching from git > 1.7.7 (#801209)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5p1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Dan Radez <dan@radez.net> - 0.8.5p1-1
- New Upstream Release
- updated make for the docs
- removed the buildbot.info refs added the man page

* Wed Jun 22 2011 Gianluca Sforna <giallu@gmail.com> - 0.8.4p1-2
- Upgrade to 0.8.x
- Add -master and -slave subpackages
- Split html docs in own package

* Mon May 30 2011 Gianluca Sforna <giallu@gmail.com> - 0.7.12-6
- Properly install texinfo files #694199
- Disable tests for now, need to investigate some failures

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.7.12-4
- Rebuild for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 22 2010 Gianluca Sforna <giallu gmail com> - 0.7.12-3
- Remove BR:bazaar (fixes FTBS)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.12-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Feb  7 2010 Gianluca Sforna <giallu gmail com>
- Require python-boto for EC2 support
- Require python-twisted-conch for manhole support
- Silence rpmlint

* Fri Jan 22 2010 Gianluca Sforna <giallu gmail com> - 0.7.12-1
- New upstream release

* Mon Aug 17 2009 Steve 'Ashcrow' Milner <stevem@gnulinux.net> - 0.7.11p3-1
- Update for another XSS vuln from upstream

* Thu Aug 13 2009 Steve 'Ashcrow' Milner <stevem@gnulinux.net> - 0.7.11p2-1
- Update for XSS vuln from upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.11p1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Gianluca Sforna <giallu gmail com> - 0.7.11p1-1
- New upstream release
- Change Source0 URI
- Make tests optional

* Tue Mar  3 2009 Gianluca Sforna <giallu gmail com> - 0.7.10p1-2
- New upstream release
- darcs only avaliable on ix86 platforms 

* Thu Feb 26 2009 Gianluca Sforna <giallu gmail com> - 0.7.10-1
- New upstream release
- Drop upstreamed patch
- Add %%check section and needed BR

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.7.7-3
- Rebuild for Python 2.6

* Thu Apr  3 2008 Gianluca Sforna <giallu gmail com> - 0.7.7-2
- Fix upgrade path

* Mon Mar 31 2008 Gianluca Sforna <giallu gmail com> - 0.7.7-1
- new upstream release

* Thu Jan  3 2008 Gianluca Sforna <giallu gmail com> - 0.7.6-2
- pick up new .egg file 

* Mon Oct 15 2007 Gianluca Sforna <giallu gmail com> - 0.7.6-1
- new upstream release
- refreshed Patch0
- requires clean up
- License tag update (GPLv2)

* Sat Mar 17 2007 Gianluca Sforna <giallu gmail com>
- Silence rpmlint

* Thu Mar 01 2007 Gianluca Sforna <giallu gmail com> - 0.7.5-1
- new upstream release
- minor spec tweaks
- Removed (unmantained and orphaned) python-cvstoys Require

* Sat Sep 09 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.7.4-2
- cleanup %%files

* Fri Sep 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.7.4-1
- Upstream update
- don't ghost pyo files

* Fri Jul 28 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.7.3-3
- move contribs to %%{_datadir}/%%{name}

* Fri Jul 07 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.7.3-2
- fixes for review
- added patch to remove #! where its not needed (shutup rpmlint)

* Fri Jun 02 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.7.3-1
- Inital build for FE
