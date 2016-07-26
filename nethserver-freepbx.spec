Name: nethserver-freepbx
Version: 0.0.1
Release: 1%{?dist}
Summary: NethServer configuration for FreePBX
License: GPL
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Requires: asterisk13, freepbx
Requires: rh-php56, rh-php56-php-fpm, rh-php56-php-mysql, rh-php56-php-pdo
Requires: nethserver-mysql

%description
nethserver-freepbx is the FreePBX configuration package for NethServer

%prep
%setup -q

%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-%{release}-filelist

%changelog
* Fri Jul 26 2016 Edoardo Spadoni <edoardo.spadoni@nethesis.it> - 0.0.1
- First implementation