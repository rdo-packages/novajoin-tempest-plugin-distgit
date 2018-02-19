%{!?upstream_version: %global upstream_version %{commit}}
%global commit 59d7ba68345a55cd7c6879b623177ebdc39b0414
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global service novajoin-tests-tempest
%global plugin novajoin-tempest-plugin
%global module novajoin_tempest_plugin
%global with_doc 1
%global common_desc \
This package contains Tempest tests to cover the Novajoin project. \
Additionally it provides a plugin to automatically load these tests \
into tempest.

%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?dlrn}
%define tarsources %module
%else
%define tarsources %plugin
%endif

Name:       python-%{service}
Version:    0.0.1
Release:    0.1%{?alphatag}%{?dist}
Summary:    Tempest Integration of Novajoin
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}

Source0:    http://github.com/openstack/%{plugin}/archive/%{commit}.tar.gz#/%{plugin}-%{shortcommit}.tar.gz

BuildArch:  noarch
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{service}
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}}
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-six

Requires:   python2-ipalib
%if 0%{?fedora}
Requires:   python2-gssapi
%else
Requires:   python-gssapi
%endif
Requires:   python2-oslo-config >= 2:4.0.0
Requires:   python2-oslo-log >= 3.30.0
Requires:   python2-pbr >= 2.0.0
Requires:   python2-six >= 1.9.0
Requires:   python2-tempest >= 1:17.2.0

%description -n python2-%{service}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-doc
Summary:        python-%{service} documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description -n python-%{service}-doc
This package contains the documentation for the Novajoin tempest tests.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

Requires:   python3-ipalib
Requires:   python3-gssapi
Requires:   python3-oslo-config >= 2:4.0.0
Requires:   python3-oslo-log >= 3.30.0
Requires:   python3-pbr >= 2.0.0
Requires:   python3-six >= 1.9.0
Requires:   python3-tempest >= 1:17.2.0

%description -n python3-%{service}
%{common_desc}
%endif


%prep
%autosetup -n %{tarsources}-%{upstream_version} -S git

# remove requirements
%py_req_cleanup
# Remove bundled egg-info
rm -rf *.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Mon Feb 19 2018 Chandan Kumar <chkumar@redhat.com> 0.0.1-0.1.59d7ba68git
- Update to pre-release 0.0.1 (59d7ba68345a55cd7c6879b623177ebdc39b0414)