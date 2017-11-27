Installation
------------

* `Install Waldur <http://nodeconductor.readthedocs.org/en/latest/guide/intro.html#installation-from-source>`_

* Clone Waldur Auth Social repository

  .. code-block:: bash

    git clone https://github.com/opennode/waldur-auth-social.git

* Install Waldur Auth Social into Waldur virtual environment

  .. code-block:: bash

    cd /path/to/waldur-auth-social/
    python setup.py install

Configuration
-------------

Add WALDUR_AUTH_SOCIAL dictionary to Waldur settings.
It will contain settings for Waldur Auth Social application.

* GOOGLE_SECRET - secret key of GooglePlus application (key from test application: 5ivAldGqEv3K5rKZL2QIUfme)
* FACEBOOK_SECRET - secret key of Facebook application (key from test application: fdd9d7ed8cee4a97ff49d2209d3d3db6)
* USER_ACTIVATION_URL_TEMPLATE - URL template of frontend site, which is used for account activation, for example
  http://example.com/#/activate/{user_uuid}/{token}/
