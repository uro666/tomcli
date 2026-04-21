%define module tomcli
%bcond manpages 1
%bcond tests 1

Name:		tomcli
Summary:	CLI for working with TOML files
Version:	0.10.1
Release:	1
License:	MIT
Group:		Development/Python
URL:		https://pypi.org/project/tomcli
Source0:	https://files.pythonhosted.org/packages/source/t/%{module}/%{module}-%{version}.tar.gz

BuildSystem:	python
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(click)
BuildRequires:	python%{pyver}dist(flit-core)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	python%{pyver}dist(tomlkit)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif
%if %{with manpages}
BuildRequires:  scdoc
%endif
Requires:	python%{pyver}dist(tomlkit)

%description
CLI for working with TOML files.

%build -a
%if %{with manpages}
for page in doc/*.scd; do
    dest="${page%.scd}"
    scdoc <"${page}" >"${dest}"
done
%endif

%install -a
%if %{with manpages}
# Install manpages
mkdir -p %{buildroot}%{_mandir}/man1
install -Dpm 0644 doc/*.1 -t %{buildroot}%{_mandir}/man1
%endif

# Install shell completions
(
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
export PATH="%{buildroot}%{_bindir}:${PATH}"
%{__python} compgen.py \
    --installroot %{buildroot} \
    --bash-dir %{_datadir}/bash-completion/completions \
    --fish-dir %{_datadir}/fish/vendor_completions.d \
    --zsh-dir %{_datadir}/zsh/site-functions
)


%if %{with tests}
%check
export CI=true
TOMCLI="%{buildroot}%{_bindir}/%{module}"
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pytest
%endif

%files
%doc README.md NEWS.md
%license LICENSE
%{_bindir}/%{module}*
%{_datadir}/bash-completion/completions/%{module}*
%{_datadir}/fish/vendor_completions.d/%{module}*.fish
%{_datadir}/zsh/site-functions/_%{module}*
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}.dist-info
%if %{with manpages}
%{_mandir}/man1/%{module}*.1*
%endif
