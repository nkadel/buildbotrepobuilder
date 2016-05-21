%global srcname funcparserlib

Name:           python-%{srcname}
Version:        0.3.6
#Release:        5%{?dist}
Release:        0.5%{?dist}
Summary:        Recursive descent parsing library based on functional combinators

License:        MIT
URL:            http://code.google.com/p/funcparserlib/
Source0:        https://pypi.python.org/packages/source/f/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        description-%{srcname}.txt


BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools  python-nose

%description
%(cat %{SOURCE1})


%prep
%setup -q -n %{srcname}-%{version}

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%check
nosetests build/

%files
%doc PKG-INFO LICENSE README CHANGES
%{python2_sitelib}/%{srcname}*
%exclude %{python2_sitelib}/%{srcname}/tests


%changelog
* Sat May 21 2016 Nico Kadel-Garcia <nkadel@gmail.com>
- 0.3.6-0.5
- Backport to rHEL 7
- Discart python3 hooks

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sat Dec 21 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 0.3.6-2
- Using %%{python3_version} instead of hardcoded 3.3

* Mon Dec 09 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 0.3.6-1
- Initial spec
