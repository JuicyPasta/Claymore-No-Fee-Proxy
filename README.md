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
_C://Windows/System32/drivers/etc/hosts_

Place this at the end:
```
127.0.0.1   eth-eu.dwarfpool.com
```

## Configure your address
Spot and edit the `worker_name` variable in `stratum_proxy.py` and replace it by yours.

## RUN
Run the proxy daemon first
```
./stratum_proxy.py 127.0.0.1 8008 us1.ethpool.org 3333 False
```

Run the mining software as usual
```
./ethdcrminer64 ....
```


## FAQ

### What if i use other pool?
TODO

### How can i be 100% sure this is not a scam ?
This is an open source projet, so you can read the source code and check it.

### Should i run the proxy on every mining station?
TODO

### Is it compatible with every currency?
TODO

### Is it compatible with dual mode mining?
TODO

## Credit
[JuicyPasta] (https://github.com/JuicyPasta)

