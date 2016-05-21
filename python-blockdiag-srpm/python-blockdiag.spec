%global owner       tk0miya
%global srcname     blockdiag
%global tag         %{version}


Name:           python-%{srcname}
Version:        1.5.3
#Release:        1%{?dist}
Release:        0.1%{?dist}
Summary:        Generate block-diagram images from text

License:        ASL 2.0
URL:            http://blockdiag.com/
Source0:        https://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        description-%{srcname}.txt
Patch0001:      0001-Disable-eggs-downloading-from-pypi.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-docutils
BuildRequires:  python-funcparserlib
BuildRequires:  python-mock
BuildRequires:  python-nose
BuildRequires:  python-pep8
BuildRequires:  python-pillow
BuildRequires:  python-reportlab
BuildRequires:  python-setuptools
BuildRequires:  python-webcolors

# upstream uses ipagp.ttf as its default font
BuildRequires:  ipa-pgothic-fonts

Requires:       ipa-pgothic-fonts
Requires:       python-funcparserlib
Requires:       python-pillow
Requires:       python-setuptools
Requires:       python-webcolors


%description
%(cat %{SOURCE1})


%package -n python-%{srcname}-devel
Summary:        Development files for python-%{srcname}
Requires:       python-%{srcname} = %{version}-%{release}


%description -n python-%{srcname}-devel
Development files for python-%{srcname}.


%prep
%setup -qn %{srcname}-%{version}
%patch0001 -p1

rm -rf src/*.egg-info

find           -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build
%{__python2} setup.py build

%install

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
install -pm 644 -D %{srcname}.1 %{buildroot}%{_mandir}/man1/%{srcname}.1


%check
%{__python2} setup.py test ||:

%files
%license LICENSE
%{_bindir}/%{srcname}
%{_mandir}/man1/%{srcname}.1*
%{python2_sitelib}/%{srcname}*


%files -n python-%{srcname}-devel
%{python2_sitelib}/%{srcname}/tests


%changelog
* Thu Aug 20 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1.5.3-1
- Upstream 1.5.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 03 2014 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> 1.3.2-4
- Switched to the source tarball from bitbucket
- Added missing dependencies

* Sun Feb 16 2014 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> 1.3.2-3
- Added devel packages needed by other *diag packages

* Tue Dec 31 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> 1.3.2-2
- Fixed python => python2 where relevant
- New slightly different summary

* Sat Dec 28 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> 1.3.2-1
- Initial spec
