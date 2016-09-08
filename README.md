nethserver-freepbx
==================

This package configure FreePBX and Asterisk for NethServer

Installation
------------

    yum --enablerepo=nethserver-testing clean all
    yum install -y centos-release-scl
    yum --enablerepo=nethserver-testing install nethserver-freepbx

This install and configure MariaDB, Asterisk 13, FreePBX 14

FreePBX Modules
---------------

Since there are still a few modules on freepbx mirrors for 14, to see full list of all available modules you need to change FreePBX version to 13. This could have negative consequences, but allow you to install old modules that are probably compatible

    mysql asterisk -e "UPDATE admin SET value = '13.0.999' WHERE variable = 'version'"

Backup
------

FreePBX configuration is stored on mysql, nethserver-backup-data is neeeded to backup it

Open services from external networks
------------------------------------

IAX and WebRTC access can be opened to external networks from server manager web gui -> PBX Access

SIP and other ports, from command line

    config setprop asterisk access public
    signal-event firewall-adjust


User from Active Directory
--------------------------
You can import your active directory user into freepbx by following this official guide from freepbx:

[Import users from Active Directory ](http://wiki.freepbx.org/display/FPG/How+to+Authenticate+User+Manager+via+Microsoft+Active+Directory)

WebRTC
------
You can create WebRTC extension by following this official guide from freepbx:

[Setting up WebRTC on FreePBX](http://wiki.freepbx.org/display/FPG/WebRTC+Phone-UCP#WebRTCPhone-UCP-EnablingWebRTCPhoneforauser)

After the installation of Certificate Manager and WebRTC modules there is a valid self-signed certificate that can be use for WebRTC.

Know bugs:
 - WebRTC under Chrome is not allowed in HTTP
 - WebRTC in UCP module on FreepBX not works as expected. [Ref](http://community.freepbx.org/t/webrtc-phone-with-https/26698/9)

Asterisk
--------

Asterisk 13 is installed from Sangoma FreePBX distro RPMs:

- pjproject-2.4.5-1.9.sng.x86_64.rpm
- libresample-0.1.3-17.2.sng.x86_64.rpm
- asterisk13-voicemail-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-13.9.1-1.17.sng.x86_64.rpm
- sterisk13-alsa-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-odbc-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-core-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-sqlite3-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-snmp-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-ogg-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-speex-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-addons-ooh323-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-pgsql-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-addons-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-addons-mysql-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-curl-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-devel-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-flite-2.2.1.3-3_3118e6a.sng7.x86_64.rpm
- asterisk13-voicemail-odbcstorage-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-doc-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-resample-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-dahdi-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-voicemail-imapstorage-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-tds-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-configs-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-addons-bluetooth-13.9.1-1.17.sng.x86_64.rpm
- asterisk13-addons-core-13.9.1-1.17.sng.x86_64.rpm

 Sangoma repository:
 
       # This is the standard Sangoma Yum Repository

       [sng-base]
       name=Sangoma-$releasever - Base
       mirrorlist=http://mirrorlist.pbx.ws/?release=$releasever&arch=$basearch&repo=os&dist=$dist
       #baseurl=http:/package1.sangoma.net/sng7/$releasever/os/$basearch/
       gpgcheck=0
       gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Sangoma-7

       [sng-updates]
       name=Sangoma-$releasever - Updates
       mirrorlist=http://mirrorlist.pbx.ws/?release=$releasever&arch=$basearch&repo=updates&dist=$dist
       #baseurl=http://package1.sangoma.net/sng7/$releasever/updates/$basearch/
       gpgcheck=0
       gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Sangoma-7

       [sng-extras]
       name=Sangoma-$releasever - Extras
       mirrorlist=http://mirrorlist.pbx.ws/?release=$releasever&arch=$basearch&repo=extras&dist=$dist
       #baseurl=http://package1.sangoma.net/sng7/$releasever/extras/$basearch/
       gpgcheck=0
       gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Sangoma-7

       [sng-pkgs]
       name=Sangoma-$releasever - Sangoma Open Source Packages
       mirrorlist=http://mirrorlist.pbx.ws/?release=$releasever&arch=$basearch&repo=sng7&dist=$dist
       #baseurl=http://package1.sangoma.net/sng7/$releasever/sng7/$basearch/
       gpgcheck=0
       gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Sangoma-7

       [sng-epel]
       name=Sangoma-$releasever - Sangoma Epel mirror
       mirrorlist=http://mirrorlist.pbx.ws/?release=$releasever&arch=$basearch&repo=epel&dist=$dist
       #baseurl=http://package1.sangoma.net/sng7/$releasever/epel/$basearch/
       gpgcheck=0
       gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7


