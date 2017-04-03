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


Users
=====

User are synced with NethServer users. You can manually force Userman module sync with

::

    /usr/bin/scl enable rh-php56 "/usr/sbin/fwconsole userman sync"


WebRTC
======

You can create WebRTC extensions following this official guide from freepbx:

- http://wiki.freepbx.org/display/FPG/WebRTC+Phone-UCP#WebRTCPhone-UCP-EnablingWebRTCPhoneforauser

After the installation of Certificate Manager and WebRTC modules there is a valid self-signed certificate that can be used for WebRTC.

How to test it
--------------

1. Install "Certificate management" module

2. From "Advanced settings" page:

   - Enable the mini-HTTP Server
   - Set "SIP Channel Driver" to `chan_pjsip`

3. From "SIP settings", inside the PJSIP tab, set the following values:

   - Certificate Manager: default
   - SSL Method: default
   - Verify Client: No
   - Verify Server: No
   - udp: yes
   - tcp: no
   - tls: no
   - ws: yes
   - wss: yes
   - Port listen: 5160

4. Configure a new PJSIP extension and set the following values:

   - Enable AVPF: yes
   - Enable ICE Support: yes
   - Media use received transport: no
   - RTP symmetric: yes
   - Media encryption: DTLS-SRTP
   - Require RTP (media) encryption: yes
   - Enable DTLS: yes
   - Use certificate: default
   - DTLS verify: no
   - DLTS setup: Act/Pass
   - DTLS Rekey Interval: 0


5. Restart asterisk and temporarly disable the firewall:

   ::
  
   systemctl restart asterisk
   shorewall clear

6. Open `https://<server_ip>:8089/ws` URL with the browser and accept the certificate

7. Try with one of the below WebRTC cients:

- http://jssip.net/
- https://www.doubango.org/sipml5/

Known bugs
----------

- WebRTC under Chrome is not allowed in HTTP
- WebRTC in UCP module on FreepBX doesn't work as expected. (http://community.freepbx.org/t/webrtc-phone-with-https/26698/9)
- WebRTC doesn't work on Firefox

The server may raise the following error: ::

 ERROR[23205][C-00000007]: res_rtp_asterisk.c:2172 __rtp_recvfrom: 
 DTLS failure occurred on RTP instance '0x7fa9540f54d8' due to reason 'missing tmp ecdh key', terminating

By the way, the bug should be already fixed, see: https://issues.asterisk.org/jira/browse/ASTERISK-25265

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


Source RPMs
-----------

Add this repository: ::

 [sng-src]
 name=SRPMs for Sanoma specific packages
 baseurl=http://package1.sangoma.net/sangoma/src
 gpgcheck=0
 enabled=0

Use yum downloader: ::

 yumdownloader --source kmod-dahdi-linux-2.11.1-3.10.0_327.36.1.el7.24.sng7.x86_64 --enablerepo=sng-src


Download all asterisk RPMs
--------------------------

You can download all needed RPMs from upstream using rpm-harvester: ::

  git clone -b freepbx https://github.com/Stell0/rpm-harvester.git
  cd rpm-harvester
  wget https://raw.githubusercontent.com/NethServer/nethserver-freepbx/master/asterisk-rpms
  ./get_rpms.sh `cat asterisk-rpms | sed '/^#/d'`

All downloaded packages will be available inside the RPMs directory.
