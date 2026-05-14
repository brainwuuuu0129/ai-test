# PicOS 4.6 OSPF CLI Quick Reference

## Configuration Commands

### Router ID
```
set protocols ospf router-id <A.B.C.D>
```

### Area Configuration
```
set protocols ospf area <area-id>
set protocols ospf area <area-id> area-type <normal|stub|nssa>
set protocols ospf area <area-id> no-summary
set protocols ospf area <area-id> range <prefix/len>
```

### Interface Assignment
```
set protocols ospf interface <l3-intf> area <area-id>
set protocols ospf network <prefix/len> area <area-id>
```

### Interface Parameters
```
set protocols ospf interface <l3-intf> hello-interval <seconds>
set protocols ospf interface <l3-intf> dead-interval <seconds>
set protocols ospf interface <l3-intf> cost <value>
set protocols ospf interface <l3-intf> passive
```

### Authentication
```
set protocols ospf interface <l3-intf> authentication message-digest
set protocols ospf interface <l3-intf> message-digest-key <id> md5 <key>
```

### Route Redistribution
```
set protocols ospf redistribute <bgp|connected|kernel|static|table>
set protocols ospf redistribute <type> metric <value>
set protocols ospf redistribute <type> route-map "<map-name>"
```

### Route Maps & Prefix Lists
```
set routing prefix-list IPv4 <list-name> permit prefix <prefix/len>
set routing route-map <map-name> order <seq> matching-policy "permit"
set routing route-map <map-name> order <seq> match ip address prefix-list "<list-name>"
```

### Graceful Restart (Restarting Router)
```
set protocols ospf capability opaque
set protocols ospf graceful-restart enable true
set protocols ospf grace-period <seconds>
run graceful-restart prepare ospf
```

### Graceful Restart (Helper)
```
set protocols ospf capability opaque
set protocols ospf graceful-restart helper enable true
set protocols ospf graceful-restart helper planned-only
set protocols ospf graceful-restart helper strict-lsa-checking enable true
set protocols ospf graceful-restart helper supported-grace-time <seconds>
```

### Multi-Instance
```
set protocols ospf instance-id <id> router-id <A.B.C.D>
```

### VRF
```
set protocols ospf vrf <vrf-name> router-id <A.B.C.D>
set protocols ospf vrf <vrf-name> network <prefix/len> area <area-id>
```

### OSPFv3
```
set protocols ospf6 router-id <A.B.C.D>
set protocols ospf6 area <area-id> interface <intf>
```

### BFD for OSPF
```
set protocols ospf interface <l3-intf> bfd
```

## Prerequisite Commands

### VLAN Interface Setup
```
set vlans vlan-id <id> l3-interface <vlan-name>
set interface gigabit-ethernet <port> family ethernet-switching native-vlan-id <id>
set l3-interface vlan-interface <vlan-name> address <ip> prefix-length <mask>
```

### Loopback
```
set l3-interface loopback lo address <ip> prefix-length 32
```

### Enable Routing
```
set ip routing enable true
```

### Commit
```
commit
```

## Verification (Show) Commands

```
run show ospf neighbor
run show ospf database
run show ospf interface
run show ospf route
run show route ipv4
run show ospf graceful-restart helper [detail]
run show ospf border-routers
```

## Operational Commands

```
run clear ospf process
run graceful-restart prepare ospf
```
