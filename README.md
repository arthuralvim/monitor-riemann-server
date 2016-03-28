# monitor-riemann-server

Ansible playbooks for launching servers to be monitored with Riemann.

We will make the provision of 2 Ubuntu machine with this tools:

* [Riemann](http://riemann.io/)
* [Grafana](http://grafana.org)
* [InfluxDB](https://influxdata.com/)


## Architecture

1. Riemann Server, Riemann Dashboard and Grafana. (ssh root@33.33.33.30)
2. InfluxDB (ssh root@33.33.33.31)

## Installation


### Install Ansible

```bash
$ pip install -r requirements.txt
```

### Install Vagrant and an Ubuntu Box

```bash
$ sudo apt-get install virtualbox
$ sudo apt-get install vagrant
$ sudo apt-get install virtualbox-dkms
$ vagrant box add ubuntu/trusty64 https://atlas.hashicorp.com/ubuntu/boxes/trusty64
```

### Deploy Vagrant Machines

```bash
$ vagrant up
```

### Deploy all acording to your hosts.

```bash
$ play dev (WIP)
```

---

### Deploy InfluxDB

```bash
$ play dev servers-db
$ open http://33.33.33.31:8083
```

_Authentication needed: username: admin password: admin_

### Deploy Riemann Server

```bash
$ play dev servers-reimann
$ open http://33.33.33.30:4567
```

### Deploy Grafana

```bash
$ play dev servers-reimann -t grafana
$ open http://33.33.33.30:3000
```
_Authentication needed: username: grafana password: grafana_

### Deploy Riemann Client

```bash
$ play dev servers-reimann -t riemann-client (WIP)
```

## License

MIT
