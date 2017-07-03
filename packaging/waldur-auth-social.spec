Name: waldur-auth-social
Summary: Waldur plugin for social authentication.
Group: Development/Libraries
Version: 0.7.1
Release: 1.el7
License: MIT
Url: http://waldur.com
Source0: %{name}-%{version}.tar.gz

Requires: waldur-core > 0.138.0

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

Obsoletes: nodeconductor-auth-social

%description
Waldur plugin for social authentication.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
* Fri Jun 30 2017 Jenkins <jenkins@opennodecloud.com> - 0.7.1-1.el7
- New upstream release

* Fri Jun 9 2017 Jenkins <jenkins@opennodecloud.com> - 0.7.0-1.el7
- New upstream release

* Wed May 24 2017 Jenkins <jenkins@opennodecloud.com> - 0.6.1-1.el7
- New upstream release

* Sun Apr 23 2017 Jenkins <jenkins@opennodecloud.com> - 0.6.0-1.el7
- New upstream release

* Tue Apr 11 2017 Jenkins <jenkins@opennodecloud.com> - 0.5.0-1.el7
- New upstream release

* Thu Mar 2 2017 Jenkins <jenkins@opennodecloud.com> - 0.4.0-1.el7
- New upstream release

* Tue Jan 24 2017 Jenkins <jenkins@opennodecloud.com> - 0.3.0-1.el7
- New upstream release

* Tue Jan 17 2017 Jenkins <jenkins@opennodecloud.com> - 0.2.1-1.el7
- New upstream release

* Tue Jan 17 2017 Jenkins <jenkins@opennodecloud.com> - 0.2.0-1.el7
- New upstream release

* Wed Dec 7 2016 Jenkins <jenkins@opennodecloud.com> - 0.1.2-1.el7
- New upstream release

* Tue Dec 6 2016 Jenkins <jenkins@opennodecloud.com> - 0.1.1-1.el7
- New upstream release

* Mon Dec 5 2016 Dmitri Tsumak <dmitri@opennodecloud.com> - 0.1.0-1.el7
- Initial version of the package
