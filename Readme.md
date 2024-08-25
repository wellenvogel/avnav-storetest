Test plugin for AvNav
=====================
Copy to DATADIR/plugins/storetest.

Add 
```
<user-storetest allowKeyOverwrite="True"/>
```

to plugin config.

Listens on udp localhost:9100 , receives lines with

key=value

and writes them directly to the internal store.