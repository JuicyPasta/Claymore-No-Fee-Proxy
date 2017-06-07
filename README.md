# flakjacket

Removes Claymore's 1-2% mining fee using Stratum Proxy. Tested on Ubuntu 16.04 and Windows 10 with claymore 9.4.

## How it works?
This proxy is placed between Claymore and Internet in order to catch mining fee packet and substituting the devfee address with your wallet address. The changes are done on the fly and do not require stoping or relaunching the mining software.

## Setup

### On Linux
Edit the host file on every mining system.
```
nano /etc/hosts
```
Place this at the end:
```
127.0.0.1   eth-eu.dwarfpool.com
```

### On Windows
Edit the host file as Administrator on every mining system. 
_C:/Windows/System32/drivers/etc/hosts_

Place this at the end:
```
127.0.0.1   eth-eu.dwarfpool.com
```

## Configure your address
Spot and edit the `worker_name` variable in `stratum_proxy.py` and replace it by yours.

## RUN
Run the proxy daemon first
```
./stratum_proxy.py 127.0.0.1 8008 eth-eu.dwarfpool.com 8008 False
```

Run the mining software as usual
```
./ethdcrminer64 ....
```


## FAQ

### What if i use other pool?
Claymore try to mine the fee on the same pool as you. So you have to change the pool server above by yours.

### Is it lightweight?
We try to reduce the footprint to the maximum, the stratum proxy daemon take up to 130MB RAM and few CPU resources.

### How can i be 100% sure this is not a scam ?
This is an open source project, so you can read the source code and check it. BTW, don't hesitate to create pull requests if you see something broken.

### Should i run the proxy on every mining station?
Yes, we recommand to install the proxy on every mining station. If you have a farm consider having a couple of dedicated computer (with good CPU and network).

### Is it compatible with every currency?
This proxy was designed to be used with Claymore ETH version. If you are planning to mine ETH-like, you have to specify `-allpools 1` in claymore and replace the host file with the right pool.

### Is it compatible with dual mode mining?
Yes, the claymore software take the fee from ETH mining only.

### How can I check if it works?
Read the Stratum proxy output. You can also check your pool stats, but some pool ignore small mining time if it did not find a share. But it mines for you !

### Claymore warns me something about local proxy...
Do not worry, Claymore check the pool's IP to avoid local proxies, because it can cause stale shares. In our case, the proxy is on the same computer so the lag is trivial. Personally, I never had any stale shares.

## Credit
[JuicyPasta](https://github.com/JuicyPasta)

