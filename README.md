# HoneySpot
*Spotting Honeypots to make them better*

## Introduction

HoneySpot is an open-source tool written in Python 2.7 that aims to detect various (for now) low and medium interaction honeypot, by employing various techniques. The tool started out as weekend project of finding problems in existing honeypots by reading Github issues. We already have anti-VM/anti-Sandbox malware out in the wild, how long before also see a malware with anti-honeypot techniques too? (I am not aware of any existing ones)

The tool provides plugin/modules based architechure, where any user can write detection for a new honeypot and just put the Python script in "modules" directory.

This tool can be seen as [*Pafish for Honeypots*](https://github.com/a0rtega/pafish), in fact it is inspired by Pafish too.

## Motivation

The goal of the project is find issues with your existing honeypot installation. These issues then can be fixed to make honeypots less fingerprint-prone (or too obvious). The tool is not supposed to be a tool to defeat honeypots, on the contrary, it should be used in adjunction with other honeypots and tools.

The author is aware that it is impossible to make a low/medium interaction honeypot undetectable, however, the goal should be to waste more and more of attackers' time. HoneySpot could be used to detect those obvious issues and configure a robust honeypot

## Supported Honeypots

As of now, HoneySpot can detect following honeypots:

* Cowrie
* Glastopf
* GasPot

Support coming soon for:
* HoneyPy (various plugins)
* ElasticHoney
* *You tell us*

## Using HoneySpot

Before starting to use HoneySpot, please install the Python libraries needed. To install the same, run:
```bash
pip install -r requirements.txt
```

Using HoneySpot is fairly easy. Run following command to see help:
```bash
python honeyspot.py
```

To check out available modules/plugins, run:
```bash
python honeyspot.py -ls
```
To run HoneySpot against a target, you need to specify following parameters:
* Host
* Port (Modules have default port in case you skip)
* Module to run (see above to list modules)

An example command to run HoneySpot against a Cowrie/Kippo instance would be:
```bash
python honeyspot.py --host 127.0.0.1 --port 2222 --module cowrie_kippo
```


## License

This tool is licensed under [The Beerware License](https://en.wikipedia.org/wiki/Beerware).

## Reporting bugs/ contributing
Feel free to report bugs using Github issues and send pull requests if you add anything new. Any and all help is appreciated.
