# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name cloudkitty-dashboard
%global mod_name cloudkittydashboard
%global with_doc 1

# tests are disabled by default
%bcond_with tests

Name:         openstack-cloudkitty-ui
Version:      9.0.0
Release:      1%{?dist}
Summary:      The UI component for the CloudKitty service

License:      ASL 2.0
URL:          https://github.com/openstack/%{pypi_name}
Source0:      https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

#

BuildArch:     noarch

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-pbr
BuildRequires: git
BuildRequires: python%{pyver}-cloudkittyclient
BuildRequires: openstack-macros
BuildRequires: gettext

Requires: openstack-dashboard
Requires: python%{pyver}-pbr
Requires: python%{pyver}-cloudkittyclient >= 0.5.0
Requires: python%{pyver}-XStatic-D3
# Handle python2 exception
%if %{pyver} == 2
Requires: python-XStatic-Rickshaw
%else
Requires: python%{pyver}-XStatic-Rickshaw
%endif

%description
openstack-cloudkitty-ui is a dashboard for CloudKitty

%if 0%{?with_doc}
%package doc
Summary: Documentation for the CloudKitty dashboard

BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-sphinxcontrib-rsvgconverter

%description doc
Documentation files for the CloudKitty dashboard
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup


%build
# build
%{pyver_build}

%if 0%{?with_doc}
# Build html documentation
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# Remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Move config to horizon
mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/
install -p -D -m 640 %{mod_name}/enabled/_[0-9]* %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/

%check
%if 0%{?with_test}
%{pyver_bin} setup.py test
%endif

%files
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{mod_name}
%{pyver_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_[0-9]*

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Wed Oct 16 2019 RDO <dev@lists.rdoproject.org> 9.0.0-1
- Update to 9.0.0

* Mon Sep 30 2019 RDO <dev@lists.rdoproject.org> 9.0.0-0.1.0rc1
- Update to 9.0.0.0rc1

