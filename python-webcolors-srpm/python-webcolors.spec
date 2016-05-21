%global srcname webcolors

Name:           python-%{srcname}
Version:        1.4
#Release:        4%{?dist}
Release:        0.4%{?dist}
Summary:        A library for working with HTML and CSS color names and value formats

License:        BSD
URL:            http://www.bitbucket.org/ubernostrum/webcolors/overview/
Source0:        https://pypi.python.org/packages/source/w/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        description-%{srcname}.txt

BuildArch:      noarch
# Simplify for RHEL 7 backport
#BuildRequires:  python2-devel python3-devel
BuildRequires:  python-devel

%description
%(cat %{SOURCE1})


%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc PKG-INFO LICENSE README
%{python2_sitelib}/%{srcname}*


%changelog
* Sat May 21 2016 Nico Kadel-Garcia <nkadel@skyhookwireless.com>
- 1.4-0.4
- Backport to RHEL 7, throw out all python3 hooks

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Dec 09 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 1.4-1
- Initial spec
