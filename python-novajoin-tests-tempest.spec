%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global service novajoin-tests-tempest
%global plugin novajoin-tempest-plugin
%global module novajoin_tempest_plugin
%global with_doc 1
%global common_desc \
This package contains Tempest tests to cover the Novajoin project. \
Additionally it provides a plugin to automatically load these tests \
into tempest.


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-%{service}
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of Novajoin
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}

Source0:    http://tarballs.opendev.org/x/%{plugin}/%{module}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.opendev.org/x/%{plugin}/%{module}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{service}
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

Requires:   python3-ipalib
Requires:   python3-oslo-config >= 2:5.2.0
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-pbr >= 3.1.1
Requires:   python3-six >= 1.10.0
Requires:   python3-tempest >= 1:18.0.0
Requires:   python3-ipaclient

Requires:   python3-gssapi

%description -n python3-%{service}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-doc
Summary:        python-%{service} documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description -n python-%{service}-doc
This package contains the documentation for the Novajoin tempest tests.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{module}-%{upstream_version} -S git

# remove requirements
%py_req_cleanup
# Remove bundled egg-info
rm -rf *.egg-info

%build
%{py3_build}

# Generate Docs
%if 0%{?with_doc}
%{__python3} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%files -n python3-%{service}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
