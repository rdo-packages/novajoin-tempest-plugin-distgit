%global service novajoin
%global plugin novajoin-tempest-plugin
%global module novajoin_tempest_plugin
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of Novajoin
License:    ASL 2.0
URL:        https://github.com/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{version}.tar.gz

BuildArch:  noarch

%description
This package contains Tempest tests to cover the Novajoin project.
Additionally it provides a plugin to automatically load these tests into tempest.


%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

Requires:   python-pbr
Requires:   python-tempest >= 1:12.1.0
Requires:   python-oslo-config >= 3.22.0

%description -n python2-%{service}-tests-tempest
This package contains Tempest tests to cover the Novajoin project.
Additionally it provides a plugin to automatically load these tests into tempest.

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-openstackdocstheme

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Novajoin tempest tests.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-pbr
Requires:   python3-tempest >= 1:12.1.0
Requires:   python3-oslo-config >= 3.22.0

%description -n python3-%{service}-tests-tempest
This package contains Tempest tests to cover the Novajoin project.
Additionally it provides a plugin to automatically load these tests into tempest.
%endif


%prep
%autosetup -n %{module}-%{upstream_version} -S git

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
%{__python2} setup.py build_sphinx
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}-tests-tempest
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}-tests-tempest
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
