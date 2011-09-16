Django Tinycart
===============

Django Tinycart is a simple cart application for a Django powered site,
inspired by django-shop (but without products, orders, payments and shipping).

Features
--------

- Cart can be stored in session for anonymous users or binded with user for
  authenticated users.
- Support for price modifiers for cart and cart items (e.g., for discounts or
  taxes).

Installation
------------

1. ``pip install git://github.com/trilan/django-tinycart.git#egg=django-tinycart``
2. Add ``'tinycart'`` to your ``INSTALLED_APPS`` setting.
3. Add ``'tinycart.middleware.CartMiddleware'`` to ``MIDDLEWARE_CLASSES``.
4. Add ``'tinycart.context_processors.cart'`` to
   ``TEMPLATE_CONTEXT_PROCESSORS``.
3. Add app urls to your project URLConf::

    url(r'^cart/', include('tinycart.urls'))

Contributing
------------

Feel free to fork, send pull requests or report bugs and issues on github.
