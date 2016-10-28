Name: nethserver-freepbx
Version: 0.0.1
Release: 1%{?dist}
Summary: NethServer configuration for FreePBX
License: GPL
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: freepbx
Requires: rh-php56, rh-php56-php-fpm
Requires: rh-php56-php-mysql, rh-php56-php-pear, rh-php56-php-pdo
Requires: rh-php56-php-process, rh-php56-php-xml, rh-php56-php-mbstring
Requires: rh-php56-php-intl, rh-php56-php-ldap, rh-php56-php-odbc, rh-php56-php-gd
Requires: nethserver-mysql

%description
nethserver-freepbx is the FreePBX configuration package for NethServer

%prep
%setup -q

%build
%{makedocs}
perl createlinks

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}/%{_localstatedir}/log/httpd-fpbx

%post
%systemd_post httpd-admin.service asterisk.service

%preun
%systemd_preun httpd-admin.service asterisk.service

%postun
%systemd_postun


%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)

%dir %{_nseventsdir}/%{name}-update

%attr(0644,root,root) %config %{_sysconfdir}/httpd/fpbx-conf/httpd.conf
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd-fpbx
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/httpd-fpbx/access_log
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/httpd-fpbx/error_log
%config(noreplace) /etc/sysconfig/httpd-fpbx
%config /etc/dahdi/system.conf

%changelog
* Fri Jul 26 2016 Edoardo Spadoni <edoardo.spadoni@nethesis.it> - 0.0.1
- First implementation
