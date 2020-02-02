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

The source code has absolutely no documentation, as all you need is already provided in the above mention website,
and documenting is pretty boring.

.. _website: https://www.davidwong.fr/blockbreakers/

Quickstart
**********

To install the package:

.. code-block:: bash

   pip install .


This attack is a chosen plaintext attack, so you must find a way to encrypt the initial delta set. To do this, implement
your own function, respecting the following signature:

.. code-block:: python

   from typing import Iterable, List
   from aes.common import State

   def encrypt_delta_set(delta_set: Iterable[State]) -> List[State]:
       ...


As an example, the one implemented in this source code is just a homemade AES that encrypts the delta set using a
supplied key. Use `functools.partial` if you need extra arguments (see `tests/functional/test_crack_key.py`).

Once it is done, you can perform the attack using the following snippet:

.. code-block:: python

    import binascii
    from functools import partial

    from aes.square import crack_key

    def encrypt_delta_set(delta_set: Iterable[State]) -> List[State]:
        ...

    cracked_key = crack_key(encrypt_delta_set)
    print(f"[+] Found key: {binascii.hexlify(cracked_key)}")


Issues
******

If you encounter an issue, please fill free to open an issue_.

.. _issue: https://github.com/thomasperrot/aes-square-attack/issues
