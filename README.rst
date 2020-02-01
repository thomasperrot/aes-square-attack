*****************
AES Square Attack
*****************

.. image:: https://img.shields.io/badge/python-3.6+-blue
   :target: https://www.python.org/downloads/release/python-350/
   :alt: Python3.5+ compatible

.. image:: https://travis-ci.com/thomasperrot/aes-square-attack.svg?branch=master
   :target: https://travis-ci.org/thomasperrot/aes-square-attack
   :alt: Continuous Integration Status

.. image:: https://codecov.io/gh/thomasperrot/aes-square-attack/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/thomasperrot/aes-square-attack
   :alt: Coverage Status

.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://github.com/thomasperrot/aes-square-attack/blob/master/LICENSE.rst
   :alt: MIT License

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style black

Homemade implementation of Square Attack against 4 rounds AES

Overview
********

This repository is a simple implementation of the Square Attack against 4 rounds AES, based on this amazing website_
(all credits goes to David Wong). The source code gathers all the functions to encrypt using 128-bit AES algorithm,
and a module dedicated to square attack.

.. warning::

   The source code has absolutely no documentation, as all you need is already provided in the above mention website,
   and documenting is pretty boring.

.. _website: https://www.davidwong.fr/blockbreakers/

Quickstart
**********

This attack is a chosen plaintext attack, so you must find a way to encrypt the initial delta set. To do this, implement
your own function, respecting the following signature:

.. code-block:: python

   def get_encrypted_delta_set(inactive_value: int, *args, **kwargs) -> List[State]:


As an example, the one implemented in this source code is just a homemade AES that encrypts the delta set using a
supplied key.

Once it is done, you can perform the attack using the following functions:

.. code-block:: python

    rounds = 4
    get_encrypted_ds = partial(get_encrypted_delta_set, my_extra_args)
    last_key = crack_last_key(get_encrypted_ds)
    cracked_key = get_first_key(last_key, rounds + 1)
    print(f"[+] Found key: {cracked_key}")
