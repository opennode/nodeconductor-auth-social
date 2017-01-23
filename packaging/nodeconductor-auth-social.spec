Name: nodeconductor-auth-social
Summary: NodeConductor plugin for social authentication.
Group: Development/Libraries
Version: 0.2.1
Release: 1.el7
License: MIT
Url: http://nodeconductor.com
Source0: %{name}-%{version}.tar.gz

Requires: nodeconductor > 0.118.0

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

%description
NodeConductor plugin for social authentication.

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
