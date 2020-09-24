%global milestone .0rc1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name cloudkitty-dashboard
%global mod_name cloudkittydashboard
%global with_doc 1

# tests are disabled by default
%bcond_with tests

Name:         openstack-cloudkitty-ui
Version:      11.0.0
Release:      0.1%{?milestone}%{?dist}
Summary:      The UI component for the CloudKitty service

License:      ASL 2.0
URL:          https://github.com/openstack/%{pypi_name}
Source0:      https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

#
# patches_base=11.0.0.0rc1
#

BuildArch:     noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
BuildRequires: git
BuildRequires: python3-cloudkittyclient
BuildRequires: openstack-macros
BuildRequires: gettext

Requires: openstack-dashboard
Requires: python3-pbr
Requires: python3-cloudkittyclient >= 0.5.0
Requires: python3-XStatic-D3
Requires: python3-XStatic-Rickshaw

%description
openstack-cloudkitty-ui is a dashboard for CloudKitty

%if 0%{?with_doc}
%package doc
Summary: Documentation for the CloudKitty dashboard

BuildRequires: python3-openstackdocstheme
BuildRequires: python3-sphinx
BuildRequires: python3-sphinxcontrib-rsvgconverter

%description doc
Documentation files for the CloudKitty dashboard
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup


%build
# build
%{py3_build}

%if 0%{?with_doc}
# Build html documentation
sphinx-build -W -b html doc/source doc/build/html
# Remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Move config to horizon
mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/
install -p -D -m 640 %{mod_name}/enabled/_[0-9]* %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/

%check
%if 0%{?with_test}
%{__python3} setup.py test
%endif

%files
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{mod_name}
%{python3_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_[0-9]*

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Thu Sep 24 2020 RDO <dev@lists.rdoproject.org> 11.0.0-0.1.0rc1
- Update to 11.0.0.0rc1

