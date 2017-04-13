===============
External Access
===============
Allow to open IAX, WebRTC and WebSocket to public networks 

Allow external IAX access
=======================================
Enabling IAX access, it will be possible to create IAX connection with PBX from public networks.
UDP 4569 and UDP 5060 ports will be opened

Allow external SIP TLS access
==============================
Enabling SIP TLS access, it will be possible to connect to PBX using SIP TLS. This option opens SIP TLS port TCP 5061 and SRTP UDP ports from 10000 to 20000

Allow external WebRTC and WebSocket access
======================================================
Enabling WebRTC and WebSocket access, it will be possible to connect to PBX using a WebRTC SIP Phone
TCP 8089 and TCP 8181 ports will be opened

========================
PBX Web interface access
========================

For security reasons, access to PBX web configuration gui is allowed only from local and trusted networks.
From this page it's possible to add new network allowed to access to PBX web interface.

Create new
=====================

Add a new network allowed to access to PBX web gui

Network address
    Network address of the allowed network to add

Network mask
    Network mask of the allowed network to add

