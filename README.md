# Python-smartqq-client
A simple QQ client implemented with python, based on smartqq protocol.

Note: this project is not meant to be used standalone, but rather as component of other projects.
### Prerequisites
This project was developed with python3.5.3, but it might be functional with any python version > 3. Keep in mind that this is not tested.

To run properly, `mongodb`, `requests` and `pymongo` are required.

#### To install `mongodb`:

##### On Debian:
```
$ apt-get install mongodb
```
Make sure you have proper permissions, if you have any problems installing those packages, use `sudo`.
##### On other Operating Systems:
To install MongoDB on other Operating Systems, please refer to [the official installation guide](https://docs.mongodb.com/manual/administration/install-community/)

Type `mongo` in console to check if MongoDB has been installed properly and started up.
#### To install `requests` and `pymongo`:
##### If you plan to install this project through `pip`:
Simply ignore this part since pip will indeed install these packages as dependencies.
##### Otherwise:
```
$ pip3 install requests pymongo
```
will do the job.
### Installing
#### To install through pip:
```
$ pip3 install python-smartqq-client
```
Again, you might want to use `sudo` while doing this.
#### Otherwise:
Simply clone this git repo.
### Usage
Given proper handlers (keep empty for default handlers), the `SmartqqClient` objects then should have their `.run` method wrapped as threads, which enables the objects to send messages while receiving them.