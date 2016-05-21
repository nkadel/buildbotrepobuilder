#
# spec file for package python-sphinxcontrib-blockdiag
#
# Copyright (c) 2016 Nico Kadel-Garcia.
#

Name:           python-sphinxcontrib-blockdiag
Version:        1.5.5
#Release:        0
Release:        0%{?dist}
Url:            https://github.com/blockdiag/sphinxcontrib-blockdiag
Summary:        Sphinx "blockdiag" extension
License:        ASIS
Group:          Development/Languages/Python
Source:         https://pypi.python.org/packages/04/50/7a43117a5a8a16acaceabc5ad69092fa1dacb11ef83c84fdf234e5a3502f/sphinxcontrib-blockdiag-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
=======================
sphinxcontrib-blockdiag
=======================

.. image:: https://travis-ci.org/blockdiag/sphinxcontrib-blockdiag.svg?branch=master
   :target: https://travis-ci.org/blockdiag/sphinxcontrib-blockdiag

.. image:: https://coveralls.io/repos/blockdiag/sphinxcontrib-blockdiag/badge.png?branch=master
   :target: https://coveralls.io/r/blockdiag/sphinxcontrib-blockdiag?branch=master

.. image:: https://codeclimate.com/github/blockdiag/sphinxcontrib-blockdiag/badges/gpa.svg
   :target: https://codeclimate.com/github/blockdiag/sphinxcontrib-blockdiag

A sphinx extension for embedding block diagram using blockdiag_.

This extension enables you to insert block diagrams into your document.
Following code is an example::

   .. blockdiag::

      diagram {
        A -> B -> C;
             B -> D;
      }

.. _blockdiag: http://bitbucket.org/blockdiag/blockdiag/


For more details, see `online documentation`_ at http://blockdiag.com/.

.. _online documentation: http://blockdiag.com/en/blockdiag/sphinxcontrib.html

%prep
%setup -q -n sphinxcontrib-blockdiag-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.rst
%{python_sitelib}/*

%changelog
