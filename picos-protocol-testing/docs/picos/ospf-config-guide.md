# PicOS 4.6 OSPF Configuration Guide (Consolidated)

Source: https://pica8-fs.atlassian.net/wiki/spaces/PicOS46/

## 1. OSPF Overview

PicOS supports both OSPFv2 and OSPFv3 with VRF support.

OSPF routers send Hello packets out of all OSPF-enabled interfaces. Two routers sharing a common data link become neighbors if they agree on certain parameters in Hello packets. Some neighbors form adjacencies (virtual point-to-point links) over which routing information is exchanged.

Each OSPF router sends LSAs over all its adjacencies. LSAs describe the router's neighbors, links, and link states. When received, LSAs are added to the link-state database and flooded. All routers run Dijkstra's SPF algorithm to calculate shortest loop-free paths.

## 2. Basic OSPF Configuration Tasks

### 2.1 Configuring OSPF Router ID
```
set protocols ospf router-id <A.B.C.D>
commit
```
NOTE: If the device has established Full-state neighbor relationships, the new router ID will not take effect immediately. Run `run clear ospf process` to apply. This resets neighbor relationships.

### 2.2 Configuring OSPF Areas
```
set protocols ospf area <area-id> area-type <normal|stub|nssa>
```
- Area 0.0.0.0 is backbone (required)
- Supported types: normal, stub, NSSA

### 2.3 Configuring OSPF Interfaces
```
set protocols ospf interface <l3-interface> area <area-id>
```
L3 interface can be: VLAN interface, loopback interface, routed interface, or sub-interface.

Alternative network-based method:
```
set protocols ospf network <prefix/len> area <area-id>
```

### 2.4 Additional OSPF Parameters
```
set protocols ospf interface <intf> hello-interval <seconds>
set protocols ospf interface <intf> cost <value>
set protocols ospf interface <intf> dead-interval <seconds>
```

### 2.5 Enabling IP Routing
```
set ip routing enable true
```

### 2.6 VLAN Interface Setup (prerequisite)
```
set vlans vlan-id <id> l3-interface <vlan-name>
set interface gigabit-ethernet <port> family ethernet-switching native-vlan-id <id>
set l3-interface vlan-interface <vlan-name> address <ip> prefix-length <mask>
```

### 2.7 Loopback Interface
```
set l3-interface loopback lo address <ip> prefix-length 32
```

## 3. OSPF Area Types

### 3.1 Standard/Normal Area
Default area type. Accepts all LSA types.

### 3.2 Stub Area
External routes (Type-5 LSAs) are not advertised. A default route 0.0.0.0 is injected.
```
set protocols ospf area <area-id> area-type stub
```

### 3.3 Totally Stubby Area
Neither external nor inter-area routes are injected. Only a default route.
```
set protocols ospf area <area-id> area-type stub
set protocols ospf area <area-id> no-summary
```

### 3.4 NSSA (Not-So-Stubby Area)
External routes can be imported via Type-7 LSAs but Type-5 LSAs are blocked.
```
set protocols ospf area <area-id> area-type nssa
```

### 3.5 Totally NSSA
```
set protocols ospf area <area-id> area-type nssa
set protocols ospf area <area-id> no-summary
```

## 4. OSPF Route Redistribution and Route Maps

### 4.1 Redistribution Types
PicOS can redistribute: BGP, Connected, Kernel, Static, Table routes into OSPF.
```
set protocols ospf redistribute <bgp|connected|kernel|static|table>
set protocols ospf redistribute <type> metric <value>
set protocols ospf redistribute <type> route-map "<map-name>"
```

### 4.2 Route Maps and Prefix Lists
```
set routing prefix-list IPv4 <list-name> permit prefix <prefix/len>
set routing route-map <map-name> order <seq> matching-policy "permit"
set routing route-map <map-name> order <seq> match ip address prefix-list "<list-name>"
set protocols ospf redistribute connected route-map "<map-name>"
```

## 5. OSPF Route Summarization
```
set protocols ospf area <area-id> range <prefix/len>
```

## 6. OSPF Graceful Restart (GR)

### 6.1 Overview
Allows OSPF process to restart without impacting data forwarding. Uses Type 9 Opaque LSAs.

### 6.2 Configuring Restarting Router
```
set protocols ospf capability opaque
set protocols ospf graceful-restart enable true
set protocols ospf grace-period <seconds>    # default 120
run graceful-restart prepare ospf
commit
```

### 6.3 Configuring Helper Router
```
set protocols ospf capability opaque
set protocols ospf graceful-restart helper enable true
set protocols ospf graceful-restart helper planned-only           # optional
set protocols ospf graceful-restart helper strict-lsa-checking enable true  # optional
set protocols ospf graceful-restart helper supported-grace-time <seconds>   # optional
commit
```

### 6.4 Triggering Restart
```
root@Switch# pkill ospfd
```
The system automatically restarts the OSPF process.

### 6.5 Verification
```
run show ospf graceful-restart helper detail
run show ospf neighbor
```

## 7. OSPF Multi-Instance Support
PicOS supports running multiple OSPF instances.
```
set protocols ospf instance-id <id> router-id <A.B.C.D>
```

## 8. OSPFv3 (IPv6)
```
set protocols ospf6 router-id <A.B.C.D>
set protocols ospf6 area <area-id> interface <intf>
```

## 9. OSPF with VRF
```
set protocols ospf vrf <vrf-name> router-id <A.B.C.D>
set protocols ospf vrf <vrf-name> network <prefix/len> area <area-id>
```

## 10. Verification Commands
```
run show ospf neighbor
run show ospf database
run show ospf interface
run show ospf route
run show route ipv4
run show ospf graceful-restart helper detail
run clear ospf process
```

## 11. PicOS OSPF Supported Features Summary
- OSPFv2 and OSPFv3
- Area types: Normal, Stub, Totally Stubby, NSSA, Totally NSSA
- Route redistribution (BGP, Connected, Kernel, Static, Table)
- Route maps and prefix lists
- Route summarization (area range)
- Graceful Restart (restarting device + helper mode)
- Multi-instance
- VRF support
- BFD for OSPF
- MD5 authentication
- Passive interfaces
- Interface cost, hello-interval, dead-interval
