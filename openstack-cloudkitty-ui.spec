%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name cloudkitty-dashboard
%global mod_name cloudkittydashboard
%global with_doc 1

# tests are disabled by default
%bcond_with tests

Name:         openstack-cloudkitty-ui
Version:      XXX
Release:      XXX
Summary:      The UI component for the CloudKitty service

License:      ASL 2.0
URL:          https://github.com/openstack/%{pypi_name}
Source0:      https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:     noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
BuildRequires: git-core
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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
