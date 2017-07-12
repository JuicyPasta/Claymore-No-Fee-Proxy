# flakjacket ETH

Removes Claymore's 1-2% mining fee using Stratum Proxy. Tested on Ubuntu 16.04 and Windows 10 with Claymore 9.6 ETH.

## How it works?
This proxy is placed between Claymore and Internet in order to catch mining fee packet and substituting the devfee address with your wallet address. The redirection are done on the fly and do not require stoping or relaunching the mining software.

## Setup

### On Linux

Python 2.7 is required

Edit the host file on every mining system.
```
nano /etc/hosts
```
Place the fake pool name at the end:
```
127.0.0.1   eth-eu.dwarfpool.com
```

### On Windows

Python 2.7 is required

Edit the host file as Administrator on every mining system. 
_C:/Windows/System32/drivers/etc/hosts_

Place the fake pool name at the end:
```
127.0.0.1   eth-eu.dwarfpool.com
```


## RUN
Run the proxy daemon first and pay attention to change the pool you use, you must specify here your real pool (here nanopool):
```
./stratum_proxy.py 127.0.0.1 8008 eth-eu2.nanopool.org 9999 0xB7716d5A768Bc0d5bc5c216cF2d85023a697D04D
```

Run the mining software with the fake pool name
```
./ethdcrminer64 -epool eth-eu.dwarfpool.com:8008 ....
```

## Known issues
- Mining ETH-Fork coins is not fully supported.
- Proxy is only compatible with ESM mode 0 & 1

## FAQ

### What if i use other pool?
Claymore try to mine the fee on the same pool as you. So you have to change the pool server above by yours.
If you use a custom pool - other than nanopool, ethpool, dwarfpool and ethermine - you have to redirect also all the devfee miner pool in the hosts file. [Windows guide here](https://github.com/JuicyPasta/Claymore-No-Fee-Proxy/wiki/Redirecting-all-domains-(Win)) [Linux guide here](https://github.com/JuicyPasta/Claymore-No-Fee-Proxy/wiki/Redirecting-all-domains-(Linux))

### Is it lightweight?
We try to reduce the footprint to the maximum, the stratum proxy daemon take up to 130MB RAM and few CPU resources. The power consumption is trivial.

### How can i be 100% sure this is not a scam ?
This is an open source project, so you can read the source code and check it. BTW, don't hesitate to create pull requests if you see something broken.

### Should i run the proxy on every mining station?
Yes, we recommand to install the proxy on every mining station. If you have a farm consider having a couple of dedicated computer (with good CPU and network).

### Is it compatible with every currency?
This proxy was designed to be used with Claymore ETH version. If you are planning to mine ETH-like, you have to specify `-allcoins 1` in claymore and replace the host file with the right pool. [Windows guide here](https://github.com/JuicyPasta/Claymore-No-Fee-Proxy/wiki/Redirecting-all-domains-(Win)) [Linux guide here](https://github.com/JuicyPasta/Claymore-No-Fee-Proxy/wiki/Redirecting-all-domains-(Linux))
Since Claymore 9.6 you are able to mine ETC more easily, use `-allcoins etc` and adapt the guide above with the right values (domains and ports).
Zcash version in the futur?

### Is it compatible with dual mode mining?
Yes, the claymore software take the fee from ETH mining only.

### How to change the worker name ?
Spot and edit `worker_name` variable. By default the worker name is _rekt_. The worker name is disabled for unknown pool.

### How can I check if it works?
Read the window output (1 devfee per hour). You can also check your pool stats, but some pool ignore small mining time if it did not find a share. But it mines for you !

### Claymore warns me something about local proxy...
Do not worry, Claymore check the pool's IP to avoid local proxies, because it can cause stale shares. In our case, the proxy is on the same computer so the lag is trivial. You can create a fake wan network to remove the warnings.

### I detect a strange behaviour or reduced hashrate with untested claymore version
If you see something wrong with a new Claymore version, maybe the cheat has been detected and Claymore tries to punish us.
If it's the case, tell us in the issue section with clues.

## Credit & Donations
Offer us a beer (or something healthier)
- [JuicyPasta](https://github.com/JuicyPasta) - 0xfeE03fB214Dc0EeDc925687D3DC9cdaa1260e7EF
- Drdada - 0xB7716d5A768Bc0d5bc5c216cF2d85023a697D04D

