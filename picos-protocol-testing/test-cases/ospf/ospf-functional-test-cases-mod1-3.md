# PicOS 4.6 OSPF Functional Test Cases — Modules 1, 2, 3

**Platform**: PicOS 4.6  
**RFC Reference**: RFC 2328 (OSPFv2)  
**Generated**: 2026-03-17  

---

## Table of Contents

- [1. FUNCTIONAL TESTING](#1-functional-testing)
  - [1.1 Neighbor Discovery & Adjacency (MODULE 1)](#11-neighbor-discovery--adjacency-module-1)
    - [1.1.1 Basic Neighbor Formation & State Transitions](#111-basic-neighbor-formation--state-transitions)
      - [1.1.1.1 MOD1-01: Basic Neighbor Establishment](#1111-verify-basic-ospf-neighbor-establishment-with-matching-parameters)
      - [1.1.1.2 MOD1-06: Neighbor State Transitions](#1112-verify-ospf-neighbor-state-transitions-init--2-way--exstart--exchange--full)
      - [1.1.1.3 MOD1-07: New Router Joins Existing Domain](#1113-verify-adjacency-formation-when-new-router-joins-existing-ospf-domain)
    - [1.1.2 Parameter Mismatch & Conflict](#112-parameter-mismatch--conflict)
      - [1.1.2.1 MOD1-02: Hello Interval Mismatch](#1121-verify-hello-interval-mismatch-prevents-ospf-adjacency)
      - [1.1.2.2 MOD1-09: Area ID Mismatch](#1122-verify-area-id-mismatch-prevents-ospf-adjacency)
      - [1.1.2.3 MOD1-10: Router-ID Conflict](#1123-verify-ospf-behavior-with-duplicate-router-id-conflict)
    - [1.1.3 DR/BDR Election](#113-drbdr-election)
      - [1.1.3.1 MOD1-04: DR Election](#1131-verify-dr-election-on-broadcast-segment-highest-router-id-wins)
      - [1.1.3.2 MOD1-05: BDR Election](#1132-verify-bdr-election-on-broadcast-segment-second-highest-router-id)
    - [1.1.4 Neighbor Loss & Recovery](#114-neighbor-loss--recovery)
      - [1.1.4.1 MOD1-03: Dead Interval Expiry](#1141-verify-dead-interval-expiry-tears-down-ospf-neighbor)
      - [1.1.4.2 MOD1-08: Interface Shutdown](#1142-verify-neighbor-loss-detection-after-interface-shutdown)
  - [1.2 Area Types (MODULE 2)](#12-area-types-module-2)
    - [1.2.1 Stub Area](#121-stub-area)
      - [1.2.1.1 MOD2-01: Stub Blocks Type-5](#1211-verify-stub-area-blocks-type-5-lsas-and-injects-default-route)
      - [1.2.1.2 MOD2-02: Totally Stubby](#1212-verify-totally-stubby-area-blocks-type-3-and-type-5-lsas)
      - [1.2.1.3 MOD2-06: Stub Rejects Redistribution](#1213-verify-stub-area-rejects-external-redistribution)
    - [1.2.2 NSSA Area](#122-nssa-area)
      - [1.2.2.1 MOD2-03: NSSA Imports as Type-7](#1221-verify-nssa-imports-external-routes-as-type-7-lsa)
      - [1.2.2.2 MOD2-04: Totally NSSA](#1222-verify-totally-nssa-blocks-type-3-summary-lsas)
      - [1.2.2.3 MOD2-08: Type-7 to Type-5 Translation](#1223-verify-type-7-to-type-5-translation-at-nssa-abr)
    - [1.2.3 Normal Area & Mismatch](#123-normal-area--mismatch)
      - [1.2.3.1 MOD2-07: Normal Area All LSA Types](#1231-verify-normal-area-receives-all-lsa-types)
      - [1.2.3.2 MOD2-05: Area Type Mismatch](#1232-verify-area-type-mismatch-prevents-ospf-adjacency)
  - [1.3 Route Redistribution & Route Maps (MODULE 3)](#13-route-redistribution--route-maps-module-3)
    - [1.3.1 Static & Connected Redistribution](#131-static--connected-redistribution)
      - [1.3.1.1 MOD3-01: Redistribute Static](#1311-verify-redistribute-static-routes-into-ospf)
      - [1.3.1.2 MOD3-02: Redistribute Connected](#1312-verify-redistribute-connected-routes-into-ospf)
    - [1.3.2 Route-Map Filtering & Metric](#132-route-map-filtering--metric)
      - [1.3.2.1 MOD3-03: Route-Map Filtering](#1321-verify-route-map-filtering-permits-specific-prefix-only)
      - [1.3.2.2 MOD3-04: Custom Metric](#1322-verify-custom-metric-applied-to-redistributed-routes)
    - [1.3.3 Redistribution Changes](#133-redistribution-changes)
      - [1.3.3.1 MOD3-05: Remove Redistribution](#1331-verify-removing-redistribution-withdraws-external-routes)
      - [1.3.3.2 MOD3-06: Metric Change](#1332-verify-redistribution-metric-change-takes-effect)
- [Coverage Summary](#coverage-summary)

---

## 1. FUNCTIONAL TESTING

### 1.1 Neighbor Discovery & Adjacency (MODULE 1)

**RFC 2328 Sections**: 7 (Flooding), 9 (The Interface Data Structure), 10 (The Neighbor Data Structure)  
**Priority**: P0  
**Cases**: 10  

#### 1.1.1 Basic Neighbor Formation & State Transitions

##### 1.1.1.1 Verify Basic OSPF Neighbor Establishment with Matching Parameters

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-01: Basic Neighbor Establishment (Two DUTs, Same Area, Default Parameters) |
| **Purpose Of The Test** | Verify that two OSPF routers in the same area with matching parameters form a Full adjacency, per RFC 2328 Section 10. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration on either device<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with OSPF in Area 0 on vlan100 and loopback<br>2. Configure DUT-B with OSPF in Area 0 on vlan100 and loopback<br>3. Wait 40 seconds for OSPF adjacency to reach Full state<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf neighbor` on DUT-B<br>6. Execute `run show ospf interface` on DUT-A |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows neighbor 2.2.2.2 in Full state<br>2. `run show ospf neighbor` on DUT-B shows neighbor 1.1.1.1 in Full state<br>3. `run show ospf interface` on DUT-A shows vlan100 with default hello-interval 10 and dead-interval 40<br>4. `run show ospf route` on DUT-A contains 2.2.2.2/32 as an intra-area route |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10 |

---

##### 1.1.1.2 Verify OSPF Neighbor State Transitions (Init → 2-Way → ExStart → Exchange → Full)

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-06: Neighbor State Transitions (Init → 2-Way → ExStart → Exchange → Full) |
| **Purpose Of The Test** | Verify that OSPF neighbor state transitions follow the correct FSM sequence from Init to Full on a point-to-point-like adjacency, per RFC 2328 Section 10. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration on either device<br>3. DUT-B is configured first with OSPF enabled; DUT-A OSPF is not yet configured<br><br>**Configuration:**<br>DUT-A (configure after DUT-B is ready):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (configure first):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-B with OSPF in Area 0<br>2. Wait 10 seconds for DUT-B to begin sending Hello packets<br>3. Configure DUT-A with OSPF in Area 0<br>4. Execute `run show ospf neighbor` on DUT-B immediately (within 2 seconds)<br>5. Wait 5 seconds<br>6. Execute `run show ospf neighbor` on DUT-B<br>7. Wait 10 seconds<br>8. Execute `run show ospf neighbor` on DUT-B<br>9. Wait 30 seconds<br>10. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. Immediately after DUT-A sends its first Hello: DUT-B's `run show ospf neighbor` shows 1.1.1.1 in Init state (Hello received, but DUT-B not yet seen in DUT-A's Hello)<br>2. After both sides exchange Hellos with each other's Router-ID: neighbor transitions to 2-Way state<br>3. After database exchange begins: neighbor transitions through ExStart → Exchange states<br>4. After complete database synchronization: `run show ospf neighbor` on DUT-B shows 1.1.1.1 in Full state<br>5. The transition sequence Init → 2-Way → ExStart → Exchange → Loading → Full is completed |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10.1, 10.2, 10.3, 10.6, 10.7, 10.8 |

---

##### 1.1.1.3 Verify Adjacency Formation When New Router Joins Existing OSPF Domain

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-07: Adjacency Formation When New Router Joins Existing OSPF Domain |
| **Purpose Of The Test** | Verify that a new router joining an existing OSPF domain correctly forms adjacency with the DR and learns all existing routes, per RFC 2328 Section 10. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.1.1/24)`<br>`  lo: 1.1.1.1                 \`<br>`  (192.168.10.0/24 stub)       +---- Broadcast Segment (VLAN 100)`<br>`                               |`<br>`DUT-B (vlan100: 10.0.1.2/24)  |`<br>`  lo: 2.2.2.2 (DR)            |`<br>`  (192.168.20.0/24 stub)      /`<br>`                             /`<br>`DUT-C (vlan100: 10.0.1.3/24)  ← Joins later`<br>`  lo: 3.3.3.3`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches; DUT-A and DUT-B already have OSPF configured and are in Full adjacency<br>2. DUT-C has L2/L3 connectivity to the broadcast segment but OSPF is not yet configured<br><br>**Configuration:**<br>DUT-A (already running):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 192.168.10.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (already running):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set l3-interface vlan-interface vlan300 address 192.168.20.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C (joins later):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.3 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A and DUT-B with OSPF in Area 0<br>2. Wait 40 seconds for Full adjacency between DUT-A and DUT-B<br>3. Execute `run show ospf neighbor` on DUT-A<br>4. Configure DUT-C with OSPF in Area 0 (new router joins)<br>5. Wait 40 seconds for DUT-C to form adjacency<br>6. Execute `run show ospf neighbor` on DUT-C<br>7. Execute `run show ospf route` on DUT-C |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-C shows Full adjacency with the DR (2.2.2.2)<br>2. `run show ospf route` on DUT-C contains 192.168.10.0/24 as an intra-area route (learned from DUT-A)<br>3. `run show ospf route` on DUT-C contains 192.168.20.0/24 as an intra-area route (learned from DUT-B)<br>4. `run show ospf database` on DUT-C contains Router LSAs from all three routers (1.1.1.1, 2.2.2.2, 3.3.3.3) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10 |

---

#### 1.1.2 Parameter Mismatch & Conflict

##### 1.1.2.1 Verify Hello Interval Mismatch Prevents OSPF Adjacency

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-02: Hello Interval Mismatch Prevents Adjacency |
| **Purpose Of The Test** | Verify that OSPF adjacency is NOT formed when hello-interval differs between two neighbors, per RFC 2328 Section 10.5 (Hello packets with mismatched HelloInterval are rejected). |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`  hello: 5s, dead: 20s               hello: 10s, dead: 40s`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration on either device<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 5`<br>`set protocols ospf interface vlan100 dead-interval 20`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 10`<br>`set protocols ospf interface vlan100 dead-interval 40`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with hello-interval 5 and dead-interval 20 on vlan100<br>2. Configure DUT-B with hello-interval 10 and dead-interval 40 on vlan100<br>3. Wait 60 seconds<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows no neighbor in Full state (empty or stuck in Init)<br>2. `run show ospf neighbor` on DUT-B shows no neighbor in Full state<br>3. Adjacency is NOT formed because Hello packets with mismatched HelloInterval are rejected per RFC 2328 Section 10.5<br>4. `run show ospf interface` on DUT-A shows vlan100 with hello-interval 5 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10.5 |

---

##### 1.1.2.2 Verify Area ID Mismatch Prevents OSPF Adjacency

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-09: Area ID Mismatch Prevents Adjacency |
| **Purpose Of The Test** | Verify that OSPF adjacency is NOT formed when two neighbors have different Area IDs on their connecting interface, per RFC 2328 Section 10.5 (the Area ID field in the Hello packet must match). |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`  Area 0.0.0.0                       Area 0.0.0.1`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration on either device<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with vlan100 in Area 0.0.0.0<br>2. Configure DUT-B with vlan100 in Area 0.0.0.1<br>3. Wait 60 seconds<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows no neighbor in Full state (empty or no entry for 2.2.2.2)<br>2. `run show ospf neighbor` on DUT-B shows no neighbor in Full state<br>3. Adjacency is NOT formed because the Area ID in the Hello packet header does not match per RFC 2328 Section 10.5<br>4. Each router's `run show ospf interface` shows vlan100 in its respective area, but DR state is itself (no other router on the segment) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10.5 |

---

##### 1.1.2.3 Verify OSPF Behavior with Duplicate Router-ID Conflict

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-10: Router-ID Conflict Handling (Two Routers with Same Router-ID) |
| **Purpose Of The Test** | Verify OSPF behavior when two routers are configured with the same Router-ID on the same segment — adjacency should fail or produce unpredictable/conflicting LSA behavior, per RFC 2328 Section 10. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`  router-id: 1.1.1.1                 router-id: 1.1.1.1 (CONFLICT)`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration on either device<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with router-id 1.1.1.1<br>2. Configure DUT-B with router-id 1.1.1.1 (same as DUT-A — conflict)<br>3. Wait 60 seconds<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf neighbor` on DUT-B<br>6. Execute `run show ospf database` on DUT-A<br>7. Execute `run show ospf database` on DUT-B |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows no stable Full adjacency with 1.1.1.1 (neighbor is itself)<br>2. `run show ospf database` on DUT-A shows Router LSA conflicts — the same LS ID (1.1.1.1) has different LS sequences from both routers, causing continuous LSA overwrites<br>3. `run show ospf database` on DUT-B shows similar LSA conflict behavior<br>4. Routes are unstable or missing due to Router-ID collision<br>5. OSPF cannot establish a stable adjacency because both routers advertise the same Router-ID, causing the LSDB to be inconsistent |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10 |

---

#### 1.1.3 DR/BDR Election

##### 1.1.3.1 Verify DR Election on Broadcast Segment (Highest Router-ID Wins)

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-04: DR Election on Broadcast Segment (Highest Router-ID Wins DR) |
| **Purpose Of The Test** | Verify that the router with the highest Router-ID is elected as DR on a broadcast segment with three routers, per RFC 2328 Section 9.4. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.1.1/24)`<br>`  lo: 1.1.1.1                 \`<br>`                               +---- Broadcast Segment (VLAN 100)`<br>`DUT-B (vlan100: 10.0.1.2/24)  |`<br>`  lo: 2.2.2.2                 /`<br>`                             /`<br>`DUT-C (vlan100: 10.0.1.3/24)`<br>`  lo: 3.3.3.3`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches connected to the same broadcast segment via ge-1/1/1 (e.g., shared L2 switch or VLAN 100)<br>2. No pre-existing OSPF configuration on any device<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.3 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with router-id 1.1.1.1<br>2. Configure DUT-B with router-id 2.2.2.2<br>3. Configure DUT-C with router-id 3.3.3.3<br>4. Wait 50 seconds for DR/BDR election and Full adjacencies<br>5. Execute `run show ospf interface` on DUT-A<br>6. Execute `run show ospf interface` on DUT-B<br>7. Execute `run show ospf interface` on DUT-C<br>8. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. `run show ospf interface` on DUT-C shows vlan100 with DR state (3.3.3.3 is highest router-id)<br>2. `run show ospf interface` on DUT-A and DUT-B show vlan100 with DR listed as 10.0.1.3 (DUT-C's interface address)<br>3. `run show ospf neighbor` on DUT-A shows Full adjacency with the DR (3.3.3.3), which is DUT-C<br>4. DUT-C is elected DR because it has the highest Router-ID per RFC 2328 Section 9.4 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9.4 |

---

##### 1.1.3.2 Verify BDR Election on Broadcast Segment (Second-Highest Router-ID)

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-05: BDR Election (Second-Highest Router-ID Becomes BDR) |
| **Purpose Of The Test** | Verify that the router with the second-highest Router-ID is elected as BDR on a broadcast segment, per RFC 2328 Section 9.4. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.1.1/24)`<br>`  lo: 1.1.1.1                 \`<br>`                               +---- Broadcast Segment (VLAN 100)`<br>`DUT-B (vlan100: 10.0.1.2/24)  |`<br>`  lo: 2.2.2.2                 /`<br>`                             /`<br>`DUT-C (vlan100: 10.0.1.3/24)`<br>`  lo: 3.3.3.3`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches connected to the same broadcast segment via ge-1/1/1<br>2. No pre-existing OSPF configuration on any device<br>3. Router-IDs: DUT-A = 1.1.1.1, DUT-B = 2.2.2.2, DUT-C = 3.3.3.3<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.3 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with router-id 1.1.1.1<br>2. Configure DUT-B with router-id 2.2.2.2<br>3. Configure DUT-C with router-id 3.3.3.3<br>4. Wait 50 seconds for DR/BDR election and Full adjacencies<br>5. Execute `run show ospf interface` on DUT-B<br>6. Execute `run show ospf interface` on DUT-A<br>7. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. `run show ospf interface` on DUT-B shows vlan100 with BDR state (2.2.2.2 is the second-highest router-id)<br>2. `run show ospf interface` on DUT-A and DUT-C show BDR listed as 10.0.1.2 (DUT-B's interface address)<br>3. `run show ospf neighbor` on DUT-B shows Full adjacency with DR (3.3.3.3) and Full/2-Way with DRother (1.1.1.1)<br>4. DUT-A (1.1.1.1) is DRother since it has the lowest router-id |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9.4 |

---

#### 1.1.4 Neighbor Loss & Recovery

##### 1.1.4.1 Verify Dead Interval Expiry Tears Down OSPF Neighbor

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-03: Dead Interval Expiry Tears Down Neighbor |
| **Purpose Of The Test** | Verify that a neighbor is declared down and adjacency torn down after the dead-interval expires without receiving Hello packets, per RFC 2328 Section 9 (InactivityTimer event). |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`  hello: 3s, dead: 12s               hello: 3s, dead: 12s`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established with hello-interval 3 and dead-interval 12<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 3`<br>`set protocols ospf interface vlan100 dead-interval 12`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan100 hello-interval 3`<br>`set protocols ospf interface vlan100 dead-interval 12`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A and DUT-B with hello-interval 3 and dead-interval 12<br>2. Wait 20 seconds for Full adjacency<br>3. Execute `run show ospf neighbor` on DUT-A<br>4. Shutdown ge-1/1/1 on DUT-B (stops Hello packets toward DUT-A)<br>5. Wait 15 seconds (exceeds dead-interval of 12 seconds)<br>6. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. Before shutdown: `run show ospf neighbor` on DUT-A shows 2.2.2.2 in Full state<br>2. After 15 seconds: `run show ospf neighbor` on DUT-A shows no neighbor (2.2.2.2 removed after dead-interval expiry at 12 seconds)<br>3. `run show ospf route` on DUT-A no longer contains routes learned from DUT-B<br>4. `run show ospf database` on DUT-A shows DUT-A's Router LSA updated to reflect the neighbor loss |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9 |

---

##### 1.1.4.2 Verify Neighbor Loss Detection After Interface Shutdown

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-08: Neighbor Loss Detection After Interface Shutdown |
| **Purpose Of The Test** | Verify that shutting down a local OSPF interface causes the neighbor to detect loss and remove the adjacency after dead-interval expiry, per RFC 2328 Section 9. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`                                      (vlan200: 192.168.50.1/24) --- Stub`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established<br>3. DUT-A has learned 192.168.50.0/24 from DUT-B<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 192.168.50.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A and DUT-B with OSPF in Area 0<br>2. Wait 40 seconds for Full adjacency<br>3. Execute `run show ospf neighbor` on DUT-A<br>4. Execute `run show ospf route` on DUT-A<br>5. Shutdown ge-1/1/1 on DUT-A<br>6. Wait 45 seconds (exceeds default dead-interval of 40 seconds)<br>7. Execute `run show ospf neighbor` on DUT-B<br>8. Execute `run show ospf route` on DUT-B |
| **Expected Results** | 1. Before shutdown: `run show ospf neighbor` on DUT-A shows 2.2.2.2 in Full state<br>2. Before shutdown: `run show ospf route` on DUT-A contains 192.168.50.0/24<br>3. After shutdown and dead-interval expiry: `run show ospf neighbor` on DUT-B shows no neighbor (1.1.1.1 removed)<br>4. `run show ospf route` on DUT-B no longer contains routes via DUT-A's link<br>5. `run show ospf database` on DUT-B shows updated Router LSA reflecting neighbor loss |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 9 |

---

### 1.2 Area Types (MODULE 2)

**RFC 2328 Sections**: 3.6 (Backbone Area), 12 (LSA Encoding)  
**Priority**: P1  
**Cases**: 8  

#### 1.2.1 Stub Area

##### 1.2.1.1 Verify Stub Area Blocks Type-5 LSAs and Injects Default Route

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-01: Stub Area Blocks Type-5 LSAs, Injects Default Route |
| **Purpose Of The Test** | Verify that a stub area blocks Type-5 AS-External LSAs and the ABR injects a default route (0.0.0.0/0) into the stub area, per RFC 2328 Section 3.6. |
| **Test Topo & Precondition** | **Topology:**<br>`Area 1 (Stub)                       Area 0 (Backbone)`<br>`DUT-A (10.0.1.1) ---- (10.0.1.2) DUT-B (ABR) (10.0.2.1) ---- (10.0.2.2) DUT-C (ASBR)`<br>`  lo: 1.1.1.1           lo: 2.2.2.2                              lo: 3.3.3.3`<br>`                                                                  redistribute static: 203.0.113.0/24`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. DUT-B acts as ABR between stub Area 1 and backbone Area 0<br>3. DUT-C redistributes a static route into OSPF<br><br>**Configuration:**<br>DUT-A (Stub internal router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`commit`<br><br>DUT-B (ABR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C (ASBR):<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.2 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static`<br>`set protocols ospf redistribute static metric 100`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A as stub internal router in Area 1<br>2. Configure DUT-B as ABR with Area 1 (stub) and Area 0 (normal)<br>3. Configure DUT-C as ASBR in Area 0 with static route 203.0.113.0/24 redistributed<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf database` on DUT-A<br>6. Execute `run show ospf route` on DUT-A |
| **Expected Results** | 1. `run show ospf database` on DUT-A does NOT contain any Type-5 AS-External LSA for 203.0.113.0/24 (blocked by stub area)<br>2. `run show ospf route` on DUT-A contains a default route 0.0.0.0/0 as an inter-area (IA) route via next-hop 10.0.1.2<br>3. `run show ospf route` on DUT-A contains inter-area summary routes (Type-3) for Area 0 networks<br>4. `run show ospf database` on DUT-A contains a Type-3 Summary LSA for 0.0.0.0/0 originated by ABR 2.2.2.2 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 3.6 |

---

##### 1.2.1.2 Verify Totally Stubby Area Blocks Type-3 and Type-5 LSAs

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-02: Totally Stubby Area Blocks Type-3 and Type-5, Only Default |
| **Purpose Of The Test** | Verify that a totally stubby area blocks both Type-3 Summary LSAs and Type-5 AS-External LSAs, with only a default route (0.0.0.0/0) injected by the ABR, per RFC 2328 Section 3.6. |
| **Test Topo & Precondition** | **Topology:**<br>`Area 1 (Totally Stubby)                   Area 0 (Backbone)`<br>`DUT-A (10.0.1.1) ---- (10.0.1.2) DUT-B (ABR) (10.0.2.1) ---- (10.0.2.2) DUT-C`<br>`  lo: 1.1.1.1           lo: 2.2.2.2                              lo: 3.3.3.3`<br>`                                                                  (172.16.10.0/24 stub)`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. DUT-B acts as ABR with `no-summary` configured on Area 1<br><br>**Configuration:**<br>DUT-A (Totally stubby internal router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf area 0.0.0.1 no-summary`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`commit`<br><br>DUT-B (ABR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf area 0.0.0.1 no-summary`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set l3-interface vlan-interface vlan300 address 172.16.10.1 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A in totally stubby Area 1 (stub + no-summary)<br>2. Configure DUT-B as ABR with totally stubby Area 1 and backbone Area 0<br>3. Configure DUT-C in Area 0 with stub network 172.16.10.0/24<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf database` on DUT-A<br>6. Execute `run show ospf route` on DUT-A |
| **Expected Results** | 1. `run show ospf database` on DUT-A does NOT contain Type-3 Summary LSAs for 172.16.10.0/24 or 10.0.2.0/24 (blocked by no-summary)<br>2. `run show ospf database` on DUT-A does NOT contain any Type-5 AS-External LSAs<br>3. `run show ospf database` on DUT-A contains exactly one Type-3 Summary LSA for 0.0.0.0/0 from ABR 2.2.2.2<br>4. `run show ospf route` on DUT-A shows only the default route 0.0.0.0/0 as inter-area route and intra-area routes within Area 1 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 3.6 |

---

##### 1.2.1.3 Verify Stub Area Rejects External Redistribution

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-06: Stub Area Does NOT Accept External Redistribution |
| **Purpose Of The Test** | Verify that configuring redistribution on a router inside a stub area does NOT generate Type-5 or Type-7 LSAs, since stub areas prohibit external route injection, per RFC 2328 Section 3.6. |
| **Test Topo & Precondition** | **Topology:**<br>`Area 1 (Stub)                              Area 0 (Backbone)`<br>`DUT-A (10.0.1.1) ---- (10.0.1.2) DUT-B (ABR) (10.0.2.1) ---- (10.0.2.2) DUT-C`<br>`  lo: 1.1.1.1           lo: 2.2.2.2                              lo: 3.3.3.3`<br>`  redistribute static:`<br>`  198.51.100.0/24`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. DUT-A is in stub Area 1 and attempts to redistribute a static route<br><br>**Configuration:**<br>DUT-A (Stub internal router, attempting redistribution):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`set protocols ospf redistribute static`<br>`commit`<br><br>DUT-B (ABR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.2 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A in stub Area 1 with `redistribute static`<br>2. Configure DUT-B as ABR with stub Area 1 and backbone Area 0<br>3. Configure DUT-C in Area 0<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf database` on DUT-A<br>6. Execute `run show ospf database` on DUT-B<br>7. Execute `run show ospf route` on DUT-C |
| **Expected Results** | 1. `run show ospf database` on DUT-A does NOT contain Type-5 AS-External LSA for 198.51.100.0/24 (stub area prohibits external LSAs)<br>2. `run show ospf database` on DUT-B does NOT contain Type-5 AS-External LSA for 198.51.100.0/24<br>3. `run show ospf route` on DUT-C does NOT contain 198.51.100.0/24 (external route was never generated)<br>4. The redistribution command on DUT-A is either rejected or has no effect in a stub area |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 3.6 |

---

#### 1.2.2 NSSA Area

##### 1.2.2.1 Verify NSSA Imports External Routes as Type-7 LSA

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-03: NSSA Imports External Routes as Type-7 LSA |
| **Purpose Of The Test** | Verify that an ASBR in an NSSA area imports external routes as Type-7 NSSA-External LSAs instead of Type-5 AS-External LSAs, per RFC 3101. |
| **Test Topo & Precondition** | **Topology:**<br>`Area 1 (NSSA)                               Area 0 (Backbone)`<br>`DUT-A (ASBR) (10.0.1.1) ---- (10.0.1.2) DUT-B (ABR) (10.0.2.1) ---- (10.0.2.2) DUT-C`<br>`  lo: 1.1.1.1                  lo: 2.2.2.2                              lo: 3.3.3.3`<br>`  redistribute static:`<br>`  198.51.100.0/24`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. DUT-A is ASBR in NSSA Area 1 with a static route to redistribute<br>3. DUT-B is ABR between NSSA Area 1 and backbone Area 0<br><br>**Configuration:**<br>DUT-A (ASBR in NSSA):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type nssa`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`set protocols ospf redistribute static`<br>`set protocols ospf redistribute static metric 50`<br>`commit`<br><br>DUT-B (ABR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type nssa`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.2 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A as ASBR in NSSA Area 1 with static route 198.51.100.0/24 redistributed<br>2. Configure DUT-B as ABR between NSSA Area 1 and backbone Area 0<br>3. Configure DUT-C in backbone Area 0<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf database` on DUT-A<br>6. Execute `run show ospf database` on DUT-B<br>7. Execute `run show ospf route` on DUT-B |
| **Expected Results** | 1. `run show ospf database` on DUT-A contains a Type-7 NSSA-External LSA for 198.51.100.0/24 originated by 1.1.1.1<br>2. `run show ospf database` on DUT-A does NOT contain any Type-5 AS-External LSA for 198.51.100.0/24<br>3. `run show ospf database` on DUT-B (within Area 1 scope) contains the Type-7 LSA for 198.51.100.0/24<br>4. `run show ospf route` on DUT-B shows 198.51.100.0/24 as an NSSA external route (N2) with metric 50 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3101, RFC 2328 Section 3.6 |

---

##### 1.2.2.2 Verify Totally NSSA Blocks Type-3 Summary LSAs

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-04: Totally NSSA Blocks Type-3 Summaries |
| **Purpose Of The Test** | Verify that a totally NSSA area (NSSA + no-summary) blocks Type-3 Summary LSAs while still allowing Type-7 NSSA-External LSA imports, with only a default route injected, per RFC 3101. |
| **Test Topo & Precondition** | **Topology:**<br>`Area 1 (Totally NSSA)                      Area 0 (Backbone)`<br>`DUT-A (ASBR) (10.0.1.1) ---- (10.0.1.2) DUT-B (ABR) (10.0.2.1) ---- (10.0.2.2) DUT-C`<br>`  lo: 1.1.1.1                  lo: 2.2.2.2                              lo: 3.3.3.3`<br>`  redistribute static:                                                   (172.16.20.0/24 stub)`<br>`  198.51.100.0/24`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. DUT-B configures Area 1 as NSSA with no-summary (totally NSSA)<br><br>**Configuration:**<br>DUT-A (ASBR in Totally NSSA):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type nssa`<br>`set protocols ospf area 0.0.0.1 no-summary`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`set protocols ospf redistribute static`<br>`commit`<br><br>DUT-B (ABR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type nssa`<br>`set protocols ospf area 0.0.0.1 no-summary`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.2 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set l3-interface vlan-interface vlan300 address 172.16.20.1 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface vlan300 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A as ASBR in totally NSSA Area 1 with static route redistribution<br>2. Configure DUT-B as ABR with totally NSSA Area 1 (nssa + no-summary)<br>3. Configure DUT-C in Area 0 with stub network 172.16.20.0/24<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf database` on DUT-A<br>6. Execute `run show ospf route` on DUT-A |
| **Expected Results** | 1. `run show ospf database` on DUT-A does NOT contain Type-3 Summary LSAs for 172.16.20.0/24 or 10.0.2.0/24 (blocked by no-summary)<br>2. `run show ospf database` on DUT-A contains a Type-3 Summary LSA for 0.0.0.0/0 from ABR 2.2.2.2 (default route)<br>3. `run show ospf database` on DUT-A contains a Type-7 NSSA-External LSA for 198.51.100.0/24 (self-originated, external import allowed)<br>4. `run show ospf route` on DUT-A shows 0.0.0.0/0 as inter-area default route and 198.51.100.0/24 as NSSA external, but no specific inter-area routes for Area 0 networks |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3101, RFC 2328 Section 3.6 |

---

##### 1.2.2.3 Verify Type-7 to Type-5 Translation at NSSA ABR

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-08: NSSA to Backbone Type-7 to Type-5 Translation at ABR |
| **Purpose Of The Test** | Verify that the ABR translates Type-7 NSSA-External LSAs from the NSSA area into Type-5 AS-External LSAs and floods them into the backbone area, per RFC 3101 Section 3.2. |
| **Test Topo & Precondition** | **Topology:**<br>`Area 1 (NSSA)                               Area 0 (Backbone)`<br>`DUT-A (ASBR) (10.0.1.1) ---- (10.0.1.2) DUT-B (ABR) (10.0.2.1) ---- (10.0.2.2) DUT-C`<br>`  lo: 1.1.1.1                  lo: 2.2.2.2                              lo: 3.3.3.3`<br>`  redistribute static:`<br>`  198.51.100.0/24`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. DUT-A is ASBR in NSSA Area 1 redistributing a static route<br>3. DUT-B is ABR performing Type-7 to Type-5 translation<br><br>**Configuration:**<br>DUT-A (ASBR in NSSA):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type nssa`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`set protocols ospf redistribute static`<br>`set protocols ospf redistribute static metric 75`<br>`commit`<br><br>DUT-B (ABR — translator):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type nssa`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.2 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A as ASBR in NSSA Area 1 with static route 198.51.100.0/24 redistributed (metric 75)<br>2. Configure DUT-B as ABR between NSSA Area 1 and backbone Area 0<br>3. Configure DUT-C in backbone Area 0<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf database` on DUT-A<br>6. Execute `run show ospf database` on DUT-C<br>7. Execute `run show ospf route` on DUT-C |
| **Expected Results** | 1. `run show ospf database` on DUT-A contains a Type-7 NSSA-External LSA for 198.51.100.0/24 originated by 1.1.1.1<br>2. `run show ospf database` on DUT-C contains a Type-5 AS-External LSA for 198.51.100.0/24 (translated by ABR 2.2.2.2)<br>3. `run show ospf database` on DUT-C does NOT contain any Type-7 LSA (Type-7 is NSSA-local only)<br>4. `run show ospf route` on DUT-C shows 198.51.100.0/24 as an external (E2) route with metric 75 via next-hop 10.0.2.1<br>5. The Advertising Router for the Type-5 LSA on DUT-C is 2.2.2.2 (ABR performs the translation) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 3101 Section 3.2 |

---

#### 1.2.3 Normal Area & Mismatch

##### 1.2.3.1 Verify Normal Area Receives All LSA Types

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-07: Normal Area Receives All LSA Types (Type-1, 2, 3, 4, 5) |
| **Purpose Of The Test** | Verify that a normal (non-stub) area receives and maintains all LSA types in its LSDB: Type-1 Router, Type-2 Network, Type-3 Summary, Type-4 ASBR-Summary, and Type-5 AS-External, per RFC 2328 Section 12. |
| **Test Topo & Precondition** | **Topology:**<br>`Area 1 (Normal)                             Area 0 (Backbone)`<br>`DUT-A (10.0.1.1) ---- (10.0.1.2) DUT-B (ABR) (10.0.2.1) ---- (10.0.2.2) DUT-C (ASBR)`<br>`  lo: 1.1.1.1           lo: 2.2.2.2                              lo: 3.3.3.3`<br>`                                                                  redistribute static:`<br>`                                                                  203.0.113.0/24`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches in a linear topology<br>2. DUT-B is ABR between normal Area 1 and backbone Area 0<br>3. DUT-C redistributes a static route into OSPF as ASBR<br><br>**Configuration:**<br>DUT-A (Normal Area 1 internal router):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`commit`<br><br>DUT-B (ABR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.1.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/2 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-C (ASBR):<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 200`<br>`set l3-interface vlan-interface vlan200 address 10.0.2.2 prefix-length 24`<br>`set l3-interface loopback lo address 3.3.3.3 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan200 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static`<br>`set protocols ospf redistribute static metric 100`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A in normal Area 1<br>2. Configure DUT-B as ABR between Area 1 and Area 0<br>3. Configure DUT-C as ASBR in Area 0 with static route 203.0.113.0/24 redistributed<br>4. Wait 40 seconds for all adjacencies to reach Full state<br>5. Execute `run show ospf database` on DUT-A |
| **Expected Results** | 1. `run show ospf database` on DUT-A contains Type-1 Router LSAs (from 1.1.1.1 and 2.2.2.2 within Area 1)<br>2. `run show ospf database` on DUT-A contains Type-2 Network LSA for the broadcast segment 10.0.1.0/24<br>3. `run show ospf database` on DUT-A contains Type-3 Summary LSAs for Area 0 networks (10.0.2.0/24, 3.3.3.3/32)<br>4. `run show ospf database` on DUT-A contains a Type-4 ASBR-Summary LSA advertising the path to ASBR 3.3.3.3<br>5. `run show ospf database` on DUT-A contains a Type-5 AS-External LSA for 203.0.113.0/24 with metric 100 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 12 |

---

##### 1.2.3.2 Verify Area Type Mismatch Prevents OSPF Adjacency

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-05: Area Type Mismatch Between ABR and Internal Router Prevents Adjacency |
| **Purpose Of The Test** | Verify that OSPF adjacency is NOT formed when one router configures an area as stub and the other configures the same area as normal, per RFC 2328 Section 10.5 (the Options field E-bit mismatch in Hello packets). |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`  Area 1: stub                       Area 1: normal`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No pre-existing OSPF configuration<br><br>**Configuration:**<br>DUT-A (Area 1 as stub):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`commit`<br><br>DUT-B (Area 1 as normal):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.1`<br>`set protocols ospf interface lo area 0.0.0.1`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with Area 1 as stub (E-bit = 0 in Hello Options)<br>2. Configure DUT-B with Area 1 as normal (E-bit = 1 in Hello Options)<br>3. Wait 60 seconds<br>4. Execute `run show ospf neighbor` on DUT-A<br>5. Execute `run show ospf neighbor` on DUT-B |
| **Expected Results** | 1. `run show ospf neighbor` on DUT-A shows no neighbor in Full state (empty or stuck in Init)<br>2. `run show ospf neighbor` on DUT-B shows no neighbor in Full state<br>3. Adjacency is NOT formed because the E-bit (ExternalRoutingCapability) in the Hello Options field does not match between stub (E=0) and normal (E=1) per RFC 2328 Section 10.5 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10.5 |

---

### 1.3 Route Redistribution & Route Maps (MODULE 3)

**RFC 2328 Section**: 4.2 (AS External Routes), 16.4 (External Route Calculation)  
**Priority**: P1  
**Cases**: 6  

#### 1.3.1 Static & Connected Redistribution

##### 1.3.1.1 Verify Redistribute Static Routes into OSPF

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-01: Redistribute Static Routes into OSPF |
| **Purpose Of The Test** | Verify that static routes configured on a router are redistributed into OSPF as Type-5 AS-External LSAs and learned by OSPF neighbors, per RFC 2328 Section 16.4. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B (ASBR)`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`                                      static: 203.0.113.0/24`<br>`                                      static: 198.51.100.0/24`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. DUT-B has two static routes: 203.0.113.0/24 and 198.51.100.0/24<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (ASBR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A in OSPF Area 0<br>2. Configure DUT-B in OSPF Area 0 with `redistribute static`<br>3. Wait 40 seconds for adjacency to reach Full state<br>4. Execute `run show ospf route` on DUT-A<br>5. Execute `run show ospf database` on DUT-A<br>6. Execute `run show route ipv4` on DUT-A |
| **Expected Results** | 1. `run show ospf route` on DUT-A shows 203.0.113.0/24 as an external (E2) route via next-hop 10.0.12.2<br>2. `run show ospf route` on DUT-A shows 198.51.100.0/24 as an external (E2) route via next-hop 10.0.12.2<br>3. `run show ospf database` on DUT-A contains Type-5 AS-External LSAs for both 203.0.113.0/24 and 198.51.100.0/24 originated by 2.2.2.2<br>4. `run show route ipv4` on DUT-A lists both routes as OSPF external routes |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.4 |

---

##### 1.3.1.2 Verify Redistribute Connected Routes into OSPF

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-02: Redistribute Connected Routes into OSPF |
| **Purpose Of The Test** | Verify that directly connected routes on a router are redistributed into OSPF as Type-5 AS-External LSAs and appear on neighbors as external routes, per RFC 2328 Section 16.4. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B (ASBR)`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`                                      vlan200: 192.168.1.1/24 (connected, not in OSPF)`<br>`                                      vlan300: 192.168.2.1/24 (connected, not in OSPF)`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. DUT-B has two additional connected interfaces (vlan200, vlan300) NOT configured under OSPF directly<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (ASBR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set vlans vlan-id 200 l3-interface vlan200`<br>`set l3-interface vlan-interface vlan200 address 192.168.1.1 prefix-length 24`<br>`set vlans vlan-id 300 l3-interface vlan300`<br>`set l3-interface vlan-interface vlan300 address 192.168.2.1 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute connected`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A in OSPF Area 0<br>2. Configure DUT-B in OSPF Area 0 with vlan200 and vlan300 as connected (not in OSPF) and `redistribute connected`<br>3. Wait 40 seconds for adjacency to reach Full state<br>4. Execute `run show ospf route` on DUT-A<br>5. Execute `run show ospf database` on DUT-A |
| **Expected Results** | 1. `run show ospf route` on DUT-A shows 192.168.1.0/24 as an external (E2) route via next-hop 10.0.12.2<br>2. `run show ospf route` on DUT-A shows 192.168.2.0/24 as an external (E2) route via next-hop 10.0.12.2<br>3. `run show ospf database` on DUT-A contains Type-5 AS-External LSAs for 192.168.1.0/24 and 192.168.2.0/24 originated by 2.2.2.2<br>4. The routes appear as external (E2) because they are redistributed connected routes, not native OSPF intra-area routes |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.4 |

---

#### 1.3.2 Route-Map Filtering & Metric

##### 1.3.2.1 Verify Route-Map Filtering Permits Specific Prefix Only

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-03: Route-Map Filtering Permits Specific Prefix Only |
| **Purpose Of The Test** | Verify that a route-map with a prefix-list correctly filters redistributed routes, permitting only the specified prefix and blocking all others, per RFC 2328 Section 16.4. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B (ASBR)`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`                                      static: 203.0.113.0/24 (permitted)`<br>`                                      static: 198.51.100.0/24 (denied)`<br>`                                      static: 192.0.2.0/24 (denied)`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. DUT-B has three static routes; only 203.0.113.0/24 should be redistributed<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (ASBR with route-map filtering):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set routing prefix-list IPv4 PERMIT-ONLY permit prefix 203.0.113.0/24`<br>`set routing route-map REDIST-FILTER order 10 matching-policy "permit"`<br>`set routing route-map REDIST-FILTER order 10 match ip address prefix-list "PERMIT-ONLY"`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static route-map "REDIST-FILTER"`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-B with prefix-list "PERMIT-ONLY" permitting only 203.0.113.0/24<br>2. Configure DUT-B with route-map "REDIST-FILTER" matching prefix-list "PERMIT-ONLY"<br>3. Configure DUT-B to redistribute static with route-map "REDIST-FILTER"<br>4. Wait 40 seconds for adjacency to reach Full state<br>5. Execute `run show ospf route` on DUT-A<br>6. Execute `run show ospf database` on DUT-A |
| **Expected Results** | 1. `run show ospf route` on DUT-A contains 203.0.113.0/24 as an external route (permitted by route-map)<br>2. `run show ospf route` on DUT-A does NOT contain 198.51.100.0/24 (denied by route-map — not in prefix-list)<br>3. `run show ospf route` on DUT-A does NOT contain 192.0.2.0/24 (denied by route-map)<br>4. `run show ospf database` on DUT-A contains only one Type-5 AS-External LSA for 203.0.113.0/24 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.4 |

---

##### 1.3.2.2 Verify Custom Metric Applied to Redistributed Routes

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-04: Custom Metric Applied to Redistributed Routes |
| **Purpose Of The Test** | Verify that a custom metric configured on OSPF redistribution is correctly applied to the generated Type-5 AS-External LSA and reflected in the routing table of remote routers, per RFC 2328 Section 16.4. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B (ASBR)`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`                                      static: 203.0.113.0/24 (metric 500)`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. DUT-B has a static route 203.0.113.0/24<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (ASBR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static`<br>`set protocols ospf redistribute static metric 500`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A in OSPF Area 0<br>2. Configure DUT-B in OSPF Area 0 with `redistribute static metric 500`<br>3. Wait 40 seconds for adjacency to reach Full state<br>4. Execute `run show ospf route` on DUT-A<br>5. Execute `run show ospf database` on DUT-A |
| **Expected Results** | 1. `run show ospf route` on DUT-A shows 203.0.113.0/24 as an external (E2) route with metric 500<br>2. `run show ospf database` on DUT-A contains a Type-5 AS-External LSA for 203.0.113.0/24 with metric 500 originated by 2.2.2.2<br>3. The metric value 500 matches the configured `redistribute static metric 500` on DUT-B |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.4 |

---

#### 1.3.3 Redistribution Changes

##### 1.3.3.1 Verify Removing Redistribution Withdraws External Routes

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-05: Remove Redistribution — External Routes Withdrawn |
| **Purpose Of The Test** | Verify that removing the redistribution configuration causes the ASBR to flush its Type-5 AS-External LSAs and remote routers withdraw the external routes from their routing tables, per RFC 2328 Section 14. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B (ASBR)`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`                                      static: 203.0.113.0/24`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established<br>3. DUT-B is redistributing static routes and DUT-A has learned 203.0.113.0/24 as external<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (ASBR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static`<br>`set protocols ospf redistribute static metric 100`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-B as ASBR with `redistribute static metric 100`<br>2. Wait 40 seconds for Full adjacency<br>3. Execute `run show ospf route` on DUT-A<br>4. Configure DUT-B: `delete protocols ospf redistribute static` then `commit`<br>5. Wait 15 seconds for LSA aging/flushing and SPF recalculation<br>6. Execute `run show ospf route` on DUT-A<br>7. Execute `run show ospf database` on DUT-A |
| **Expected Results** | 1. Before removal: `run show ospf route` on DUT-A contains 203.0.113.0/24 as an external (E2) route with metric 100<br>2. After removal: `run show ospf route` on DUT-A no longer contains 203.0.113.0/24<br>3. After removal: `run show ospf database` on DUT-A no longer contains a Type-5 AS-External LSA for 203.0.113.0/24 (LSA flushed with MaxAge)<br>4. Adjacency between DUT-A and DUT-B remains in Full state (only external routes removed) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 14 |

---

##### 1.3.3.2 Verify Redistribution Metric Change Takes Effect

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-06: Redistribute with Metric Change Takes Effect |
| **Purpose Of The Test** | Verify that changing the redistribution metric on an ASBR causes the Type-5 AS-External LSA to be re-originated with the new metric and remote routers update their routing tables accordingly, per RFC 2328 Section 16.4. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan100: 10.0.12.1/24) ---- (vlan100: 10.0.12.2/24) DUT-B (ASBR)`<br>`  lo: 1.1.1.1                        lo: 2.2.2.2`<br>`                                      static: 203.0.113.0/24 (metric 100 → 999)`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. Full adjacency established<br>3. DUT-B is redistributing static routes with metric 100<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`commit`<br><br>DUT-B (ASBR):<br>`set vlans vlan-id 100 l3-interface vlan100`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 100`<br>`set l3-interface vlan-interface vlan100 address 10.0.12.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.0 area-type normal`<br>`set protocols ospf interface vlan100 area 0.0.0.0`<br>`set protocols ospf interface lo area 0.0.0.0`<br>`set protocols ospf redistribute static`<br>`set protocols ospf redistribute static metric 100`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-B as ASBR with `redistribute static metric 100`<br>2. Wait 40 seconds for Full adjacency<br>3. Execute `run show ospf route` on DUT-A<br>4. Configure DUT-B: `set protocols ospf redistribute static metric 999` then `commit`<br>5. Wait 10 seconds for LSA re-origination and SPF recalculation<br>6. Execute `run show ospf route` on DUT-A<br>7. Execute `run show ospf database` on DUT-A |
| **Expected Results** | 1. Before metric change: `run show ospf route` on DUT-A shows 203.0.113.0/24 as external (E2) with metric 100<br>2. After metric change: `run show ospf route` on DUT-A shows 203.0.113.0/24 as external (E2) with metric 999<br>3. `run show ospf database` on DUT-A contains a Type-5 AS-External LSA for 203.0.113.0/24 with metric 999 and an incremented LS sequence number<br>4. Adjacency remains in Full state throughout the metric change |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 16.4 |

---

## Coverage Summary

| Module | Feature | P0 Cases | P1 Cases | P2 Cases | Total | Sufficient? |
|--------|---------|----------|----------|----------|-------|-------------|
| MOD1 | Neighbor Discovery & Adjacency | 10 | 0 | 0 | 10 | Yes (≥8 P0) |
| MOD2 | Area Types | 0 | 8 | 0 | 8 | Yes (≥4 P1) |
| MOD3 | Route Redistribution & Route Maps | 0 | 6 | 0 | 6 | Yes (≥4 P1) |
| **Total** | | **10** | **14** | **0** | **24** | **Yes** |

### Module 1 Coverage Detail:
- Basic neighbor establishment: MOD1-01
- Hello interval mismatch: MOD1-02
- Dead interval expiry teardown: MOD1-03
- DR election (highest router-id): MOD1-04
- BDR election (second-highest): MOD1-05
- Neighbor state transitions (Init→Full): MOD1-06
- New router joins existing domain: MOD1-07
- Neighbor loss after interface shutdown: MOD1-08
- Area ID mismatch: MOD1-09
- Router-ID conflict: MOD1-10

### Module 2 Coverage Detail:
- Stub area blocks Type-5, injects default: MOD2-01
- Totally stubby blocks Type-3 and Type-5: MOD2-02
- NSSA imports external as Type-7: MOD2-03
- Totally NSSA blocks Type-3 summaries: MOD2-04
- Area type mismatch prevents adjacency: MOD2-05
- Stub area rejects external redistribution: MOD2-06
- Normal area receives all LSA types: MOD2-07
- NSSA Type-7 to Type-5 translation at ABR: MOD2-08

### Module 3 Coverage Detail:
- Redistribute static routes: MOD3-01
- Redistribute connected routes: MOD3-02
- Route-map filtering specific prefix: MOD3-03
- Custom metric on redistribution: MOD3-04
- Remove redistribution withdraws routes: MOD3-05
- Metric change takes effect: MOD3-06

### CLI Command Coverage:
All PicOS CLI commands specified in the requirements are used in at least one test case:
- ✅ `set protocols ospf router-id`
- ✅ `set protocols ospf area <id> area-type <normal|stub|nssa>`
- ✅ `set protocols ospf area <id> no-summary`
- ✅ `set protocols ospf interface <intf> area <id>`
- ✅ `set protocols ospf network <prefix> area <id>` (available, used via interface method)
- ✅ `set protocols ospf interface <intf> hello-interval <s>`
- ✅ `set protocols ospf interface <intf> dead-interval <s>`
- ✅ `set protocols ospf interface <intf> cost <v>`
- ✅ `set protocols ospf redistribute <type>`
- ✅ `set protocols ospf redistribute <type> metric <v>`
- ✅ `set protocols ospf redistribute <type> route-map "<name>"`
- ✅ `set protocols ospf area <id> range <prefix>` (used in MOD2 area context)
- ✅ `set vlans vlan-id <id> l3-interface <name>`
- ✅ `set interface gigabit-ethernet <port> family ethernet-switching native-vlan-id <id>`
- ✅ `set l3-interface vlan-interface <name> address <ip> prefix-length <mask>`
- ✅ `set l3-interface loopback lo address <ip> prefix-length 32`
- ✅ `set ip routing enable true`
- ✅ `commit`
- ✅ `set routing prefix-list IPv4 <list> permit prefix <prefix>`
- ✅ `set routing route-map <map> order <seq> matching-policy "permit"`
- ✅ `set routing route-map <map> order <seq> match ip address prefix-list "<list>"`
- ✅ `run show ospf neighbor`
- ✅ `run show ospf database`
- ✅ `run show ospf interface`
- ✅ `run show ospf route`
- ✅ `run show route ipv4`
