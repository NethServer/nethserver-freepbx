Name: nethserver-freepbx
Version: 14.2.3
Release: 1%{?dist}
Summary: NethServer configuration for FreePBX
License: GPL
Source0: %{name}-%{version}.tar.gz
# Execute prep-sources to create Source1
Source1: %{name}-cockpit.tar.gz
BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: freepbx
Requires: nethserver-rh-php56-php-fpm
Requires: rh-php56-php-mysql, rh-php56-php-pear, rh-php56-php-pdo
Requires: rh-php56-php-process, rh-php56-php-xml, rh-php56-php-mbstring
Requires: rh-php56-php-intl, rh-php56-php-ldap, rh-php56-php-odbc, rh-php56-php-gd
Requires: nethserver-mysql
Requires: nethserver-unixODBC

%description
nethserver-freepbx is the FreePBX configuration package for NethServer

%prep
%setup -q

%build
%{makedocs}
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/

tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/

cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/
chmod +x %{buildroot}/usr/libexec/nethserver/api/%{name}/*

%{genfilelist} %{buildroot} --file /etc/sudoers.d/50_nsapi_nethserver_freepbx 'attr(0440,root,root)' > %{name}-%{version}-%{release}-filelist
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
%config(noreplace) /etc/asterisk/acl.conf
%config(noreplace) /etc/asterisk/pjproject.conf
%config(noreplace) /etc/sysconfig/httpd-fpbx
%config /etc/dahdi/system.conf

%changelog
* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.2.3-1
- Sudoers based authorizations for Cockpit UI - NethServer/dev#5805

* Tue Sep 03 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.2.1-1
- Cockpit. List correct application version - Nethserver/dev#5819

* Thu Aug 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.2.0-1
- FreePBX Cockpit UI - NethServer/dev#5791

* Thu Feb 07 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 14.1.1-1
- FreePBX: "apply changes" timeout on slower machines - Bug NethServer/dev#5707
- nethserver-freepbx: can't upload audio files, modules or musics bigger than 2 Mb - Bug NethServer/dev#5701

* Fri Jan 11 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 14.1.0-1
- Backup old DB during installation (#52) nethesis/dev#5454

* Tue Nov 27 2018 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.14-1
- nethserver-freepbx: filter out NethServer 6.x samba system accounts - Bug NethServer/dev#5639

* Tue Oct 30 2018 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.13-1
- Package nethserver-X must subscribe nethserver-sssd-save - NethServer/dev#5600
- Removed useless file

* Fri Jul 20 2018 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.12-1
- nethserver-freepbx: wrong path for audio files in backup-data - Bug NethServer/dev#5550

* Thu Jul 12 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.11-1
- Virtualhosts: freepbx wrongly included inside the data backup - Bug NethServer/dev#5540

* Fri Jun 01 2018 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.10-1
- nethserver-freepbx: use php 5.6 to execute Asterisk AGI - Bug NethServer/dev#5499

* Wed May 16 2018 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.9-1
- nethserver-freepbx: SIP TLS access isn't open from trusted networks - Bug NethServer/dev#5492
- Open 5061 TCP Port from local networks NethServer/dev#5492

* Tue May 08 2018 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.8-1
- nethserver-freepbx: wrong log directory permissions - Bug NethServer/dev#5483
- nethserver-freepbx: automatic bind fails if bind password starts with $ - Bug NethServer/dev#5464

* Mon Jan 29 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.7-1
- nethserver-freepbx: LDAP users can't login to amp interface - Bug NethServer/dev#5369

* Thu Jan 25 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.6-1
- PBX: Asterisk logs aren't rotated - Bug NethServer/dev#5411
- PBX: /run/systemd/sessions is filled by sessions files in closing state - Bug NethServer/dev#5412

* Tue Jan 23 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.5-1
- FreePBX doesn't apply modifications to trusted networks - Bug NethServer/dev#5410

* Tue Jan 09 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.4-1
- nethserver-freepbx: backup restore fails - Bug NethServer/dev#5402

* Fri Nov 17 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.3-1
- Make sure Aterisk home directory exists - NethServer/nethserver-freepbx#35

* Wed Oct 25 2017 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.2-1
- Configure voicemail ODBC storage NethServer/dev#5363

* Fri Oct 20 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 14.0.1-1
- FreePBX user syncing fails on 7.4 with AD user provider - Bug NethServer/dev#5361

* Thu Aug 31 2017 Stefano Fancello <stefano.fancello@nethesis.it> - 14.0.0-1
- nethserver-freepbx first release

* Fri Jul 26 2016 Edoardo Spadoni <edoardo.spadoni@nethesis.it> - 0.0.1
- First implementation
