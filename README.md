metahosting-status-updater
==========================

[![Build Status](https://travis-ci.org/BeneDicere/metahosting-status-updater.svg?branch=master)](https://travis-ci.org/BeneDicere/metahosting-status-updater)

Component that is launched to move metahosting-worker-status messages to a database,
where a GUI then could create a view from.

Start:
```
docker run -d --link messaging:messaging --link db:db BeneDicere/metahosting-status-updater
```
