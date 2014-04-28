%global dnf_version 0.4.19

Name:		dnf-utils
Version:	0.0.3
Release:	1%{?dist}
Summary:	Add-on tools for DNF
Group:		System Environment/Base
License:	GPLv2+
URL:		https://github.com/timlau/dnf-utils
Source0:	https://github.com/timlau/dnf-utils/archive/%{name}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python-nose
BuildRequires:	python2-devel
BuildRequires:	gettext
BuildRequires:	dnf >= %{dnf_version}
Requires:	dnf >= %{dnf_version}

%description
Add-on tools for DNF (Python 2.x)

%package -n python3-%{name}
Summary:	Add-on tools for DNF
Group:		System Environment/Base
BuildRequires:	python3-devel
BuildRequires:	python3-nose
BuildRequires:	python3-dnf >= %{dnf_version}
Requires:	python3-dnf >= %{dnf_version}

%description -n python3-%{name}
Add-on tools for DNF (Python 3.x)

%build

%prep
%setup -q

%install

make DESTDIR=$RPM_BUILD_ROOT install

%find_lang %name

%check

PYTHONPATH=./plugins nosetests-2.7 -s tests/
PYTHONPATH=./plugins nosetests-3.3 -s tests/

%files -f  %{name}.lang
%doc AUTHORS COPYING README.md
%{python_sitelib}/dnfutils/*
%{python_sitelib}/dnf-plugins/*

%files -n python3-%{name} -f  %{name}.lang
%doc AUTHORS COPYING README.md
%{python3_sitelib}/dnfutils/*
%{python3_sitelib}/dnf-plugins/*

%changelog
* Mon Apr 28 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.0.3-1
- dnl: added new dnl tool (timlau@fedoraproject.org)
- query: show list tags as comma separated (timlau@fedoraproject.org)
- --show-help support in tools (timlau@fedoraproject.org)
- tests: python 3 compabiltty and unittest for shared lib
  (timlau@fedoraproject.org)
- pushed translation strings to transifex (timlau@fedoraproject.org)
- move common functionality into custom ArgumentParser to avoid code
  duplication (timlau@fedoraproject.org)
- add real transifex setup. added translation wrapper til query tool refreshed
  translations (timlau@fedoraproject.org)
- added --whatrequires renamed --provides to --whatprovides
  (timlau@fedoraproject.org)
- added wrapper to format dnf package attr for output. added --showtags,
  --help-query flags (timlau@fedoraproject.org)
- query: added --repoid, --arch & --provides options, fixed --latest
  (timlau@fedoraproject.org)

* Sun Apr 13 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.0.2-1
- build: add check Makefile target to run tests (timlau@fedoraproject.org)
- query: added --queryformat option to specify an rpm QUERYFMT like output
  format (timlau@fedoraproject.org)
- query: add new query tool (timlau@fedoraproject.org)

* Fri Apr 11 2014 Tim Lauridsen <timlau@fedoraproject.org> - 0.0.1-1
- Initial package


