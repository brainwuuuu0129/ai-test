# Example Test Cases — PicOS OSPF Functional Testing (FS.COM Table Format)

These examples demonstrate the required output format for generated test cases.

---

## 1. FUNCTIONAL TESTING

### 1.1 Neighbor Discovery & Adjacency

#### 1.1.1 Basic Neighbor Formation

##### 1.1.1.1 Verify basic OSPF neighbor establishment with default parameters

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-01: Basic Neighbor Establishment |
| **Purpose Of The Test** | Verify that two PicOS switches form an OSPF Full adjacency when configured in the same area with matching parameters, per RFC 2328 Section 10.1. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan10: 10.1.1.1/24) ---- (vlan10: 10.1.1.2/24) DUT-B`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No prior OSPF configuration on either switch<br>3. STP disabled or converged<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 10 l3-interface vlan10`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 10`<br>`set l3-interface vlan-interface vlan10 address 10.1.1.1 prefix-length 24`<br>`set l3-interface loopback lo address 1.1.1.1 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf network 10.1.1.0/24 area 0.0.0.0`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 10 l3-interface vlan10`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 10`<br>`set l3-interface vlan-interface vlan10 address 10.1.1.2 prefix-length 24`<br>`set l3-interface loopback lo address 2.2.2.2 prefix-length 32`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf network 10.1.1.0/24 area 0.0.0.0`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with OSPF in Area 0 on vlan10<br>2. Configure DUT-B with OSPF in Area 0 on vlan10<br>3. Wait 45 seconds for OSPF adjacency to form<br>4. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. DUT-A shows DUT-B (2.2.2.2) as neighbor in "Full/DR" or "Full/Backup" state<br>2. The neighbor address is 10.1.1.2<br>3. RXmtL, RqstL, DBsmL counters are all 0 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10.1, 10.3 |

---

#### 1.1.2 Parameter Mismatch

##### 1.1.2.1 Verify hello interval mismatch prevents OSPF adjacency

| Field | Content |
|-------|---------|
| **Test Name** | MOD1-02: Hello Interval Mismatch Prevents Adjacency |
| **Purpose Of The Test** | Verify that two PicOS switches do NOT form OSPF adjacency when hello-interval values are mismatched, per RFC 2328 Section 10.5. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (vlan10: 10.1.1.1/24, hello=10s) ---- (vlan10: 10.1.1.2/24, hello=20s) DUT-B`<br><br>**Preconditions:**<br>1. Two PicOS 4.6 switches connected via ge-1/1/1<br>2. No prior OSPF neighbor relationship<br><br>**Configuration:**<br>DUT-A:<br>`set vlans vlan-id 10 l3-interface vlan10`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 10`<br>`set l3-interface vlan-interface vlan10 address 10.1.1.1 prefix-length 24`<br>`set ip routing enable true`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf interface vlan10 area 0.0.0.0`<br>`set protocols ospf interface vlan10 hello-interval 10`<br>`commit`<br><br>DUT-B:<br>`set vlans vlan-id 10 l3-interface vlan10`<br>`set interface gigabit-ethernet ge-1/1/1 family ethernet-switching native-vlan-id 10`<br>`set l3-interface vlan-interface vlan10 address 10.1.1.2 prefix-length 24`<br>`set ip routing enable true`<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf interface vlan10 area 0.0.0.0`<br>`set protocols ospf interface vlan10 hello-interval 20`<br>`commit` |
| **Test Procedure** | 1. Configure DUT-A with hello-interval 10 on vlan10<br>2. Configure DUT-B with hello-interval 20 on vlan10<br>3. Wait 60 seconds<br>4. Execute `run show ospf neighbor` on DUT-A |
| **Expected Results** | 1. DUT-A neighbor table does NOT contain DUT-B (2.2.2.2)<br>2. No "Full" state neighbor is listed |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 10.5 |

---

### 1.2 Area Types

#### 1.2.1 Stub Area

##### 1.2.1.1 Verify stub area blocks Type-5 LSAs and injects default route

| Field | Content |
|-------|---------|
| **Test Name** | MOD2-01: Stub Area Blocks External Routes |
| **Purpose Of The Test** | Verify that a PicOS switch in a stub area does not receive Type-5 LSAs (external routes) and instead receives a default route from the ABR, per RFC 2328 Section 3.6. |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (Stub Area 1) ---- DUT-B (ABR: Area 0 + Area 1) ---- DUT-C (Area 0, redistributes static)`<br><br>**Preconditions:**<br>1. Three PicOS 4.6 switches<br>2. DUT-C has a static route configured and redistributed into OSPF<br>3. Area 1 configured as stub on both DUT-A and DUT-B<br><br>**Configuration:**<br>DUT-A:<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf network 10.1.1.0/24 area 0.0.0.1`<br>`commit`<br><br>DUT-B (ABR):<br>`set protocols ospf router-id 2.2.2.2`<br>`set protocols ospf area 0.0.0.1 area-type stub`<br>`set protocols ospf network 10.1.1.0/24 area 0.0.0.1`<br>`set protocols ospf network 10.2.2.0/24 area 0.0.0.0`<br>`commit`<br><br>DUT-C:<br>`set protocols ospf router-id 3.3.3.3`<br>`set protocols ospf network 10.2.2.0/24 area 0.0.0.0`<br>`set protocols ospf redistribute static`<br>`commit` |
| **Test Procedure** | 1. Configure all three switches with OSPF<br>2. Wait 60 seconds for OSPF convergence<br>3. Execute `run show ospf database` on DUT-A<br>4. Execute `run show route ipv4` on DUT-A |
| **Expected Results** | 1. DUT-A OSPF database does NOT contain any Type-5 AS-External LSAs<br>2. DUT-A routing table contains a default route (0.0.0.0/0) via DUT-B with OSPF metric<br>3. DUT-A does NOT have an explicit route to 192.168.100.0/24 as an OSPF external route |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | RFC 2328 Section 3.6, 12 |
