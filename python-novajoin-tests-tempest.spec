%global service novajoin-tests-tempest
%global plugin novajoin-tempest-plugin
%global module novajoin_tempest_plugin
%global with_doc 1
%global common_desc \
This package contains Tempest tests to cover the Novajoin project. \
Additionally it provides a plugin to automatically load these tests \
into tempest.


%{!?upstream_version: %global upstream_version %{commit}}
%global commit cb81f5311ec90174c1cd9b9736a8c503f34824bc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%{?dlrn: %global tarsources %{module}-%{upstream_version}}
%{!?dlrn: %global tarsources %{plugin}}

Name:       python-%{service}
Version:    0.0.1
Release:    0.5%{?alphatag}%{?dist}
Summary:    Tempest Integration of Novajoin
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}

Source0:    http://opendev.org/x/%{plugin}/archive/%{upstream_version}.tar.gz#/%{module}-%{shortcommit}.tar.gz

BuildArch:  noarch
BuildRequires:  git
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
%autosetup -n %{tarsources} -S git

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
* Wed May 06 2020 RDO <dev@lists.rdoproject.org> - 0.0.1-0.5.cb81f53git
- Update to post 0.0.1 (cb81f5311ec90174c1cd9b9736a8c503f34824bc)
