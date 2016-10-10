==================
nethserver-freepbx
==================

This package configures FreePBX and Asterisk for NethServer

Installation
============

::

    yum --enablerepo=nethserver-testing clean all
    yum --enablerepo=nethserver-testing install nethserver-freepbx

MariaDB, Asterisk 13 and FreePBX 14 will be installed and configured.

FreePBX Modules
===============

Since there are still a few modules on freepbx mirrors for 14, to see the full list of all available modules you need to change FreePBX version to 13. This could have negative consequences, but allows you to install old modules that are probably compatible.

::

    mysql asterisk -e "UPDATE admin SET value = '13.0.999' WHERE variable = 'version'"

Backup
======

FreePBX configuration is stored in mysql, nethserver-backup-data is neeeded to backup it.

Open services from external networks
====================================

IAX and WebRTC access can be opened to external networks from server manager web gui -> PBX Access

SIP and other ports, from command line

::

    config setprop asterisk access public
    signal-event firewall-adjust


User from Active Directory
==========================

You can import your active directory user into freepbx by following this official guide from freepbx:

[Import users from Active Directory ](http://wiki.freepbx.org/display/FPG/How+to+Authenticate+User+Manager+via+Microsoft+Active+Directory)

WebRTC
======

You can create WebRTC extensions following this official guide from freepbx:

[Setting up WebRTC on FreePBX](http://wiki.freepbx.org/display/FPG/WebRTC+Phone-UCP#WebRTCPhone-UCP-EnablingWebRTCPhoneforauser)

After the installation of Certificate Manager and WebRTC modules there is a valid self-signed certificate that can be used for WebRTC.

How to test it
--------------

1. From "Advanced settings" page:

   - Enable the mini-HTTP Server
   - Set HTTP and HTTPS bind addresses to 0.0.0.0

2. Configure a user with a virtual extension

3. Enable WebRTC

4. Temporarly disable the firewall:

   ::
  
   shorewall clear

Given a virtual extension 200, FreePBX will create a new extension 99200 for WebRTC.
Open one of the following WebRTC client and use these settings:

- Name: <yourname>
- SIP URI: sip:99200@<server_ip>
- WS URI: wss://<server_ip>:8089/ws
- Password: read from MySQL

  ::

  mysql asterisk -e "select data from sip where id='99200' and keyword = 'secret';"


WebRTC clients:

- http://jssip.net/
- https://www.doubango.org/sipml5/

Known bugs
----------

- WebRTC under Chrome is not allowed in HTTP
- WebRTC in UCP module on FreepBX doesn't work as expected. [Ref](http://community.freepbx.org/t/webrtc-phone-with-https/26698/9)

Asterisk
========

Asterisk 13 is installed from Sangoma FreePBX distro RPMs.

Sangoma repository: ::

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

