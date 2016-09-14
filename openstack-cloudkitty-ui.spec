%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name cloudkitty-dashboard
%global mod_name cloudkittydashboard

# tests are disabled by default
%bcond_with tests

Name:         openstack-cloudkitty-ui
Version:      0.5.1
Release:      1%{?dist}
Summary:      The UI component for the CloudKitty service

License:      ASL 2.0
URL:          https://github.com/openstack/%{pypi_name}
Source0:      http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx
BuildRequires: git
BuildRequires: python-cloudkittyclient

BuildRequires: gettext

Requires: openstack-dashboard
Requires: python-pbr
Requires: python-cloudkittyclient

%description
openstack-cloudkitty-ui is a dashboard for CloudKitty

%package doc
Summary: Documentation for the CloudKitty dashboard
%description doc
Documentation files for the CloudKitty dashboard

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt


%build
# build
%py2_build
# Build html documentation
sphinx-build doc/source html
# Remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install

# Move config to horizon
mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/
install -p -D -m 640 %{mod_name}/enabled/_[0-9]* %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/

%check
%if 0%{?with_test}
%{__python2} setup.py test
%endif

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{mod_name}
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_[0-9]*

%files doc
%doc html
%license LICENSE

%changelog
* Wed Sep 14 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.5.1-1
- Upstream 0.5.1

* Wed Sep 14 2016 Haikel Guemar <hguemar@fedoraproject.org> 0.5.0-1
- Update to 0.5.0

