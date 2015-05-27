The Tech Oracle - FingerAuth agent
==================================

 /$$$$$$$$ /$$$$$$$$ /$$$$$$
|__  $$__/|__  $$__//$$__  $$
   | $$      | $$  | $$  \ $$
   | $$      | $$  | $$  | $$
   | $$      | $$  | $$  | $$
   | $$      | $$  | $$  | $$
   | $$      | $$  |  $$$$$$/
   |__/      |__/   \______/


FingerAuth agent
================

Simple script that continuously reads data from a fingerprint reader.

When a fingerprint is detected, it compares to a number of stored fingerprints
in a database. If the fingerprint is not already stored, it will be added to the db.

The script then opens up a browser with a URL-containing the ID of the fingerprint.

## Dependencies

- libfprint

    # aptitude install libfprint0

- pyfprint-cffi

    $ git checkout git@github.com:franciscod/pyfprint-cffi.git


## Usage

Get the full list of cmdline options:

    $ ./FingerAuth.py -h

Once started `FingerAuth` will execute an endless loop, that reads known
fingerprints from a database and then the output of the fingerprint reader.
Unknown fingerprints will be enrolled and stored in the database.

## FingerStore

`FingerAuth` supports the following storage backends:

- local memory (non-persistent; non-networked)

- MongoDB

- MySQL


## Configuration

`FingerAuth` reads a configuration file `FingerAuth.conf`, that uses an INI-style syntax.

- `FingerAuth`
	- `timeout`: timeout for re-opening the browser with the same URL
	- `url`:
	- `urlsuffix`:
	- `fingerstore`: which backend to use for storing fingerprints

- `MongoDB`
  - any keyword supported by `pymongo.MongoClient`
- `MySQL`
  - any keywords supported by `mysql.connector.connect`


You can use cmdline options to override the values from the config-files.
You can put the credentials for your 
