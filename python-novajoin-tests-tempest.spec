%{!?upstream_version: %global upstream_version %{commit}}
%global commit 3f51bbe815a21527475db38cbd3dabf8603e4498
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git
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
Version:    0.0.1
Release:    0.3%{?alphatag}%{?dist}
Summary:    Tempest Integration of Novajoin
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}

Source0:    https://opendev.org/openstack/%{plugin}/archive/%{upstream_version}.tar.gz#/%{module}-%{shortcommit}.tar.gz

BuildArch:  noarch
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{service}
Summary: %{summary}
%{?python_provide:%python_provide python%{pyver}-%{service}}
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-six

Requires:   python%{pyver}-ipalib
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-pbr >= 3.1.1
Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-tempest >= 1:18.0.0
Requires:   python%{pyver}-ipaclient

# Handle python2 exception
%if %{pyver} == 2
Requires:   python-gssapi
%else
Requires:   python%{pyver}-gssapi
%endif

%description -n python%{pyver}-%{service}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-doc
Summary:        python-%{service} documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{service}-doc
This package contains the documentation for the Novajoin tempest tests.
%endif

%prep
%autosetup -n %{module}-%{upstream_version} -S git

# remove requirements
%py_req_cleanup
# Remove bundled egg-info
rm -rf *.egg-info

%build
%{pyver_build}

# Generate Docs
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n python%{pyver}-%{service}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Thu Feb 15 2018 RDO <dev@lists.rdoproject.org> 0.0.1-0.3.3f51bbegit
- Update to pre-release 0.0.1 (3f51bbe815a21527475db38cbd3dabf8603e4498)

