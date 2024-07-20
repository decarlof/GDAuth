=======
Install
=======

This section covers the basics of how to download and install `GDAuth <https://github.com/xray-imaging/GDAuth>`_.

.. contents:: Contents:
   :local:

Installing from source
======================

Install from `Anaconda <https://www.anaconda.com/distribution/>`_ > python3.9

Create and activate a dedicated conda environment::

    (base) $ conda create --name globus python=3.9
    (base) $ conda activate globus
    (globus) $ 

Clone the  `GDAuth <https://github.com/xray-imaging/GDAuth>`_ repository

::

    (globus) $ git clone https://github.com/xray-imaging/GDAuth GDAuth

Install GDAuth::

    (globus) $ cd GDAuth
    (globus) $ pip install .

Install all packages listed in the ``env/requirements.txt`` file::

    (globus) $ conda install numpy
    (globus) $ conda install globus_sdk

Test the installation
=====================

::

    (globus) $ gdauth -h
    usage: gdauth [-h] [--config FILE]  ...

    options:
      -h, --help     show this help message and exit
      --config FILE  File name of configuration

    Commands:
      
        init         Create configuration file
        show         Show all endpoints on the Globus server
        create       Create a folder on the Globus endpoint
        share        Share a Globus endpoint folder with a user email address
        links        Create download links for all items (folder and files) listed in a Globus endpoint folder.


Update
======

**GDAuth** is constantly updated to include new features. To update your locally installed version::

    (globus) $ cd GDAuth
    (globus) $ git pull
    (globus) $ pip install .


Dependencies
============

Install the following package::

    (globus) $ conda install numpy
    (globus) $ conda install globus_sdk



