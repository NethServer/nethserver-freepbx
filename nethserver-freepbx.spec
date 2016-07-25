Name: nethserver-freepbx
Version: 14
Release: 1%{?dist}
Summary: NethServer configuration for FreePBX
Group: Networking/Daemons
License: GPL
Source0: freepbx-%{version}.tar.gz
Packager: nethesis srl <support@nethesis.it>
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: freepbx >= 14

%description
nethserver-freepbx is the FreePBX configuration package for NethServer

%prep
%setup
%build
%install
%clean
%pre
%preun
%post
%postun

%changelog
