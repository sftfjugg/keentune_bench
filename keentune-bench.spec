%define anolis_release 0

Name:           keentune-bench
Version:        2.0
Release:        %{?anolis_release}%{?dist}
Url:            https://gitee.com/anolis/keentune_bench
Summary:        Benchmark script running models for KeenTune
Vendor:         Alibaba
License:        MulanPSLv2
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch
Requires:       python3-tornado

Requires(post): 	systemd
Requires(preun): 	systemd
Requires(postun): 	systemd

%description
Benchmark script running models for KeenTune

%prep
%autosetup -n %{name}-%{version}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --single-version-externally-managed -O1 \
			      --prefix=%{_prefix} \
			      --root=%{buildroot} \
 			      --record=INSTALLED_FILES

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system/
cp -f ./keentune-bench.service ${RPM_BUILD_ROOT}/usr/lib/systemd/system/
install -D -m 0644 man/keentune-bench.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/keentune-bench.8
install -D -m 0644 man/keentune-bench.conf.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/keentune-bench.conf.5

%clean
rm -rf $RPM_BUILD_ROOT

%post
systemctl daemon-reload

%preun
%systemd_preun keentune-bench.service

%postun
%systemd_postun_with_restart keentune-bench.service

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{_prefix}/lib/systemd/system/keentune-bench.service
%{_mandir}/man8/keentune-bench.8*
%{_mandir}/man5/keentune-bench.conf.5*

%changelog
* Wed Sep 21 2022 Runzhe Wang <runzhe.wrz@alibaba-inc.com> - 1.4.0-0
- feat: new API /avaliable to checkout if destination touchable

* Thu Jul 21 2022 Runzhe Wang <runzhe.wrz@alibaba-inc.com> - 1.3.0-1
- fix: missing of man dir  

* Thu Jun 30 2022 Runzhe Wang <runzhe.wrz@alibaba-inc.com> - 1.3.0-0
- update config items in bench.conf
- return error message if benchmark script return an invalid data

* Mon Jun 20 2022 Runzhe Wang <runzhe.wrz@alibaba-inc.com> - 1.2.1-1
- update docs

* Thu Mar 03 2022 Runzhe Wang <runzhe.wrz@alibaba-inc.com> - 1.1.0-1
- fix bug: update version to 1.1.0 in setup.py script.
- refactor tornado module: replace await by threadpool
- fix other bugs

* Tue Feb 01 2022 Runzhe Wang <runzhe.wrz@alibaba-inc.com>- 1.0.1
- Supporting of multiple target tuning
- Remove version limitation of tornado
- Fix some user experience issues

* Wed Jan 26 2022 Runzhe Wang <runzhe.wrz@alibaba-inc.com> - 1.0.0
- remove empty conf dir when uninstall keentune-bench
- fix bug: can not running in alinux2 and centos7
- change modify codeup address to gitee
- add keentune to systemd
- use '%license' macro
- update license to MulanPSLv2
- Initial KeenTune-bench
