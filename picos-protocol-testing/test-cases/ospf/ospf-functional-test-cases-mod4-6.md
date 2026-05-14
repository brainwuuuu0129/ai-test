# PicOS 4.6 OSPF Functional Test Cases — Modules 4, 5, 6

**Platform**: PicOS 4.6  
**RFC Reference**: RFC 2328 (OSPFv2), RFC 3623 (Graceful Restart)  
**Generated**: 2026-03-17  

---

## Table of Contents

- 1.4 [SPF Calculation & Route Learning (MODULE 4)](#14-spf-calculation--route-learning-module-4)
  - 1.4.1 [Basic Route Learning & Path Selection](#141-basic-route-learning--path-selection)
    - 1.4.1.1 [MOD4-01: Basic intra-area route learning](#1411-verify-basic-intra-area-route-learning-via-ospf)
    - 1.4.1.2 [MOD4-02: Cost-based shortest path](#1412-verify-cost-based-shortest-path-selection)
    - 1.4.1.3 [MOD4-03: ECMP](#1413-verify-equal-cost-multipath-ecmp-routing)
  - 1.4.2 [Route Convergence & SPF Recalculation](#142-route-convergence--spf-recalculation)
    - 1.4.2.1 [MOD4-04: Route convergence after link failure](#1421-verify-route-convergence-after-link-failure)
    - 1.4.2.2 [MOD4-07: SPF recalculation after cost change](#1422-verify-spf-recalculation-after-cost-change)
  - 1.4.3 [Inter-Area & External Routes](#143-inter-area--external-routes)
    - 1.4.3.1 [MOD4-05: Inter-area route learning via ABR](#1431-verify-inter-area-route-learning-via-abr)
    - 1.4.3.2 [MOD4-06: Route summarization using area range](#1432-verify-route-summarization-using-area-range)
    - 1.4.3.3 [MOD4-08: External route learning via redistribution](#1433-verify-external-route-learning-via-redistribution)
  - 1.4.4 [Route Withdrawal & Filtering](#144-route-withdrawal--filtering)
    - 1.4.4.1 [MOD4-09: Route withdrawal after network removal](#1441-verify-route-withdrawal-after-network-removal)
    - 1.4.4.2 [MOD4-10: Redistributed route filtered by route-map](#1442-verify-redistributed-route-filtered-by-route-map)
- 1.5 [Graceful Restart (MODULE 5)](#15-graceful-restart-module-5)
  - 1.5.1 [Planned & Unplanned Restart](#151-planned--unplanned-restart)
    - 1.5.1.1 [MOD5-01: Planned restart](#1511-verify-planned-graceful-restart-restarting-router)
    - 1.5.1.2 [MOD5-02: Unplanned restart](#1512-verify-unplanned-graceful-restart-behavior)
    - 1.5.1.3 [MOD5-07: Planned restart with route preservation](#1513-verify-planned-graceful-restart-with-route-preservation)
  - 1.5.2 [Helper Mode Behavior](#152-helper-mode-behavior)
    - 1.5.2.1 [MOD5-03: Helper planned-only](#1521-verify-helper-mode-rejects-unplanned-restart-with-planned-only)
    - 1.5.2.2 [MOD5-05: Strict LSA checking](#1522-verify-strict-lsa-checking-exits-helper-mode-on-topology-change)
    - 1.5.2.3 [MOD5-06: Supported-grace-time exceeded](#1523-verify-helper-rejects-grace-period-exceeding-supported-grace-time)
  - 1.5.3 [Grace Period](#153-grace-period)
    - 1.5.3.1 [MOD5-04: Grace-period timeout](#1531-verify-grace-period-timeout-exits-helper-mode)
- 1.6 [OSPF Interface Parameters & Authentication (MODULE 6)](#16-ospf-interface-parameters--authentication-module-6)
  - 1.6.1 [Timer Parameters](#161-timer-parameters)
    - 1.6.1.1 [MOD6-01: Hello-interval configuration](#1611-verify-hello-interval-configuration-and-neighbor-formation)
    - 1.6.1.2 [MOD6-02: Hello-interval mismatch](#1612-verify-hello-interval-mismatch-prevents-adjacency)
    - 1.6.1.3 [MOD6-07: Dead-interval timeout](#1613-verify-dead-interval-timeout-declares-neighbor-down)
  - 1.6.2 [Interface Cost & Passive](#162-interface-cost--passive)
    - 1.6.2.1 [MOD6-03: Interface cost affects route selection](#1621-verify-interface-cost-affects-route-selection)
    - 1.6.2.2 [MOD6-04: Passive interface](#1622-verify-passive-interface-suppresses-hello-packets)
  - 1.6.3 [Authentication](#163-authentication)
    - 1.6.3.1 [MOD6-05: MD5 matching keys](#1631-verify-md5-authentication-with-matching-keys)
    - 1.6.3.2 [MOD6-06: MD5 key mismatch](#1632-verify-md5-authentication-key-mismatch-prevents-adjacency)
  - 1.6.4 [Fast Failure Detection](#164-fast-failure-detection)
    - 1.6.4.1 [MOD6-08: BFD for OSPF](#1641-verify-bfd-for-ospf-fast-failure-detection)
- [Coverage Summary](#coverage-summary)

---

## 1.4 SPF Calculation & Route Learning (MODULE 4)

**RFC 2328 Sections**: 2.2 (The Shortest-Path Tree), 11 (The Routing Table Structure), 16 (Calculation of the Routing Table)  
**Priority**: P0  
**Minimum Cases**: 8  

---

### 1.4.1 Basic Route Learning & Path Selection

##### 1.4.1.1 Verify basic intra-area route learning via OSPF

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-01: Basic Intra-Area Route Learning via OSPF |
| **Purpose Of The Test** | Verify that a router learns intra-area routes from a directly connected OSPF neighbor via SPF calculation, per RFC 2328 Section 16.1. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`    lo: 1.1.1.1                      lo: 2.2.2.2`<br>`                                    (vlan200: 192.168.1.1/24) --- Stub Network`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration on either device<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 192.168.1.1 prefix-length 24`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with OSPF area 0 on vlan100 and loopback<br>2. Configure DUT-B with OSPF area 0 on vlan100, loopback, and vlan200 (192.168.1.0/24)<br>3. Wait 40 seconds for OSPF adjacency to reach Full state<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf route` on DUT-A<br>6. Execute `run show route ipv4` on DUT-A |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows neighbor 2.2.2.2 in Full state<br>2. `run show ospf route` on DUT-A contains route 192.168.1.0/24 as an intra-area (O) route via 10.0.12.2<br>3. `run show ospf route` on DUT-A contains route 2.2.2.2/32 as an intra-area (O) route<br>4. `run show route ipv4` on DUT-A contains OSPF-learned route 192.168.1.0/24 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.1 |

---

##### 1.4.1.2 Verify cost-based shortest path selection

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-02: Cost-Based Shortest Path Selection |
| **Purpose Of The Test** | Verify that SPF calculation selects the lowest-cost path when two paths exist to the same destination, per RFC 2328 Section 16.1. |
| **Test Topo & Precondition** | **Topology:**<br>`                  vlan100 (cost 10)`<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    |  lo: 1.1.1.1          lo: 2.2.2.2  |`<br>`    |                                     |`<br>`  vlan200 (cost 100)                   vlan300`<br>`  (10.0.13.1)                        (10.0.23.2)`<br>`    |                                     |`<br>`    +---- (10.0.13.2) DUT-C (10.0.23.1) -+`<br>`              lo: 3.3.3.3`<br>`              (172.16.1.0/24 stub)`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a triangle topology<br>2. All links operational at Layer 2<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 100`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.1 prefix-length 24`<br>`set vlans vlan-id 400 l3-interface vlan400`<br>`set l3-interface vlan-interface vlan400 address 172.16.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 100`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface vlan400 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with cost 10 on vlan100 (to DUT-B) and cost 100 on vlan200 (to DUT-C)<br>2. Configure DUT-B with cost 10 on vlan100 and cost 10 on vlan300<br>3. Configure DUT-C with cost 100 on vlan200 and cost 10 on vlan300, plus stub network 172.16.1.0/24<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf route` on DUT-A |
| **Expected Results** | 1. DUT-A's route to 172.16.1.0/24 uses next-hop 10.0.12.2 (via DUT-B) with total cost 30 (10+10+10)<br>2. DUT-A does NOT route 172.16.1.0/24 via the direct path to DUT-C (cost 100+10 = 110)<br>3. `run show ospf route` on DUT-A shows 172.16.1.0/24 with next-hop 10.0.12.2 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.1 |

---

##### 1.4.1.3 Verify equal-cost multipath (ECMP) routing

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-03: Equal-Cost Multipath (ECMP) |
| **Purpose Of The Test** | Verify that when two equal-cost paths exist to a destination, both are installed in the routing table as ECMP routes, per RFC 2328 Section 16. |
| **Test Topo & Precondition** | **Topology:**<br>`                  vlan100 (cost 10)`<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    |  lo: 1.1.1.1          lo: 2.2.2.2  |`<br>`    |                                     |`<br>`  vlan200 (cost 10)                    vlan300 (cost 10)`<br>`  (10.0.13.1)                        (10.0.23.2)`<br>`    |                                     |`<br>`    +---- (10.0.13.2) DUT-C (10.0.23.1) -+`<br>`              lo: 3.3.3.3`<br>`              (172.16.1.0/24 stub)`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a triangle topology<br>2. All links operational at Layer 2<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 10`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.1 prefix-length 24`<br>`set vlans vlan-id 400 l3-interface vlan400`<br>`set l3-interface vlan-interface vlan400 address 172.16.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 10`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface vlan400 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure all three DUTs with OSPF cost 10 on all inter-switch links<br>2. Configure DUT-C with stub network 172.16.1.0/24<br>3. Wait 40 seconds for all adjacencies to reach Full state<br>4. Execute `run show ospf route` on DUT-A<br>5. Execute `run show route ipv4` on DUT-A |
| **Expected Results** | 1. `run show ospf route` on DUT-A shows 172.16.1.0/24 with two next-hops: 10.0.12.2 (via DUT-B) and 10.0.13.2 (via DUT-C)<br>2. Both paths have equal cost of 20 (10+10)<br>3. `run show route ipv4` on DUT-A shows 172.16.1.0/24 as OSPF route with two ECMP next-hops |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.1 |

---

### 1.4.2 Route Convergence & SPF Recalculation

##### 1.4.2.1 Verify route convergence after link failure

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-04: Route Convergence After Link Failure |
| **Purpose Of The Test** | Verify that SPF is recalculated and routes converge to an alternate path after a link failure, per RFC 2328 Section 16. |
| **Test Topo & Precondition** | **Topology:**<br>`                  vlan100 (cost 10)`<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    |  lo: 1.1.1.1          lo: 2.2.2.2  |`<br>`    |                                     |`<br>`  vlan200 (cost 50)                    vlan300 (cost 10)`<br>`  (10.0.13.1)                        (10.0.23.2)`<br>`    |                                     |`<br>`    +---- (10.0.13.2) DUT-C (10.0.23.1) -+`<br>`              lo: 3.3.3.3`<br>`              (172.16.1.0/24 stub)`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a triangle topology<br>2. All adjacencies in Full state<br>3. DUT-A reaches 172.16.1.0/24 via DUT-B (cost 30) as primary path<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 50`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.1 prefix-length 24`<br>`set vlans vlan-id 400 l3-interface vlan400`<br>`set l3-interface vlan-interface vlan400 address 172.16.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 50`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface vlan400 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure all three DUTs as specified (DUT-A→DUT-B cost 10, DUT-A→DUT-C cost 50, DUT-B→DUT-C cost 10)<br>2. Wait 40 seconds for all adjacencies to reach Full state<br>3. Execute `run show ospf route` on DUT-A<br>4. Shutdown ge-1/1/1 on DUT-A (link to DUT-B)<br>5. Wait 45 seconds for dead-interval expiry and SPF recalculation<br>6. Execute `run show ospf route` on DUT-A<br>7. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. Before link failure: `run show ospf route` on DUT-A shows 172.16.1.0/24 via next-hop 10.0.12.2 (cost 30)<br>2. After link failure: DUT-A's neighbor 2.2.2.2 is no longer present in `run show ospf neighbor`<br>3. After convergence: `run show ospf route` on DUT-A shows 172.16.1.0/24 via next-hop 10.0.13.2 (cost 60)<br>4. Route to DUT-C's stub network is reachable through the backup path |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.1, 16.3 |

---

##### 1.4.2.2 Verify SPF recalculation after cost change

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-07: SPF Recalculation After Cost Change |
| **Purpose Of The Test** | Verify that changing the OSPF interface cost triggers SPF recalculation and updates the routing table to reflect the new shortest path, per RFC 2328 Section 16.1. |
| **Test Topo & Precondition** | **Topology:**<br>`                  vlan100 (cost 10 → 200)`<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    |  lo: 1.1.1.1          lo: 2.2.2.2  |`<br>`    |                                     |`<br>`  vlan200 (cost 50)                    vlan300 (cost 10)`<br>`  (10.0.13.1)                        (10.0.23.2)`<br>`    |                                     |`<br>`    +---- (10.0.13.2) DUT-C (10.0.23.1) -+`<br>`              lo: 3.3.3.3`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a triangle topology<br>2. All adjacencies in Full state<br>3. DUT-A reaches DUT-C's loopback via DUT-B (cost 10+10+10=30 < cost 50+10=60)<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 50`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (same as MOD4-04):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C (same as MOD4-04):<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.1 prefix-length 24`<br>`set vlans vlan-id 400 l3-interface vlan400`<br>`set l3-interface vlan-interface vlan400 address 172.16.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 50`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface vlan400 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure triangle topology with DUT-A→DUT-B cost 10, DUT-A→DUT-C cost 50<br>2. Wait 40 seconds for Full adjacencies<br>3. Execute `run show ospf route` on DUT-A<br>4. Configure DUT-A interface vlan100 cost to 200 (`set protocols ospf interface vlan100 cost 200` then `commit`)<br>5. Wait 10 seconds for SPF recalculation<br>6. Execute `run show ospf route` on DUT-A |
| **Expected Results** | 1. Before cost change: `run show ospf route` on DUT-A shows 3.3.3.3/32 via next-hop 10.0.12.2 (cost 30)<br>2. After cost change: `run show ospf route` on DUT-A shows 3.3.3.3/32 via next-hop 10.0.13.2 (cost 60, because 200+10+10=220 > 50+10=60)<br>3. `run show ospf interface` on DUT-A shows vlan100 with cost 200 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.1 |

---

### 1.4.3 Inter-Area & External Routes

##### 1.4.3.1 Verify inter-area route learning via ABR

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-05: Inter-Area Route Learning via ABR |
| **Purpose Of The Test** | Verify that an ABR correctly propagates inter-area (Type-3 Summary LSA) routes between Area 0 and a non-backbone area, per RFC 2328 Section 16.2. |
| **Test Topo & Precondition** | **Topology:**<br>`  Area 1                        Area 0`<br>`  DUT-A (10.0.1.1) ---- (10.0.1.2) DUT-B (ABR) (10.0.2.1) ---- (10.0.2.2) DUT-C`<br>`    lo: 1.1.1.1              lo: 2.2.2.2                          lo: 3.3.3.3`<br>`  (192.168.10.0/24)                                            (172.16.10.0/24)`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. DUT-B acts as ABR between Area 1 and Area 0<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 192.168.10.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface vlan200 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`commit`<br><br>DUT-B (ABR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.2.2 prefix-length 24`<br>`set vlans vlan-id 400 l3-interface vlan400`<br>`set l3-interface vlan-interface vlan400 address 172.16.10.1 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan400 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A in OSPF Area 1 with stub network 192.168.10.0/24<br>2. Configure DUT-B as ABR with interfaces in both Area 1 and Area 0<br>3. Configure DUT-C in OSPF Area 0 with stub network 172.16.10.0/24<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf route` on DUT-A<br>6. Execute `run show ospf route` on DUT-C<br>7. Execute `run show ospf database` on DUT-B |
| **Expected Results** | 1. DUT-A's `run show ospf route` shows 172.16.10.0/24 as an inter-area (IA) route via next-hop 10.0.1.2<br>2. DUT-C's `run show ospf route` shows 192.168.10.0/24 as an inter-area (IA) route via next-hop 10.0.2.1<br>3. DUT-B's `run show ospf database` contains Type-3 Summary LSAs for both 192.168.10.0/24 and 172.16.10.0/24<br>4. DUT-B is identified as an ABR in its Router LSA |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.2 |

---

##### 1.4.3.2 Verify route summarization using area range

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-06: Route Summarization Using Area Range |
| **Purpose Of The Test** | Verify that an ABR summarizes intra-area routes into a single inter-area summary when area range is configured, per RFC 2328 Section 11. |
| **Test Topo & Precondition** | **Topology:**<br>`  Area 1                                     Area 0`<br>`  DUT-A ---- DUT-B (ABR) ---- DUT-C`<br>`  lo: 1.1.1.1   lo: 2.2.2.2     lo: 3.3.3.3`<br>`  `<br>`  Area 1 networks:`<br>`  - 10.10.1.0/24 (DUT-A vlan200)`<br>`  - 10.10.2.0/24 (DUT-A vlan300)`<br>`  - 10.10.3.0/24 (DUT-A vlan400)`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches; DUT-B is ABR<br>2. DUT-A has three subnets in Area 1 within the 10.10.0.0/16 range<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 10.10.1.1 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set l3-interface vlan-interface vlan300 address 10.10.2.1 prefix-length 24`<br>`set vlans vlan-id 400 l3-interface vlan400`<br>`set l3-interface vlan-interface vlan400 address 10.10.3.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface vlan200 area 0.0.0.1`<br>`set protocols ospf interface vlan300 area 0.0.0.1`<br>`set protocols ospf interface vlan400 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`commit`<br><br>DUT-B (ABR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 500 l3-interface vlan500`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 500`<br>`set l3-interface vlan-interface vlan500 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.1 range 10.10.0.0/16`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan500 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 500 l3-interface vlan500`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 500`<br>`set l3-interface vlan-interface vlan500 address 10.0.2.2 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan500 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with three subnets (10.10.1.0/24, 10.10.2.0/24, 10.10.3.0/24) in Area 1<br>2. Configure DUT-B as ABR with `area 0.0.0.1 range 10.10.0.0/16`<br>3. Configure DUT-C in Area 0<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf route` on DUT-C<br>6. Execute `run show ospf database` on DUT-C |
| **Expected Results** | 1. `run show ospf route` on DUT-C shows a single summary route 10.10.0.0/16 as an inter-area (IA) route<br>2. DUT-C does NOT have individual routes for 10.10.1.0/24, 10.10.2.0/24, or 10.10.3.0/24<br>3. `run show ospf database` on DUT-C contains one Type-3 Summary LSA for 10.10.0.0/16 originated by 2.2.2.2 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 11 |

---

##### 1.4.3.3 Verify external route learning via redistribution

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-08: External Route Learning via Redistribution |
| **Purpose Of The Test** | Verify that external routes redistributed into OSPF are learned by other routers as Type-5 External LSAs, per RFC 2328 Section 16.4. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B (ASBR)`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`                              static route: 203.0.113.0/24`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. DUT-B has a static route 203.0.113.0/24 configured<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (ASBR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static`<br>`set protocols ospf redistribute static metric 100`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A in OSPF Area 0<br>2. Configure DUT-B in OSPF Area 0 with `redistribute static metric 100`<br>3. Wait 40 seconds for adjacency to reach Full state<br>4. Execute `run show ospf route` on DUT-A<br>5. Execute `run show ospf database` on DUT-A |
| **Expected Results** | 1. `run show ospf route` on DUT-A shows 203.0.113.0/24 as an external (E2) route via next-hop 10.0.12.2 with metric 100<br>2. `run show ospf database` on DUT-A contains a Type-5 AS-External LSA for 203.0.113.0/24 originated by 2.2.2.2<br>3. `run show route ipv4` on DUT-A lists 203.0.113.0/24 as an OSPF external route |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.4 |

---

### 1.4.4 Route Withdrawal & Filtering

##### 1.4.4.1 Verify route withdrawal after network removal

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-09: Route Withdrawal After Network Removal |
| **Purpose Of The Test** | Verify that when a network is removed from OSPF, the corresponding route is withdrawn from remote routers after SPF recalculation, per RFC 2328 Section 16. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`                              (vlan200: 192.168.50.1/24) --- Stub Network`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Both in Full adjacency state<br>3. DUT-A has learned 192.168.50.0/24 from DUT-B<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 192.168.50.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure both DUTs with OSPF in Area 0; DUT-B advertises vlan200 (192.168.50.0/24)<br>2. Wait 40 seconds for adjacency to reach Full state<br>3. Execute `run show ospf route` on DUT-A<br>4. Configure DUT-B: `delete protocols ospf interface vlan200` then `commit`<br>5. Wait 10 seconds for LSA update and SPF recalculation<br>6. Execute `run show ospf route` on DUT-A |
| **Expected Results** | 1. Before removal: `run show ospf route` on DUT-A contains 192.168.50.0/24 as intra-area route<br>2. After removal: `run show ospf route` on DUT-A no longer contains 192.168.50.0/24<br>3. `run show ospf database` on DUT-A shows updated Router LSA from 2.2.2.2 without the 192.168.50.0/24 link |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16 |

---

##### 1.4.4.2 Verify redistributed route filtered by route-map

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-10: Redistributed Route Filtered by Route-Map |
| **Purpose Of The Test** | Verify that route-map filters applied to OSPF redistribution correctly control which external routes are advertised, per RFC 2328 Section 16.4. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B (ASBR)`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`                              static: 203.0.113.0/24 (permitted)`<br>`                              static: 198.51.100.0/24 (denied)`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. DUT-B has two static routes: 203.0.113.0/24 and 198.51.100.0/24<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (ASBR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set routing prefix-list IPv4 ALLOWED permit prefix 203.0.113.0/24`<br>`set routing route-map OSPF-FILTER order 10 matching-policy "permit"`<br>`set routing route-map OSPF-FILTER order 10 match ip address prefix-list "ALLOWED"`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static route-map "OSPF-FILTER"`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-B with prefix-list permitting only 203.0.113.0/24 and route-map "OSPF-FILTER"<br>2. Configure DUT-B to redistribute static routes with route-map "OSPF-FILTER"<br>3. Wait 40 seconds for adjacency to reach Full state<br>4. Execute `run show ospf route` on DUT-A<br>5. Execute `run show ospf database` on DUT-A |
| **Expected Results** | 1. `run show ospf route` on DUT-A contains 203.0.113.0/24 as an external route<br>2. `run show ospf route` on DUT-A does NOT contain 198.51.100.0/24<br>3. `run show ospf database` on DUT-A contains a Type-5 LSA for 203.0.113.0/24 only |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.4 |

---

## 1.5 Graceful Restart (MODULE 5)

**RFC Reference**: RFC 3623 (Graceful OSPF Restart) + PicOS Implementation  
**Priority**: P1  
**Minimum Cases**: 6  

---

### 1.5.1 Planned & Unplanned Restart

##### 1.5.1.1 Verify planned graceful restart (restarting router)

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-01: Graceful Restart — Planned Restart (Restarting Router) |
| **Purpose Of The Test** | Verify that a planned graceful restart allows the OSPF process to restart without disrupting forwarding, and neighbors maintain adjacency via helper mode, per RFC 3623 Section 3. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (GR Restarting) (10.0.12.1) ---- (10.0.12.2) DUT-B (GR Helper)`<br>`    lo: 1.1.1.1                            lo: 2.2.2.2`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established before GR is triggered<br><br>**Configuration:**<br>DUT-A (Restarting Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart enable true`<br>`set protocols ospf grace-period 120`<br>`commit`<br><br>DUT-B (Helper Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart helper enable true`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A as GR restarting router with grace-period 120<br>2. Configure DUT-B as GR helper<br>3. Wait 40 seconds for Full adjacency<br>4. Execute `run graceful-restart prepare ospf` on DUT-A<br>5. Execute `pkill ospfd` on DUT-A<br>6. Wait 5 seconds<br>7. Execute `run show ospf graceful-restart helper detail` on DUT-B<br>8. Wait 60 seconds for OSPF process to restart and re-establish adjacency<br>9. Execute `run show ospf neighbor` on DUT-A<br>10. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. `run show ospf graceful-restart helper detail` on DUT-B shows it is in helper mode for neighbor 1.1.1.1<br>2. DUT-B continues to list routes from DUT-A during the restart period (forwarding not disrupted)<br>3. After OSPF process restarts, `run show ospf neighbor` on DUT-A shows neighbor 2.2.2.2 in Full state<br>4. `run show ospf neighbor` on DUT-B shows neighbor 1.1.1.1 in Full state (adjacency restored without going through Init/2-Way) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3623 Section 3 |

---

##### 1.5.1.2 Verify unplanned graceful restart behavior

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-02: Graceful Restart — Unplanned Restart (No Prepare) |
| **Purpose Of The Test** | Verify behavior when OSPF process is killed without `run graceful-restart prepare ospf`, simulating an unplanned crash, per RFC 3623 Section 3.1. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (GR Restarting) (10.0.12.1) ---- (10.0.12.2) DUT-B (GR Helper)`<br>`    lo: 1.1.1.1                            lo: 2.2.2.2`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established<br>3. DUT-A configured for GR but `run graceful-restart prepare ospf` NOT executed<br><br>**Configuration:**<br>DUT-A (Restarting Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart enable true`<br>`set protocols ospf grace-period 120`<br>`commit`<br><br>DUT-B (Helper Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart helper enable true`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A and DUT-B with GR capabilities<br>2. Wait 40 seconds for Full adjacency<br>3. Execute `pkill ospfd` on DUT-A without executing `run graceful-restart prepare ospf`<br>4. Wait 5 seconds<br>5. Execute `run show ospf graceful-restart helper detail` on DUT-B<br>6. Wait 60 seconds for OSPF to auto-restart<br>7. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. Since `run graceful-restart prepare ospf` was not run, the Grace LSA may indicate "unknown" restart reason<br>2. DUT-B's `run show ospf graceful-restart helper detail` shows helper activated (if implementation supports unplanned restart) or indicates no valid Grace LSA received<br>3. After OSPF restarts on DUT-A, adjacency is re-established — `run show ospf neighbor` on DUT-B shows 1.1.1.1 in Full state<br>4. Route convergence completes and DUT-B's routing table is updated |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3623 Section 3.1 |

---

##### 1.5.1.3 Verify planned graceful restart with route preservation

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-07: Graceful Restart — Successful Planned Restart with Route Preservation |
| **Purpose Of The Test** | Verify that during a planned graceful restart, the helper maintains forwarding entries and routes from the restarting router remain in the routing table throughout the restart, per RFC 3623 Section 2. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (GR Restarting) (10.0.12.1) ---- (10.0.12.2) DUT-B (GR Helper) (10.0.23.1) ---- (10.0.23.2) DUT-C`<br>`    lo: 1.1.1.1              lo: 2.2.2.2                                    lo: 3.3.3.3`<br>`  (192.168.1.0/24 stub)`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. All in Area 0, all adjacencies Full<br>3. DUT-C has learned 192.168.1.0/24 from DUT-A via DUT-B<br><br>**Configuration:**<br>DUT-A (Restarting Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 192.168.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart enable true`<br>`set protocols ospf grace-period 120`<br>`commit`<br><br>DUT-B (Helper Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart helper enable true`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.2 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`commit` |
| **Test Procedure** | 1. Configure three-router linear topology with GR on DUT-A and helper on DUT-B<br>2. Wait 40 seconds for all adjacencies to reach Full state<br>3. Execute `run show ospf route` on DUT-C<br>4. Execute `run graceful-restart prepare ospf` on DUT-A<br>5. Execute `pkill ospfd` on DUT-A<br>6. Wait 10 seconds<br>7. Execute `run show ospf route` on DUT-C<br>8. Execute `run show ospf route` on DUT-B<br>9. Wait 60 seconds for DUT-A's OSPF to fully restart<br>10. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. Before restart: `run show ospf route` on DUT-C contains 192.168.1.0/24 via 10.0.23.1<br>2. During restart (step 7): `run show ospf route` on DUT-C still contains 192.168.1.0/24 (route preserved by helper)<br>3. During restart (step 8): `run show ospf route` on DUT-B still contains 192.168.1.0/24 (helper maintains stale routes)<br>4. After restart: `run show ospf neighbor` on DUT-A shows both neighbors in Full state; all routes intact |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3623 Section 2 |

---

### 1.5.2 Helper Mode Behavior

##### 1.5.2.1 Verify helper mode rejects unplanned restart with planned-only

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-03: Graceful Restart — Helper Mode with planned-only |
| **Purpose Of The Test** | Verify that when helper is configured with `planned-only`, it only enters helper mode for planned restarts and rejects unplanned restarts, per RFC 3623 Section 3.2. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (GR Restarting) (10.0.12.1) ---- (10.0.12.2) DUT-B (GR Helper, planned-only)`<br>`    lo: 1.1.1.1                            lo: 2.2.2.2`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established<br><br>**Configuration:**<br>DUT-A (Restarting Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart enable true`<br>`set protocols ospf grace-period 120`<br>`commit`<br><br>DUT-B (Helper Router — planned-only):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart helper enable true`<br>`set protocols ospf graceful-restart helper planned-only`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-B helper with `planned-only` restriction<br>2. Wait 40 seconds for Full adjacency<br>3. Execute `pkill ospfd` on DUT-A without `run graceful-restart prepare ospf` (unplanned restart)<br>4. Wait 5 seconds<br>5. Execute `run show ospf graceful-restart helper detail` on DUT-B<br>6. Wait 45 seconds for dead-interval expiry<br>7. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. `run show ospf graceful-restart helper detail` on DUT-B shows it did NOT enter helper mode (restart reason is unplanned)<br>2. DUT-B treats the restart as a normal neighbor down event<br>3. `run show ospf neighbor` on DUT-B shows neighbor 1.1.1.1 dropped to Init or absent (normal re-adjacency process)<br>4. After OSPF restarts on DUT-A, adjacency is re-established through normal Init → 2-Way → ExStart → Exchange → Full sequence |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3623 Section 3.2 |

---

##### 1.5.2.2 Verify strict LSA checking exits helper mode on topology change

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-05: Graceful Restart — Strict LSA Checking |
| **Purpose Of The Test** | Verify that when strict-lsa-checking is enabled on the helper, it exits helper mode if topology changes (new LSA) occur during the grace period, per RFC 3623 Section 3.2. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (GR Restarting) (10.0.12.1) ---- (10.0.12.2) DUT-B (Helper, strict-lsa)`<br>`    lo: 1.1.1.1              lo: 2.2.2.2    |`<br>`                                             |`<br>`                              (10.0.23.1) ---+--- (10.0.23.2) DUT-C`<br>`                                                   lo: 3.3.3.3`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches; DUT-A and DUT-C connect to DUT-B<br>2. All adjacencies in Full state<br>3. DUT-B is configured as GR helper with strict-lsa-checking<br><br>**Configuration:**<br>DUT-A (Restarting Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart enable true`<br>`set protocols ospf grace-period 120`<br>`commit`<br><br>DUT-B (Helper — strict-lsa-checking):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.23.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart helper enable true`<br>`set protocols ospf graceful-restart helper strict-lsa-checking enable true`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.23.2 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-B helper with `strict-lsa-checking enable true`<br>2. Wait 40 seconds for all adjacencies to reach Full state<br>3. Execute `run graceful-restart prepare ospf` on DUT-A<br>4. Execute `pkill ospfd` on DUT-A<br>5. Wait 5 seconds<br>6. Execute `run show ospf graceful-restart helper detail` on DUT-B<br>7. Configure DUT-C: add a new network `set protocols ospf network 192.168.99.0/24 area 0.0.0.0` then `commit` (topology change)<br>8. Wait 10 seconds<br>9. Execute `run show ospf graceful-restart helper detail` on DUT-B |
| **Expected Results** | 1. After step 6: `run show ospf graceful-restart helper detail` on DUT-B shows active helper mode for neighbor 1.1.1.1<br>2. After step 7: DUT-C's topology change generates a new Router LSA<br>3. After step 9: DUT-B detects the topology-changing LSA and exits helper mode due to strict-lsa-checking<br>4. `run show ospf graceful-restart helper detail` on DUT-B no longer shows active helper for 1.1.1.1<br>5. DUT-B flushes stale routes and performs normal SPF recalculation |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3623 Section 3.2 |

---

##### 1.5.2.3 Verify helper rejects grace-period exceeding supported-grace-time

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-06: Graceful Restart — Helper Supported-Grace-Time Exceeded |
| **Purpose Of The Test** | Verify that the helper router rejects a GR request when the restarting router's grace-period exceeds the helper's configured supported-grace-time, per RFC 3623. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (GR Restarting) (10.0.12.1) ---- (10.0.12.2) DUT-B (GR Helper)`<br>`    lo: 1.1.1.1                            lo: 2.2.2.2`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established<br><br>**Configuration:**<br>DUT-A (Restarting Router — grace-period 300):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart enable true`<br>`set protocols ospf grace-period 300`<br>`commit`<br><br>DUT-B (Helper — supported-grace-time 60):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart helper enable true`<br>`set protocols ospf graceful-restart helper supported-grace-time 60`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with grace-period 300 seconds<br>2. Configure DUT-B helper with supported-grace-time 60 seconds<br>3. Wait 40 seconds for Full adjacency<br>4. Execute `run graceful-restart prepare ospf` on DUT-A<br>5. Execute `pkill ospfd` on DUT-A<br>6. Wait 5 seconds<br>7. Execute `run show ospf graceful-restart helper detail` on DUT-B |
| **Expected Results** | 1. `run show ospf graceful-restart helper detail` on DUT-B shows that helper mode was NOT entered because the requested grace-period (300s) exceeds the supported-grace-time (60s)<br>2. DUT-B treats the neighbor down event through normal OSPF procedures<br>3. After DUT-A's OSPF process restarts, adjacency is re-formed through normal Init → Full sequence |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3623 Section 3.2 |

---

### 1.5.3 Grace Period

##### 1.5.3.1 Verify grace-period timeout exits helper mode

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-04: Graceful Restart — Grace-Period Timeout |
| **Purpose Of The Test** | Verify that if the restarting router fails to complete GR within the grace-period, the helper exits helper mode and adjacency is reset, per RFC 3623 Section 3.2. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (GR Restarting) (10.0.12.1) ---- (10.0.12.2) DUT-B (GR Helper)`<br>`    lo: 1.1.1.1                            lo: 2.2.2.2`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established<br>3. DUT-A configured with a very short grace-period (30 seconds)<br><br>**Configuration:**<br>DUT-A (Restarting Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart enable true`<br>`set protocols ospf grace-period 30`<br>`commit`<br><br>DUT-B (Helper Router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf capability opaque`<br>`set protocols ospf graceful-restart helper enable true`<br>`set protocols ospf graceful-restart helper supported-grace-time 30`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with grace-period 30 seconds<br>2. Configure DUT-B helper with supported-grace-time 30 seconds<br>3. Wait 40 seconds for Full adjacency<br>4. Execute `run graceful-restart prepare ospf` on DUT-A<br>5. Execute `pkill ospfd` on DUT-A<br>6. Disconnect DUT-A's management interface to prevent OSPF from restarting (simulate process hang)<br>7. Wait 35 seconds (beyond grace-period)<br>8. Execute `run show ospf graceful-restart helper detail` on DUT-B<br>9. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. During the first 30 seconds: `run show ospf graceful-restart helper detail` on DUT-B shows active helper mode<br>2. After 30 seconds (grace-period expiry): DUT-B exits helper mode<br>3. `run show ospf neighbor` on DUT-B no longer shows 1.1.1.1 in Full state; adjacency is reset<br>4. DUT-B removes stale routes from DUT-A and runs SPF recalculation |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3623 Section 3.2 |

---

## 1.6 OSPF Interface Parameters & Authentication (MODULE 6)

**RFC Reference**: RFC 2328 Sections 8 (Protocol Packet Processing), 9 (The Interface Data Structure)  
**Priority**: P1  
**Minimum Cases**: 6  

---

### 1.6.1 Timer Parameters

##### 1.6.1.1 Verify hello-interval configuration and neighbor formation

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-01: Hello-Interval Configuration and Neighbor Formation |
| **Purpose Of The Test** | Verify that OSPF neighbors form adjacency when hello-interval matches on both sides, and fail when mismatched, per RFC 2328 Section 9.5. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 5`<br>`set protocols ospf interface vlan100 dead-interval 20`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 5`<br>`set protocols ospf interface vlan100 dead-interval 20`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with hello-interval 5 and dead-interval 20 on vlan100<br>2. Configure DUT-B with hello-interval 5 and dead-interval 20 on vlan100<br>3. Wait 30 seconds for adjacency formation<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf interface` on DUT-A |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows neighbor 2.2.2.2 in Full state<br>2. `run show ospf interface` on DUT-A shows vlan100 with hello-interval 5 and dead-interval 20<br>3. Adjacency formed successfully because hello-interval and dead-interval match on both sides |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9.5 |

---

##### 1.6.1.2 Verify hello-interval mismatch prevents adjacency

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-02: Hello-Interval Mismatch Prevents Adjacency |
| **Purpose Of The Test** | Verify that OSPF adjacency is NOT formed when hello-interval differs between two neighbors, per RFC 2328 Section 10.5. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`  hello: 5s                  hello: 10s`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 5`<br>`set protocols ospf interface vlan100 dead-interval 20`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 10`<br>`set protocols ospf interface vlan100 dead-interval 40`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with hello-interval 5 on vlan100<br>2. Configure DUT-B with hello-interval 10 on vlan100<br>3. Wait 60 seconds<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf interface` on DUT-A |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows no neighbor in Full state (empty or stuck in Init/Attempt)<br>2. `run show ospf interface` on DUT-A shows vlan100 with hello-interval 5<br>3. Adjacency is NOT formed because hello-interval mismatch causes Hello packets to be rejected per RFC 2328 Section 10.5 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10.5 |

---

##### 1.6.1.3 Verify dead-interval timeout declares neighbor down

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-07: Dead-Interval Configuration and Neighbor Timeout |
| **Purpose Of The Test** | Verify that a neighbor is declared down after the dead-interval expires without receiving Hello packets, per RFC 2328 Section 9. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`    hello: 2s, dead: 8s      hello: 2s, dead: 8s`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established with aggressive timers (hello 2s, dead 8s)<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 2`<br>`set protocols ospf interface vlan100 dead-interval 8`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 2`<br>`set protocols ospf interface vlan100 dead-interval 8`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure both DUTs with hello-interval 2 and dead-interval 8<br>2. Wait 20 seconds for Full adjacency<br>3. Execute `run show ospf neighbor` on DUT-A<br>4. Shutdown ge-1/1/1 on DUT-B (stops Hello packets)<br>5. Wait 10 seconds (exceeds dead-interval of 8 seconds)<br>6. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. Before shutdown: `run show ospf neighbor` on DUT-A shows 2.2.2.2 in Full state<br>2. After 10 seconds: `run show ospf neighbor` on DUT-A shows no neighbor (2.2.2.2 removed after dead-interval expiry at 8 seconds)<br>3. `run show ospf interface` on DUT-A still shows vlan100 with dead-interval 8 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9 |

---

### 1.6.2 Interface Cost & Passive

##### 1.6.2.1 Verify interface cost affects route selection

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-03: Interface Cost Affects Route Selection |
| **Purpose Of The Test** | Verify that configuring different interface costs on OSPF interfaces correctly influences SPF path selection, per RFC 2328 Section 9. |
| **Test Topo & Precondition** | **Topology:**<br>`                  vlan100 (cost 10)`<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    |  lo: 1.1.1.1          lo: 2.2.2.2  |`<br>`    |                                     |`<br>`  vlan200 (cost 500)                   vlan300 (cost 10)`<br>`  (10.0.13.1)                        (10.0.23.2)`<br>`    |                                     |`<br>`    +---- (10.0.13.2) DUT-C (10.0.23.1) -+`<br>`              lo: 3.3.3.3`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a triangle topology<br>2. All links operational<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 500`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 cost 10`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.13.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 300`<br>`set l3-interface vlan-interface vlan300 address 10.0.23.1 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 cost 500`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface vlan300 cost 10`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with cost 10 toward DUT-B and cost 500 toward DUT-C<br>2. Configure DUT-B and DUT-C accordingly<br>3. Wait 40 seconds for all adjacencies to reach Full state<br>4. Execute `run show ospf route` on DUT-A<br>5. Execute `run show ospf interface` on DUT-A |
| **Expected Results** | 1. `run show ospf route` on DUT-A shows route to 3.3.3.3/32 via next-hop 10.0.12.2 (DUT-B) with cost 30 (10+10+10)<br>2. Route to DUT-C does NOT use the direct link (cost 500+10 = 510)<br>3. `run show ospf interface` on DUT-A confirms vlan100 cost=10 and vlan200 cost=500 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9 |

---

##### 1.6.2.2 Verify passive interface suppresses hello packets

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-04: Passive Interface Suppresses Hello Packets |
| **Purpose Of The Test** | Verify that configuring an interface as passive advertises its network into OSPF but suppresses Hello packets (no adjacency formed on that interface), per RFC 2328 Section 9. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`    vlan200: 192.168.1.1/24 (passive)`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. DUT-A has an additional interface vlan200 configured as passive<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 192.168.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan200 passive`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with vlan200 as passive OSPF interface<br>2. Configure DUT-B in OSPF Area 0<br>3. Wait 40 seconds for adjacency on vlan100<br>4. Execute `run show ospf interface` on DUT-A<br>5. Execute `run show ospf route` on DUT-B<br>6. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. `run show ospf interface` on DUT-A shows vlan200 as passive<br>2. `run show ospf route` on DUT-B contains 192.168.1.0/24 as an intra-area route (network is advertised)<br>3. `run show ospf neighbor` on DUT-A shows only neighbor 2.2.2.2 on vlan100 — no neighbor on vlan200<br>4. No OSPF Hello packets are sent on DUT-A's vlan200 interface |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9 |

---

### 1.6.3 Authentication

##### 1.6.3.1 Verify MD5 authentication with matching keys

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-05: MD5 Authentication — Matching Keys |
| **Purpose Of The Test** | Verify that OSPF adjacency forms successfully when both neighbors are configured with the same MD5 authentication key, per RFC 2328 Appendix D. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`    MD5 key-id 1: "SecretKey123"    MD5 key-id 1: "SecretKey123"`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 authentication message-digest`<br>`set protocols ospf interface vlan100 message-digest-key 1 md5 SecretKey123`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 authentication message-digest`<br>`set protocols ospf interface vlan100 message-digest-key 1 md5 SecretKey123`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with MD5 authentication key-id 1, key "SecretKey123" on vlan100<br>2. Configure DUT-B with MD5 authentication key-id 1, key "SecretKey123" on vlan100<br>3. Wait 40 seconds for adjacency formation<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf interface` on DUT-A |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows neighbor 2.2.2.2 in Full state<br>2. `run show ospf interface` on DUT-A shows vlan100 with authentication type "message-digest"<br>3. Adjacency is successfully formed because MD5 key-id and key value match |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Appendix D |

---

##### 1.6.3.2 Verify MD5 authentication key mismatch prevents adjacency

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-06: MD5 Authentication — Key Mismatch Prevents Adjacency |
| **Purpose Of The Test** | Verify that OSPF adjacency is NOT formed when MD5 authentication keys differ between two neighbors, per RFC 2328 Appendix D. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`    MD5 key-id 1: "KeyAlpha"    MD5 key-id 1: "KeyBravo"`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 authentication message-digest`<br>`set protocols ospf interface vlan100 message-digest-key 1 md5 KeyAlpha`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 authentication message-digest`<br>`set protocols ospf interface vlan100 message-digest-key 1 md5 KeyBravo`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with MD5 key "KeyAlpha" on vlan100<br>2. Configure DUT-B with MD5 key "KeyBravo" on vlan100<br>3. Wait 60 seconds<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows no neighbor in Full state (empty or stuck in Init)<br>2. `run show ospf neighbor` on DUT-B shows no neighbor in Full state<br>3. Adjacency is NOT formed because MD5 authentication digest mismatch causes packet rejection per RFC 2328 Appendix D |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Appendix D |

---

### 1.6.4 Fast Failure Detection

##### 1.6.4.1 Verify BFD for OSPF fast failure detection

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-08: BFD for OSPF Fast Failure Detection |
| **Purpose Of The Test** | Verify that enabling BFD on OSPF interfaces provides sub-second failure detection and triggers adjacency teardown faster than the OSPF dead-interval. |
| **Test Topo & Precondition** | **Topology:**<br>`  DUT-A (10.0.12.1) ---- (10.0.12.2) DUT-B`<br>`    lo: 1.1.1.1              lo: 2.2.2.2`<br>`    BFD enabled               BFD enabled`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Both devices support BFD<br>3. Full adjacency established<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 10`<br>`set protocols ospf interface vlan100 dead-interval 40`<br>`set protocols ospf interface vlan100 bfd`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 10`<br>`set protocols ospf interface vlan100 dead-interval 40`<br>`set protocols ospf interface vlan100 bfd`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure both DUTs with BFD enabled on OSPF interface vlan100 (hello 10s, dead 40s)<br>2. Wait 40 seconds for Full adjacency and BFD session establishment<br>3. Execute `run show ospf neighbor` on DUT-A<br>4. Shutdown ge-1/1/1 on DUT-B<br>5. Wait 3 seconds<br>6. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. Before shutdown: `run show ospf neighbor` on DUT-A shows 2.2.2.2 in Full state<br>2. After link failure with BFD: `run show ospf neighbor` on DUT-A shows neighbor removed within 3 seconds (far faster than the 40-second dead-interval)<br>3. BFD detects the link failure in sub-second time and notifies OSPF to tear down the adjacency immediately<br>4. `run show ospf route` on DUT-A no longer contains routes via 10.0.12.2 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9 (interface parameters) + BFD integration |

---

## Coverage Summary

| Module | Feature | P0 Cases | P1 Cases | P2 Cases | Total | Sufficient? |
|--------|---------|----------|----------|----------|-------|-------------|
| MOD4 | SPF Calculation & Route Learning | 10 | 0 | 0 | 10 | Yes (≥8 P0) |
| MOD5 | Graceful Restart | 0 | 7 | 0 | 7 | Yes (≥6 P1) |
| MOD6 | Interface Parameters & Authentication | 0 | 8 | 0 | 8 | Yes (≥6 P1) |
| **Total** | | **10** | **15** | **0** | **25** | **Yes** |

### Module 4 Coverage Detail:
- Basic route learning: MOD4-01
- Cost-based path selection: MOD4-02
- ECMP: MOD4-03
- Route convergence after link failure: MOD4-04
- Inter-area route learning (ABR): MOD4-05
- Route summarization (area range): MOD4-06
- SPF recalculation after cost change: MOD4-07
- External route learning (redistribution): MOD4-08
- Route withdrawal: MOD4-09
- Route filtering via route-map: MOD4-10

### Module 5 Coverage Detail:
- Planned GR restart: MOD5-01
- Unplanned GR restart: MOD5-02
- Helper planned-only mode: MOD5-03
- Grace-period timeout: MOD5-04
- Strict LSA checking: MOD5-05
- Supported-grace-time exceeded: MOD5-06
- Route preservation during GR: MOD5-07

### Module 6 Coverage Detail:
- Hello-interval match: MOD6-01
- Hello-interval mismatch: MOD6-02
- Interface cost: MOD6-03
- Passive interface: MOD6-04
- MD5 authentication match: MOD6-05
- MD5 authentication mismatch: MOD6-06
- Dead-interval timeout: MOD6-07
- BFD for OSPF: MOD6-08

### CLI Command Coverage:
All PicOS CLI commands provided in the requirements are used in at least one test case:
- ✅ `set protocols ospf router-id`
- ✅ `set protocols ospf area ... area-type`
- ✅ `set protocols ospf interface ... area`
- ✅ `set protocols ospf network ... area`
- ✅ `set protocols ospf interface ... hello-interval`
- ✅ `set protocols ospf interface ... dead-interval`
- ✅ `set protocols ospf interface ... cost`
- ✅ `set protocols ospf interface ... passive`
- ✅ `set protocols ospf interface ... authentication message-digest`
- ✅ `set protocols ospf interface ... message-digest-key ... md5`
- ✅ `set protocols ospf interface ... bfd`
- ✅ `set protocols ospf redistribute ...`
- ✅ `set protocols ospf redistribute ... metric`
- ✅ `set protocols ospf redistribute ... route-map`
- ✅ `set protocols ospf area ... range`
- ✅ `set protocols ospf capability opaque`
- ✅ `set protocols ospf graceful-restart enable true`
- ✅ `set protocols ospf grace-period`
- ✅ `set protocols ospf graceful-restart helper enable true`
- ✅ `set protocols ospf graceful-restart helper planned-only`
- ✅ `set protocols ospf graceful-restart helper strict-lsa-checking enable true`
- ✅ `set protocols ospf graceful-restart helper supported-grace-time`
- ✅ `run graceful-restart prepare ospf`
- ✅ `run show ospf neighbor`
- ✅ `run show ospf database`
- ✅ `run show ospf interface`
- ✅ `run show ospf route`
- ✅ `run show route ipv4`
- ✅ `run show ospf graceful-restart helper detail`
- ✅ VLAN/interface prerequisite commands
- ✅ Loopback interface commands
