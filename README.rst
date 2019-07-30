==================
nethserver-freepbx
==================

This package configures FreePBX and Asterisk for NethServer
MariaDB, Asterisk 13 and FreePBX 14 will be installed and configured.

FreePBX Web UI Access
======================

FreePBX is now reachable at https://IP_ADDRESS/freepbx from green interfaces. To add an IP address or a network from red allowed to access interface, configure it from NethServer Web UI under "PBX Access" page


Backup
======

Since FreePBX configuration is stored in MariaDB, database dump are split inside data and configuration backup:

* configuration backup: contains the ``asterisk`` db with all configurations (extensions, trunks, etc.)
* data backup: contanins the ``asteriskcdrdb`` db containg all PBX events

Open services from external networks
====================================

IAX and WebRTC access can be opened to external networks from server manager web gui -> PBX Access

SIP and other ports, from command line (Dangerous! Do it only if you know what you're doing)

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
- WebRTC in UCP module on FreepBX may not work as expected. (http://community.freepbx.org/t/webrtc-phone-with-https/26698/9)
- WebRTC may not work on Firefox

Custom User Management configuration
------------------------------------

The ``nethserver-freepbx-conf-users action`` configures users using NethServer SSSD configuration. 
This creates an entry in userman FreePBX module called ``NethServer [AD|LDAP]``.

If you need to edit this entry and you don't want it to be modified when nethserver-freepbx-conf-users is launched again, 
change it's name adding "Custom" (or any other string) at the end. Example: 'NethServer AD' -> 'NethServer AD Custom'

If you remove ``NethServer [AD|LDAP]`` string, another entry will be created by ``nethserver-freepbx-conf-users`` action.

To check user synchronization, use this command: ::

 /usr/bin/scl enable rh-php56 -- /usr/sbin/fwconsole userman --syncall --force --verbose

Syncronization need a secure connection, use SSL or enable ``STARTTLS`` in ``Account Provider`` configuration in NethServer Web GUI

Update from legacy OpenLDAP driver to OpenLDAP2 driver
------------------------------------------------------

Since nethserver-freepbx-14.0.5, if NethServer users are configured using OpenLDAP, FreePBX users are configured using FreePBX OpenLDAP 2 driver instead of legacy one.
If you have installed nethserver-freepbx before 14.0.5, and your user provider is configured using LDAP, you're using legacy driver. You can check in FreePBX User Manager module interface if NethServer LDAP driver is "OpenLDAP Directory (Legacy)"

Updating from legacy driver to the new one, allows to permit access to FreePBX interface and UCP to LDAP users, but migration isn't automatical because users would lose default extension associated and other custom options.
The openldap_migration_from_legacy script, does the driver migration and restore users default_extensions. Other custom users options could be lost anyway.
To execute migration, launch: ::

  /usr/src/freepbx/openldap_migration_from_legacy


Cockpit API
===========

settings/read
---------------

This api returns ``asterisk`` and ``httpd-fpbx`` configuration.

Input
^^^^^

- ``config``: ``asterisk`` or ``httpd-fpbx``

Input example (asterisk)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "config": "asterisk"
  }

Output example (asterisk)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "configuration": {
      "type": "service",
      "name": "asterisk",
      "props": {
        "status": "enabled",
        "TCPPorts": "5060,5061,5038,8088,8089",
        "AllowExternalIAX": "disabled",
        "access": "green",
        "AllowExternalSIPS": "enabled",
        "AllowExternalWebRTC": "disabled",
        "UDPPorts": "4569,5036,5060,5160,10000:20000"
      }
    }
  }

Input example (httpd-fpbx)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "config": "httpd-fpbx"
  }

Output example (httpd-fpbx)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "configuration": {
      "type": "service",
      "name": "httpd-fpbx",
      "props": {
        "status": "enabled",
        "access": "green",
        "ValidFrom": "10.20.30.40/255.255.255.0,10.0.0.5/255.255.255.0"
      }
    }
  }

settings/validate
------------------

This api validates an IP address allowed to access PBX web interface

Input
^^^^^

- ``ipAddress``: an IP address
- ``netmask``: a network netmask

Input example
^^^^^^^^^^^^^^
::

  {
    "ipAddress": "10.20.30.40",
    "netmask": "255.255.255.0"
  }

Output example
^^^^^^^^^^^^^^^
::

  {
    "state": "success"
  }

settings/update
-----------------

This api updates ``asterisk`` and ``httpd-fpbx`` configuration.

Input
^^^^^

- ``config``: ``externalAccess`` or ``webInterfaceAccess``
- ``allowExternalIAX``: boolean flag to enable or disable external telephony access through IAX protocol (only if ``config``: ``externalAccess``)
- ``allowExternalSIPS``: boolean flag to enable or disable external telephony access through secure SIP TLS protocol (only if ``config``: ``externalAccess``)
- ``webInterfaceAccess``: list of IP addresses and netmasks allowed to access PBX web interface (only if ``config``: ``webInterfaceAccess``)

Input example (externalAccess)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "config": "externalAccess",
    "allowExternalIAX": "enabled",
    "allowExternalSIPS": "enabled"
  }

Input example (webInterfaceAccess)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "config": "webInterfaceAccess",
    "webInterfaceAccess": [
      {
        "ipAddress": "5.6.7.8",
        "netmask": "255.255.255.0"
      },
      {
        "ipAddress": "10.20.30.40",
        "netmask": "255.255.255.0"
      }
    ]
  }
