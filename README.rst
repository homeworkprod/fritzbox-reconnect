=========================
``fritzbox-reconnect.py``
=========================

Instruct an AVM FRITZ!Box via UPnP to reconnect.

This is usually realized with tools like Netcat_ or cURL_.  However,
when developing in Python_ anyway, it is more convenient to integrate a
native implementation.  This one requires Python_ 2.5 or higher.

UPnP_ (Universal Plug and Play) control messages are based on SOAP_,
which is itself based on XML_, and transmitted over HTTP_.

Make sure UPnP_ is enabled on the FRITZ!Box.

A reconnect only takes a few second while restarting the box takes about
up to a minute; not counting the time needed to navigate through the web
interface.

.. _Netcat: http://netcat.sourceforge.net/
.. _cURL:   http://curl.haxx.se/
.. _Python: http://www.python.org/
.. _UPnP:   http://www.upnp.org/
.. _SOAP:   http://www.w3.org/TR/soap/
.. _XML:    http://www.w3.org/XML/
.. _HTTP:   http://tools.ietf.org/html/rfc2616


License
=======

Licensed under the terms of the MIT license.


Author
======

Created by Jochen Kupperschmidt.
