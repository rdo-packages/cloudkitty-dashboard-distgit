%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name cloudkitty-dashboard
%global mod_name cloudkittydashboard

# tests are disabled by default
%bcond_with tests

Name:         openstack-cloudkitty-ui
Version:      XXX
Release:      XXX
Summary:      The UI component for the CloudKitty service

License:      ASL 2.0
URL:          https://github.com/openstack/%{pypi_name}
Source0:      https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-pbr
BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: git
BuildRequires: python2-cloudkittyclient
BuildRequires: openstack-macros

BuildRequires: gettext

Requires: openstack-dashboard
Requires: python2-pbr
Requires: python2-cloudkittyclient >= 0.5.0

%description
openstack-cloudkitty-ui is a dashboard for CloudKitty

%package doc
Summary: Documentation for the CloudKitty dashboard
%description doc
Documentation files for the CloudKitty dashboard

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup


%build
# build
%py2_build
# Build html documentation
python setup.py build_sphinx -b html
# Remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

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
%doc doc/build/html
%license LICENSE

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/cloudkitty-dashboard/commit/?id=33339cdd4edd7dba0dfb04a85ec5e7c35b9d0d6d
