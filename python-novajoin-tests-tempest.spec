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
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

Name:       python-%{service}
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of Novajoin
License:    Apache-2.0
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
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{service}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-doc
Summary:        python-%{service} documentation

%description -n python-%{service}-doc
This package contains the documentation for the Novajoin tempest tests.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{module}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -R
%endif

%build
%pyproject_wheel

# Generate Docs
%if 0%{?with_doc}
%tox -e docs
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%files -n python3-%{service}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{service}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
