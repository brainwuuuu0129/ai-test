# PicOS Stacking Functional Test Cases — MOD-1 & MOD-2

**Platform**: PicOS  
**Feature**: Port Pre-Configuration & Inband Management  
**Generated**: 2026-03-16  
**Developer Requirement**: TP-1, TP-2  
**Total Cases**: 27

---

## Table of Contents

- [1. FUNCTIONAL TESTING](#1-functional-testing)
  - [1.1 Port Pre-Configuration (TP-1)](#11-port-pre-configuration-tp-1)
    - [1.1.1 Basic Pre-Configuration](#111-basic-pre-configuration)
    - [1.1.2 Module Feature Interaction](#112-module-feature-interaction)
    - [1.1.3 Pre-Config Persistence](#113-pre-config-persistence)
  - [1.2 Inband Management (TP-2)](#12-inband-management-tp-2)
    - [1.2.1 Basic Inband Connectivity](#121-basic-inband-connectivity)
    - [1.2.2 Inband During Stack Events](#122-inband-during-stack-events)
    - [1.2.3 Inband Stability](#123-inband-stability)
- [Coverage Summary](#coverage-summary)

---

## 1. FUNCTIONAL TESTING

### 1.1 Port Pre-Configuration (TP-1)

#### 1.1.1 Basic Pre-Configuration

##### 1.1.1.1 Pre-configure port on offline member — member joins and config applied

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-01: Port pre-config applied on member join |
| **Purpose Of The Test** | Verify that a port configured on an offline stack member is automatically applied when that member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Host-A ---- (ge-1/0/3 on Unit 3)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. Host-A is connected to port ge-1/0/3 on Unit 3<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface gigabit-ethernet ge-1/0/3 description "Pre-configured-for-Unit3"`<br>`set interface gigabit-ethernet ge-1/0/3 speed 1000`<br>`set interface gigabit-ethernet ge-1/0/3 mtu 9216`<br>`set interface gigabit-ethernet ge-1/0/3 enable true`<br>`commit` |
| **Test Procedure** | 1. Configure port ge-1/0/3 on Unit 3 from the master (Unit 1) while Unit 3 is offline<br>2. Execute `run show running-config interface ge-1/0/3` on the master<br>3. Connect Unit 3 to the stack via stack cable<br>4. Power on Unit 3<br>5. Wait 120 seconds for Unit 3 to boot and join the stack<br>6. Execute `run show stack` on the master<br>7. Execute `run show interface ge-1/0/3` on the master |
| **Expected Results** | 1. Step 2: `show running-config` displays pre-configured description, speed, MTU, and enable state for ge-1/0/3<br>2. Step 6: `show stack` displays Unit 3 in "Ready" state with role "Member"<br>3. Step 7: `show interface ge-1/0/3` displays description "Pre-configured-for-Unit3", speed 1000 Mbps, MTU 9216, and admin status "up" |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.1.2 Pre-configure VLAN assignment on offline member port

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-02: VLAN assignment pre-config on offline member |
| **Purpose Of The Test** | Verify that VLAN membership configured on an offline member port is applied when the member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Host-A (VLAN 100) ---- (ge-1/0/3 on Unit 3)`<br>`Host-B (VLAN 100) ---- (ge-1/0/1 on Unit 1)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. VLAN 100 is created on the stack<br>5. Host-A and Host-B are configured with IP addresses in the same subnet (10.10.100.0/24)<br><br>**Configuration:**<br>Master (Unit 1):<br>`set vlans vlan-id 100 description "Test-VLAN"`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 100`<br>`set interface gigabit-ethernet ge-1/0/1 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/1 family ethernet-switching vlan members 100`<br>`commit` |
| **Test Procedure** | 1. Configure VLAN 100 and assign ge-1/0/3 (Unit 3) and ge-1/0/1 (Unit 1) as access ports in VLAN 100 from the master while Unit 3 is offline<br>2. Execute `run show vlans` on the master<br>3. Execute `run show running-config interface ge-1/0/3` on the master<br>4. Connect Unit 3 to the stack via stack cable and power on<br>5. Wait 120 seconds for Unit 3 to boot and join the stack<br>6. Execute `run show stack` on the master<br>7. Execute `run show vlans vlan-id 100` on the master<br>8. Execute `run show interface ge-1/0/3` on the master<br>9. Initiate ping from Host-A (10.10.100.2) to Host-B (10.10.100.1) |
| **Expected Results** | 1. Step 2: VLAN 100 exists in the VLAN table with description "Test-VLAN"<br>2. Step 3: ge-1/0/3 shows access mode with VLAN 100 membership in running-config<br>3. Step 6: Unit 3 appears in "Ready" state<br>4. Step 7: VLAN 100 member list includes both ge-1/0/1 and ge-1/0/3<br>5. Step 8: ge-1/0/3 shows admin status "up", access mode, VLAN 100<br>6. Step 9: Ping from Host-A to Host-B succeeds with 0% packet loss |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.1.3 Pre-configure IP address on offline member L3 interface

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-03: L3 IP address pre-config on offline member |
| **Purpose Of The Test** | Verify that an IP address configured on a routed interface of an offline member is applied when the member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Router-A (192.168.10.2/24) ---- (ge-1/0/3 on Unit 3, 192.168.10.1/24)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. Router-A interface is configured with 192.168.10.2/24<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface gigabit-ethernet ge-1/0/3 family inet address 192.168.10.1/24`<br>`set interface gigabit-ethernet ge-1/0/3 routing-interface enable`<br>`set interface gigabit-ethernet ge-1/0/3 enable true`<br>`commit` |
| **Test Procedure** | 1. Configure L3 IP address 192.168.10.1/24 on ge-1/0/3 (Unit 3) from the master while Unit 3 is offline<br>2. Execute `run show running-config interface ge-1/0/3` on the master<br>3. Connect Unit 3 to the stack via stack cable and power on<br>4. Wait 120 seconds for Unit 3 to boot and join the stack<br>5. Execute `run show stack` on the master<br>6. Execute `run show interface ge-1/0/3` on the master<br>7. Execute `run show ip interface brief` on the master<br>8. Initiate ping from Router-A (192.168.10.2) to 192.168.10.1 |
| **Expected Results** | 1. Step 2: Running-config shows IP address 192.168.10.1/24 and routing-interface enabled on ge-1/0/3<br>2. Step 5: Unit 3 appears in "Ready" state with role "Member"<br>3. Step 6: ge-1/0/3 shows admin "up", link "up", IP address 192.168.10.1/24<br>4. Step 7: ge-1/0/3 listed with IP 192.168.10.1, status "up/up"<br>5. Step 8: Ping from Router-A to 192.168.10.1 succeeds with 0% packet loss |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.1.4 Remove pre-configured port config before member joins

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-04: Remove pre-config before member join |
| **Purpose Of The Test** | Verify that removing a pre-configured port configuration while the member is still offline results in the member joining with default port settings |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Host-A ---- (ge-1/0/3 on Unit 3)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. Port ge-1/0/3 has been pre-configured with description, speed, and VLAN 100 assignment<br><br>**Configuration:**<br>Master (Unit 1) — pre-existing:<br>`set interface gigabit-ethernet ge-1/0/3 description "Pre-configured-for-Unit3"`<br>`set interface gigabit-ethernet ge-1/0/3 speed 1000`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 100`<br>`commit` |
| **Test Procedure** | 1. Execute `run show running-config interface ge-1/0/3` on the master to confirm pre-configuration exists<br>2. Execute `delete interface gigabit-ethernet ge-1/0/3` on the master<br>3. Execute `commit` on the master<br>4. Execute `run show running-config interface ge-1/0/3` on the master<br>5. Connect Unit 3 to the stack via stack cable and power on<br>6. Wait 120 seconds for Unit 3 to boot and join the stack<br>7. Execute `run show stack` on the master<br>8. Execute `run show interface ge-1/0/3` on the master |
| **Expected Results** | 1. Step 1: Running-config shows the previously configured description, speed, and VLAN membership for ge-1/0/3<br>2. Step 4: Running-config shows no custom configuration for ge-1/0/3 (interface reverts to default)<br>3. Step 7: Unit 3 appears in "Ready" state with role "Member"<br>4. Step 8: ge-1/0/3 shows default settings — no custom description, auto speed negotiation, default VLAN |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.1.5 Pre-configure multiple ports on same offline member

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-05: Multiple port pre-configs on same offline member |
| **Purpose Of The Test** | Verify that multiple ports on the same offline member can be pre-configured simultaneously and all configurations are applied when the member joins |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Host-A (VLAN 100) ---- (ge-1/0/3 on Unit 3)`<br>`Host-B (VLAN 200) ---- (ge-1/0/4 on Unit 3)`<br>`Host-C ---- (ge-1/0/5 on Unit 3, trunk port)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. VLANs 100 and 200 are created on the stack<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 100`<br>`set interface gigabit-ethernet ge-1/0/3 description "Access-VLAN100"`<br>`set interface gigabit-ethernet ge-1/0/4 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/4 family ethernet-switching vlan members 200`<br>`set interface gigabit-ethernet ge-1/0/4 description "Access-VLAN200"`<br>`set interface gigabit-ethernet ge-1/0/5 family ethernet-switching port-mode trunk`<br>`set interface gigabit-ethernet ge-1/0/5 family ethernet-switching vlan members 100`<br>`set interface gigabit-ethernet ge-1/0/5 family ethernet-switching vlan members 200`<br>`set interface gigabit-ethernet ge-1/0/5 description "Trunk-VLAN100-200"`<br>`commit` |
| **Test Procedure** | 1. Configure ge-1/0/3 as access port in VLAN 100, ge-1/0/4 as access port in VLAN 200, and ge-1/0/5 as trunk port carrying VLANs 100 and 200 on the master while Unit 3 is offline<br>2. Execute `run show running-config interface ge-1/0/3` on the master<br>3. Execute `run show running-config interface ge-1/0/4` on the master<br>4. Execute `run show running-config interface ge-1/0/5` on the master<br>5. Connect Unit 3 to the stack via stack cable and power on<br>6. Wait 120 seconds for Unit 3 to boot and join the stack<br>7. Execute `run show stack` on the master<br>8. Execute `run show interface ge-1/0/3` on the master<br>9. Execute `run show interface ge-1/0/4` on the master<br>10. Execute `run show interface ge-1/0/5` on the master<br>11. Execute `run show vlans` on the master |
| **Expected Results** | 1. Steps 2–4: Running-config shows correct configuration for each port (access VLAN 100, access VLAN 200, trunk VLANs 100+200)<br>2. Step 7: Unit 3 appears in "Ready" state with role "Member"<br>3. Step 8: ge-1/0/3 shows access mode, VLAN 100, description "Access-VLAN100", admin "up"<br>4. Step 9: ge-1/0/4 shows access mode, VLAN 200, description "Access-VLAN200", admin "up"<br>5. Step 10: ge-1/0/5 shows trunk mode, VLANs 100 and 200, description "Trunk-VLAN100-200", admin "up"<br>6. Step 11: VLAN 100 member list includes ge-1/0/3 and ge-1/0/5; VLAN 200 member list includes ge-1/0/4 and ge-1/0/5 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

#### 1.1.2 Module Feature Interaction

##### 1.1.2.1 Pre-configure ACL on offline member port

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-06: ACL pre-config on offline member port |
| **Purpose Of The Test** | Verify that an Access Control List (ACL) applied to an offline member port takes effect when the member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Host-A (10.10.10.2/24) ---- (ge-1/0/3 on Unit 3)`<br>`Server (10.10.10.100/24) ---- (ge-1/0/1 on Unit 1)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. VLAN 10 is created; ge-1/0/3 and ge-1/0/1 are in VLAN 10<br>5. Host-A and Server are in the same subnet 10.10.10.0/24<br><br>**Configuration:**<br>Master (Unit 1):<br>`set policy access-list BLOCK_TELNET type ip`<br>`set policy access-list BLOCK_TELNET rule 10 action deny`<br>`set policy access-list BLOCK_TELNET rule 10 match protocol tcp`<br>`set policy access-list BLOCK_TELNET rule 10 match destination-port 23`<br>`set policy access-list BLOCK_TELNET rule 20 action permit`<br>`set policy access-list BLOCK_TELNET rule 20 match protocol any`<br>`set interface gigabit-ethernet ge-1/0/3 access-list in BLOCK_TELNET`<br>`commit` |
| **Test Procedure** | 1. Configure ACL "BLOCK_TELNET" denying TCP port 23 and permitting all other traffic on the master<br>2. Apply ACL to ge-1/0/3 (Unit 3) in the inbound direction while Unit 3 is offline<br>3. Execute `run show running-config policy access-list BLOCK_TELNET` on the master<br>4. Execute `run show running-config interface ge-1/0/3` on the master<br>5. Connect Unit 3 to the stack via stack cable and power on<br>6. Wait 120 seconds for Unit 3 to boot and join the stack<br>7. Execute `run show stack` on the master<br>8. Execute `run show access-list interface ge-1/0/3` on the master<br>9. Initiate ping from Host-A (10.10.10.2) to Server (10.10.10.100)<br>10. Initiate telnet connection from Host-A to Server (10.10.10.100 port 23) |
| **Expected Results** | 1. Step 3: ACL "BLOCK_TELNET" displayed with rule 10 deny TCP/23 and rule 20 permit any<br>2. Step 4: ge-1/0/3 running-config shows ACL "BLOCK_TELNET" applied inbound<br>3. Step 7: Unit 3 appears in "Ready" state with role "Member"<br>4. Step 8: `show access-list interface ge-1/0/3` displays ACL "BLOCK_TELNET" active in inbound direction<br>5. Step 9: Ping from Host-A to Server succeeds with 0% packet loss<br>6. Step 10: Telnet connection from Host-A to Server is refused/dropped (TCP RST or timeout) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.2.2 Pre-configure QoS policy on offline member port

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-07: QoS policy pre-config on offline member port |
| **Purpose Of The Test** | Verify that a QoS policy configured on an offline member port is applied and enforces traffic shaping when the member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Traffic Generator ---- (ge-1/0/3 on Unit 3)`<br>`Traffic Receiver ---- (ge-1/0/1 on Unit 1)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. Traffic generator and receiver are connected and configured<br>5. VLAN 10 is created; ge-1/0/3 and ge-1/0/1 are in VLAN 10<br><br>**Configuration:**<br>Master (Unit 1):<br>`set qos policy-map RATE_LIMIT_50M type ingress`<br>`set qos policy-map RATE_LIMIT_50M class default police rate 50000 burst 1000`<br>`set interface gigabit-ethernet ge-1/0/3 qos policy-map RATE_LIMIT_50M`<br>`commit` |
| **Test Procedure** | 1. Configure QoS policy-map "RATE_LIMIT_50M" with 50 Mbps rate limit on the master<br>2. Apply policy-map to ge-1/0/3 (Unit 3) while Unit 3 is offline<br>3. Execute `run show running-config qos policy-map RATE_LIMIT_50M` on the master<br>4. Execute `run show running-config interface ge-1/0/3` on the master<br>5. Connect Unit 3 to the stack via stack cable and power on<br>6. Wait 120 seconds for Unit 3 to boot and join the stack<br>7. Execute `run show stack` on the master<br>8. Execute `run show qos interface ge-1/0/3` on the master<br>9. Start traffic generator sending 100 Mbps continuous stream through ge-1/0/3<br>10. Wait 30 seconds for traffic to stabilize<br>11. Execute `run show interface ge-1/0/3 counters` on the master |
| **Expected Results** | 1. Step 3: Policy-map "RATE_LIMIT_50M" displayed with 50 Mbps rate and 1000 Kbps burst<br>2. Step 4: ge-1/0/3 running-config shows policy-map "RATE_LIMIT_50M" applied<br>3. Step 7: Unit 3 appears in "Ready" state<br>4. Step 8: `show qos interface ge-1/0/3` displays active policy-map "RATE_LIMIT_50M" with configured rate<br>5. Step 11: Interface counters show ingress throughput rate-limited to approximately 50 Mbps (±5%), with excess traffic counted as dropped |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.2.3 Pre-configure port-channel/LAG with offline member ports

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-08: LAG pre-config with offline member ports |
| **Purpose Of The Test** | Verify that a port-channel (LAG) configured with ports on an offline member becomes operational when the member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Remote Switch ---- (ae1: ge-1/0/3, ge-1/0/4 on Unit 3)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. Remote Switch has LACP port-channel configured with two member ports connected to Unit 3's ge-1/0/3 and ge-1/0/4<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface aggregate-ethernet ae1 aggregated-ether-options lacp active`<br>`set interface gigabit-ethernet ge-1/0/3 ether-options aggregate-ethernet ae1`<br>`set interface gigabit-ethernet ge-1/0/4 ether-options aggregate-ethernet ae1`<br>`set interface aggregate-ethernet ae1 family ethernet-switching port-mode trunk`<br>`set interface aggregate-ethernet ae1 family ethernet-switching vlan members 100`<br>`set interface aggregate-ethernet ae1 family ethernet-switching vlan members 200`<br>`commit` |
| **Test Procedure** | 1. Configure aggregate interface ae1 with LACP active mode and members ge-1/0/3, ge-1/0/4 (Unit 3) on the master while Unit 3 is offline<br>2. Execute `run show running-config interface ae1` on the master<br>3. Execute `run show running-config interface ge-1/0/3` on the master<br>4. Execute `run show running-config interface ge-1/0/4` on the master<br>5. Connect Unit 3 to the stack via stack cable and power on<br>6. Wait 120 seconds for Unit 3 to boot and join the stack<br>7. Execute `run show stack` on the master<br>8. Wait 30 seconds for LACP negotiation<br>9. Execute `run show lacp interface` on the master<br>10. Execute `run show interface ae1` on the master |
| **Expected Results** | 1. Steps 2–4: Running-config shows ae1 with LACP active, ge-1/0/3 and ge-1/0/4 as members, trunk mode with VLANs 100 and 200<br>2. Step 7: Unit 3 appears in "Ready" state<br>3. Step 9: `show lacp interface` displays ae1 with ge-1/0/3 and ge-1/0/4 both in "Collecting/Distributing" state<br>4. Step 10: ae1 shows link "up", operational members 2, trunk mode, VLANs 100 and 200 |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.2.4 Pre-configure spanning-tree settings on offline member port

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-09: STP pre-config on offline member port |
| **Purpose Of The Test** | Verify that spanning-tree parameters (edge port, BPDU guard) configured on an offline member port take effect when the member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Host-A ---- (ge-1/0/3 on Unit 3, STP edge port)`<br>`Remote Switch ---- (ge-1/0/4 on Unit 3, non-edge STP port)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. Spanning-tree (RSTP) is enabled globally on the stack<br>5. VLAN 10 is created; ge-1/0/3 and ge-1/0/4 are in VLAN 10<br><br>**Configuration:**<br>Master (Unit 1):<br>`set protocols rstp`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 10`<br>`set protocols rstp interface ge-1/0/3 edge-port true`<br>`set protocols rstp interface ge-1/0/3 bpdu-guard true`<br>`set interface gigabit-ethernet ge-1/0/4 family ethernet-switching port-mode trunk`<br>`set interface gigabit-ethernet ge-1/0/4 family ethernet-switching vlan members 10`<br>`set protocols rstp interface ge-1/0/4 cost 20000`<br>`commit` |
| **Test Procedure** | 1. Configure STP edge-port and BPDU guard on ge-1/0/3, and STP cost 20000 on ge-1/0/4 (both Unit 3) from the master while Unit 3 is offline<br>2. Execute `run show running-config protocols rstp interface ge-1/0/3` on the master<br>3. Execute `run show running-config protocols rstp interface ge-1/0/4` on the master<br>4. Connect Unit 3 to the stack via stack cable and power on<br>5. Wait 120 seconds for Unit 3 to boot and join the stack<br>6. Execute `run show stack` on the master<br>7. Execute `run show spanning-tree interface ge-1/0/3` on the master<br>8. Execute `run show spanning-tree interface ge-1/0/4` on the master |
| **Expected Results** | 1. Step 2: Running-config shows ge-1/0/3 with edge-port true and bpdu-guard true<br>2. Step 3: Running-config shows ge-1/0/4 with cost 20000<br>3. Step 6: Unit 3 appears in "Ready" state<br>4. Step 7: ge-1/0/3 displays STP state "Forwarding" immediately (edge port behavior), with BPDU guard "enabled"<br>5. Step 8: ge-1/0/4 displays STP path cost 20000, and port transitions through Discarding → Learning → Forwarding |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.2.5 Pre-configure OSPF interface on offline member port

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-10: OSPF interface pre-config on offline member port |
| **Purpose Of The Test** | Verify that OSPF interface parameters configured on an offline member port enable OSPF adjacency formation when the member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`OSPF Neighbor Router (192.168.1.2/24, Area 0) ---- (ge-1/0/3 on Unit 3, 192.168.1.1/24)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. OSPF neighbor router is configured with area 0, hello-interval 10, router-id 2.2.2.2<br>5. Stack router-id is 1.1.1.1<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface gigabit-ethernet ge-1/0/3 family inet address 192.168.1.1/24`<br>`set interface gigabit-ethernet ge-1/0/3 routing-interface enable`<br>`set protocols ospf router-id 1.1.1.1`<br>`set protocols ospf area 0.0.0.0 interface ge-1/0/3`<br>`set protocols ospf area 0.0.0.0 interface ge-1/0/3 hello-interval 10`<br>`set protocols ospf area 0.0.0.0 interface ge-1/0/3 dead-interval 40`<br>`commit` |
| **Test Procedure** | 1. Configure IP address and OSPF area 0 on ge-1/0/3 (Unit 3) from the master while Unit 3 is offline<br>2. Execute `run show running-config protocols ospf` on the master<br>3. Execute `run show running-config interface ge-1/0/3` on the master<br>4. Connect Unit 3 to the stack via stack cable and power on<br>5. Wait 120 seconds for Unit 3 to boot and join the stack<br>6. Execute `run show stack` on the master<br>7. Wait 60 seconds for OSPF adjacency formation<br>8. Execute `run show ip ospf neighbor` on the master<br>9. Execute `run show ip ospf interface ge-1/0/3` on the master<br>10. Execute `run show ip route ospf` on the master |
| **Expected Results** | 1. Step 2: Running-config shows OSPF area 0.0.0.0 with interface ge-1/0/3, hello-interval 10, dead-interval 40<br>2. Step 3: Running-config shows IP address 192.168.1.1/24 and routing-interface enabled<br>3. Step 6: Unit 3 appears in "Ready" state<br>4. Step 8: `show ip ospf neighbor` displays neighbor 2.2.2.2 in "Full" state on ge-1/0/3<br>5. Step 9: ge-1/0/3 shows OSPF interface state "DR" or "BDR", area 0.0.0.0, hello 10, dead 40<br>6. Step 10: OSPF routes learned from neighbor appear in the routing table |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

#### 1.1.3 Pre-Config Persistence

##### 1.1.3.1 Pre-config survives master/standby switchover

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-11: Pre-config persists after master/standby switchover |
| **Purpose Of The Test** | Verify that port pre-configuration for an offline member is retained in running-config after a master/standby switchover occurs |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Host-A ---- (ge-1/0/3 on Unit 3)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. Pre-configuration applied on ge-1/0/3: description, VLAN 100 access, speed 1000<br><br>**Configuration:**<br>Master (Unit 1) — pre-existing:<br>`set interface gigabit-ethernet ge-1/0/3 description "Persist-Test"`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 100`<br>`set interface gigabit-ethernet ge-1/0/3 speed 1000`<br>`commit` |
| **Test Procedure** | 1. Execute `run show running-config interface ge-1/0/3` on the master (Unit 1)<br>2. Execute `run show stack` on the master (Unit 1)<br>3. Execute `request stack switchover` on the master (Unit 1) to trigger failover<br>4. Wait 120 seconds for switchover to complete<br>5. Execute `run show stack` on the new master (Unit 2)<br>6. Execute `run show running-config interface ge-1/0/3` on the new master (Unit 2)<br>7. Connect Unit 3 to the stack via stack cable and power on<br>8. Wait 120 seconds for Unit 3 to boot and join the stack<br>9. Execute `run show stack` on the master<br>10. Execute `run show interface ge-1/0/3` on the master |
| **Expected Results** | 1. Step 1: Pre-configuration for ge-1/0/3 visible (description, VLAN 100, speed 1000)<br>2. Step 5: Unit 2 is now master, Unit 1 is standby; Unit 3 still absent<br>3. Step 6: Running-config on new master still contains ge-1/0/3 pre-config with description "Persist-Test", access VLAN 100, speed 1000 — identical to Step 1<br>4. Step 9: Unit 3 appears in "Ready" state<br>5. Step 10: ge-1/0/3 shows description "Persist-Test", access VLAN 100, speed 1000, admin "up" |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.3.2 Pre-config retained when member leaves stack

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-12: Pre-config retained after member leaves |
| **Purpose Of The Test** | Verify that pre-configured port settings remain in the running-config when a previously online member leaves the stack, and re-apply when the member rejoins |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) ---- [Stack Link] ---- Master (Unit 1)`<br>`Host-A (VLAN 100) ---- (ge-1/0/3 on Unit 3)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. ge-1/0/3 on Unit 3 is configured with access VLAN 100, description "Member3-Port"<br>4. Host-A traffic is passing through ge-1/0/3<br><br>**Configuration:**<br>Master (Unit 1) — pre-existing applied config:<br>`set interface gigabit-ethernet ge-1/0/3 description "Member3-Port"`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 100`<br>`commit` |
| **Test Procedure** | 1. Execute `run show stack` on the master to confirm all 3 units operational<br>2. Execute `run show interface ge-1/0/3` on the master to confirm config applied<br>3. Disconnect Unit 3 from the stack by removing the stack cable<br>4. Wait 60 seconds for the master to detect member loss<br>5. Execute `run show stack` on the master<br>6. Execute `run show running-config interface ge-1/0/3` on the master<br>7. Reconnect Unit 3 to the stack via stack cable<br>8. Wait 120 seconds for Unit 3 to rejoin<br>9. Execute `run show stack` on the master<br>10. Execute `run show interface ge-1/0/3` on the master |
| **Expected Results** | 1. Step 1: All three units visible with Unit 1 master, Unit 2 standby, Unit 3 member<br>2. Step 2: ge-1/0/3 shows access VLAN 100, description "Member3-Port", link "up"<br>3. Step 5: Unit 3 status changes to "Absent" or is removed from stack display<br>4. Step 6: Running-config still contains ge-1/0/3 configuration (description, VLAN 100) despite Unit 3 being absent<br>5. Step 9: Unit 3 reappears in "Ready" state<br>6. Step 10: ge-1/0/3 shows access VLAN 100, description "Member3-Port", admin "up", link "up" |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.3.3 Pre-config on member with hardware port count mismatch

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-13: Pre-config with hardware port count mismatch |
| **Purpose Of The Test** | Verify system behavior when pre-configured ports reference port indices that do not exist on the joining member hardware (e.g., config references ge-1/0/48 but hardware only has 24 ports) |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1, 48-port model) ---- [Stack Link] ---- Standby (Unit 2, 48-port model)`<br>`Member (Unit 3, 24-port model) — disconnected from stack`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 (48-port) is master, Unit 2 (48-port) is standby, both operational<br>3. Unit 3 is a 24-port model, powered off and disconnected from the stack<br>4. Pre-configuration applied on ge-1/0/3 (valid port) and ge-1/0/48 (non-existent on 24-port model)<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface gigabit-ethernet ge-1/0/3 description "Valid-Port"`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 100`<br>`set interface gigabit-ethernet ge-1/0/48 description "Nonexistent-Port"`<br>`set interface gigabit-ethernet ge-1/0/48 family ethernet-switching vlan members 200`<br>`commit` |
| **Test Procedure** | 1. Configure ge-1/0/3 and ge-1/0/48 for Unit 3 from the master while Unit 3 (24-port) is offline<br>2. Execute `run show running-config interface ge-1/0/3` on the master<br>3. Execute `run show running-config interface ge-1/0/48` on the master<br>4. Connect Unit 3 (24-port model) to the stack via stack cable and power on<br>5. Wait 120 seconds for Unit 3 to boot and join the stack<br>6. Execute `run show stack` on the master<br>7. Execute `run show interface ge-1/0/3` on the master<br>8. Execute `run show interface ge-1/0/48` on the master<br>9. Execute `run show logging | grep ge-1/0/48` on the master |
| **Expected Results** | 1. Steps 2–3: Both pre-configurations present in running-config<br>2. Step 6: Unit 3 appears in "Ready" state (stack join not blocked by mismatched config)<br>3. Step 7: ge-1/0/3 shows description "Valid-Port", VLAN 100, admin "up", link "up" — config applied successfully<br>4. Step 8: ge-1/0/48 output indicates port does not exist or shows "not present" status<br>5. Step 9: System log contains a warning message indicating port ge-1/0/48 configuration could not be applied due to hardware mismatch |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P2 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1. Requires mixed-hardware stack (48-port and 24-port models). |

---

##### 1.1.3.4 Pre-config applied correctly after stack reboot

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-14: Pre-config applied after full stack reboot |
| **Purpose Of The Test** | Verify that pre-configured port settings persist through a full stack reboot (all units power-cycled simultaneously) and are correctly applied to all members upon boot |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Host-A (VLAN 100) ---- (ge-1/0/3 on Unit 3)`<br>`Host-B (VLAN 200) ---- (ge-1/0/2 on Unit 2)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. ge-1/0/3 (Unit 3) is configured with access VLAN 100, description "Unit3-Access"<br>4. ge-1/0/2 (Unit 2) is configured with access VLAN 200, description "Unit2-Access"<br>5. Startup-config has been saved<br><br>**Configuration:**<br>Master (Unit 1) — pre-existing saved config:<br>`set interface gigabit-ethernet ge-1/0/3 description "Unit3-Access"`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 100`<br>`set interface gigabit-ethernet ge-1/0/2 description "Unit2-Access"`<br>`set interface gigabit-ethernet ge-1/0/2 family ethernet-switching port-mode access`<br>`set interface gigabit-ethernet ge-1/0/2 family ethernet-switching vlan members 200`<br>`commit` |
| **Test Procedure** | 1. Execute `run show running-config interface ge-1/0/3` on the master<br>2. Execute `run show running-config interface ge-1/0/2` on the master<br>3. Execute `run copy running-config startup-config` on the master<br>4. Execute `request system reboot` on the master to reboot the entire stack<br>5. Wait 300 seconds for all stack members to complete reboot<br>6. Execute `run show stack` on the master<br>7. Execute `run show running-config interface ge-1/0/3` on the master<br>8. Execute `run show running-config interface ge-1/0/2` on the master<br>9. Execute `run show interface ge-1/0/3` on the master<br>10. Execute `run show interface ge-1/0/2` on the master |
| **Expected Results** | 1. Steps 1–2: Pre-existing configuration displayed correctly for both ports<br>2. Step 6: All three units appear in stack — Unit 1 master, Unit 2 standby, Unit 3 member, all "Ready"<br>3. Step 7: ge-1/0/3 running-config matches pre-reboot config (description "Unit3-Access", access VLAN 100)<br>4. Step 8: ge-1/0/2 running-config matches pre-reboot config (description "Unit2-Access", access VLAN 200)<br>5. Step 9: ge-1/0/3 shows admin "up", link "up", access VLAN 100, description "Unit3-Access"<br>6. Step 10: ge-1/0/2 shows admin "up", link "up", access VLAN 200, description "Unit2-Access" |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

##### 1.1.3.5 Pre-config consistency — running-config matches across stack members

| Field | Content |
|-------|---------|
| **Test Name** | PRECONFIG-15: Running-config consistency across stack members |
| **Purpose Of The Test** | Verify that the running-config for pre-configured ports is synchronized and consistent when viewed from any stack member (master, standby, or member) |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Host-A ---- (ge-1/0/3 on Unit 3)`<br>`Host-B ---- (ge-1/0/2 on Unit 2)`<br>`Host-C ---- (ge-1/0/1 on Unit 1)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. ge-1/0/1 (Unit 1) configured with access VLAN 10, description "Unit1-Port"<br>4. ge-1/0/2 (Unit 2) configured with access VLAN 20, description "Unit2-Port"<br>5. ge-1/0/3 (Unit 3) configured with access VLAN 30, description "Unit3-Port"<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface gigabit-ethernet ge-1/0/1 description "Unit1-Port"`<br>`set interface gigabit-ethernet ge-1/0/1 family ethernet-switching vlan members 10`<br>`set interface gigabit-ethernet ge-1/0/2 description "Unit2-Port"`<br>`set interface gigabit-ethernet ge-1/0/2 family ethernet-switching vlan members 20`<br>`set interface gigabit-ethernet ge-1/0/3 description "Unit3-Port"`<br>`set interface gigabit-ethernet ge-1/0/3 family ethernet-switching vlan members 30`<br>`commit` |
| **Test Procedure** | 1. Execute `run show running-config interface ge-1/0/1` on the master (Unit 1)<br>2. Execute `run show running-config interface ge-1/0/2` on the master (Unit 1)<br>3. Execute `run show running-config interface ge-1/0/3` on the master (Unit 1)<br>4. Execute `run show running-config interface ge-1/0/1` on Unit 2 via session redirect<br>5. Execute `run show running-config interface ge-1/0/2` on Unit 2 via session redirect<br>6. Execute `run show running-config interface ge-1/0/3` on Unit 2 via session redirect<br>7. Execute `run show running-config interface ge-1/0/1` on Unit 3 via session redirect<br>8. Execute `run show running-config interface ge-1/0/2` on Unit 3 via session redirect<br>9. Execute `run show running-config interface ge-1/0/3` on Unit 3 via session redirect<br>10. Execute `run show interface ge-1/0/1` on the master<br>11. Execute `run show interface ge-1/0/2` on the master<br>12. Execute `run show interface ge-1/0/3` on the master |
| **Expected Results** | 1. Steps 1–3: Master shows correct running-config for all three interfaces<br>2. Steps 4–6: Unit 2 (standby) shows identical running-config output for all three interfaces as master<br>3. Steps 7–9: Unit 3 (member) shows identical running-config output for all three interfaces as master<br>4. Step 10: ge-1/0/1 shows description "Unit1-Port", VLAN 10, admin "up"<br>5. Step 11: ge-1/0/2 shows description "Unit2-Port", VLAN 20, admin "up"<br>6. Step 12: ge-1/0/3 shows description "Unit3-Port", VLAN 30, admin "up" |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-1 |

---

### 1.2 Inband Management (TP-2)

#### 1.2.1 Basic Inband Connectivity

##### 1.2.1.1 Inband management interface reachable via SSH

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-01: SSH access via inband management interface |
| **Purpose Of The Test** | Verify that the stack inband management interface is reachable via SSH from a remote management station |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Management Station ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface (VLAN 1 SVI) configured with IP 10.0.0.1/24<br>4. SSH service enabled on the stack<br>5. Management Station has IP 10.0.0.100/24 with route to 10.0.0.1<br>6. User account "admin" exists with password configured<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`set system services ssh port 22`<br>`commit` |
| **Test Procedure** | 1. Execute `run show interface vlan vlan1` on the master via console<br>2. Execute `run show system services ssh` on the master via console<br>3. Initiate SSH connection from Management Station: `ssh admin@10.0.0.1`<br>4. Wait 10 seconds for SSH session establishment<br>5. Execute `run show stack` through the SSH session<br>6. Execute `run show interface vlan vlan1` through the SSH session<br>7. Disconnect the SSH session: `exit` |
| **Expected Results** | 1. Step 1: VLAN 1 SVI shows IP 10.0.0.1/24, admin "up", link "up"<br>2. Step 2: SSH service shows "enabled", port 22<br>3. Step 3: SSH connection established successfully with authentication prompt<br>4. Step 5: `show stack` output displays all three units with correct roles — accessible from remote SSH session<br>5. Step 6: VLAN 1 SVI status displayed correctly<br>6. Step 7: SSH session closes cleanly |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2 |

---

##### 1.2.1.2 Inband management interface reachable via SNMP

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-02: SNMP access via inband management interface |
| **Purpose Of The Test** | Verify that the stack inband management interface responds to SNMP queries (v2c and v3) from a remote NMS station |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`NMS Station ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface (VLAN 1 SVI) configured with IP 10.0.0.1/24<br>4. SNMP v2c enabled with community string "public"<br>5. NMS Station has IP 10.0.0.101/24 with snmpwalk/snmpget tools installed<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services snmp community public authorization read-only`<br>`set system services snmp enable true`<br>`commit` |
| **Test Procedure** | 1. Execute `run show system services snmp` on the master via console<br>2. Execute SNMP GET from NMS Station: `snmpget -v2c -c public 10.0.0.1 sysDescr.0`<br>3. Wait 5 seconds for response<br>4. Execute SNMP WALK from NMS Station: `snmpwalk -v2c -c public 10.0.0.1 ifTable`<br>5. Wait 15 seconds for walk completion<br>6. Execute SNMP GET for sysUpTime from NMS Station: `snmpget -v2c -c public 10.0.0.1 sysUpTimeInstance` |
| **Expected Results** | 1. Step 1: SNMP service shows "enabled", community "public" with read-only access<br>2. Step 2: SNMP GET returns sysDescr containing "PicOS" and version information<br>3. Step 4: SNMP WALK returns ifTable entries for all stack interfaces including ge-1/0/x ports across all three units<br>4. Step 6: sysUpTimeInstance returns a valid timetick value representing system uptime |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2 |

---

##### 1.2.1.3 Inband management interface handles Syslog output

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-03: Syslog output via inband management interface |
| **Purpose Of The Test** | Verify that the stack sends syslog messages to a remote syslog server through the inband management interface |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Syslog Server (10.0.0.200/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface (VLAN 1 SVI) configured with IP 10.0.0.1/24<br>4. Remote syslog server at 10.0.0.200 listening on UDP port 514<br>5. Syslog server is capturing incoming messages<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system syslog host 10.0.0.200 facility any severity info`<br>`set system syslog host 10.0.0.200 transport udp port 514`<br>`commit` |
| **Test Procedure** | 1. Execute `run show system syslog` on the master via console<br>2. Start packet capture on Syslog Server filtering UDP port 514 from 10.0.0.1<br>3. Shutdown interface ge-1/0/1 on the master: `set interface gigabit-ethernet ge-1/0/1 enable false` then `commit`<br>4. Wait 10 seconds for syslog message generation<br>5. Re-enable interface ge-1/0/1: `set interface gigabit-ethernet ge-1/0/1 enable true` then `commit`<br>6. Wait 10 seconds for syslog message generation<br>7. Stop packet capture on Syslog Server<br>8. Execute `run show logging | tail 20` on the master |
| **Expected Results** | 1. Step 1: Syslog configuration shows host 10.0.0.200, UDP 514, facility any, severity info<br>2. Step 7: Packet capture on Syslog Server shows UDP packets from 10.0.0.1 to port 514 containing interface down and interface up messages for ge-1/0/1<br>3. Step 8: Local log shows interface ge-1/0/1 state change events (down and up) with timestamps |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2 |

---

##### 1.2.1.4 Inband management traffic on non-default VLAN

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-04: Inband management on non-default VLAN |
| **Purpose Of The Test** | Verify that inband management works correctly when configured on a non-default VLAN (e.g., VLAN 999) instead of the default VLAN 1 |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Management Station (10.99.0.100/24) ---- [Trunk Port ge-1/0/48 on Unit 1, VLAN 999] ---- Stack`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. VLAN 999 created as management VLAN<br>4. Management Station connected to ge-1/0/48 on Unit 1 with tagged VLAN 999<br>5. Management Station has IP 10.99.0.100/24<br><br>**Configuration:**<br>Master (Unit 1):<br>`set vlans vlan-id 999 description "Management-VLAN"`<br>`set interface vlan vlan999 family inet address 10.99.0.1/24`<br>`set interface gigabit-ethernet ge-1/0/48 family ethernet-switching port-mode trunk`<br>`set interface gigabit-ethernet ge-1/0/48 family ethernet-switching vlan members 999`<br>`set system services ssh enable true`<br>`commit` |
| **Test Procedure** | 1. Execute `run show vlans vlan-id 999` on the master via console<br>2. Execute `run show interface vlan vlan999` on the master via console<br>3. Initiate ping from Management Station (10.99.0.100) to 10.99.0.1<br>4. Wait 10 seconds for ping results<br>5. Initiate SSH connection from Management Station: `ssh admin@10.99.0.1`<br>6. Wait 10 seconds for SSH session establishment<br>7. Execute `run show stack` through the SSH session<br>8. Execute `run show vlans vlan-id 999` through the SSH session<br>9. Disconnect the SSH session: `exit` |
| **Expected Results** | 1. Step 1: VLAN 999 exists with description "Management-VLAN" and ge-1/0/48 as member<br>2. Step 2: VLAN 999 SVI shows IP 10.99.0.1/24, admin "up", link "up"<br>3. Step 3: Ping from Management Station to 10.99.0.1 succeeds with 0% packet loss<br>4. Step 5: SSH connection established successfully<br>5. Step 7: `show stack` output displays all three units — management accessible via non-default VLAN<br>6. Step 8: VLAN 999 information displayed correctly through SSH session |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2 |

---

#### 1.2.2 Inband During Stack Events

##### 1.2.2.1 Inband continuity during master/standby switchover

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-05: Inband continuity during master/standby switchover |
| **Purpose Of The Test** | Verify inband management connectivity during a master/standby switchover, measuring management downtime |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Management Station (10.0.0.100/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface configured with IP 10.0.0.1/24<br>4. SSH established from Management Station to 10.0.0.1 and verified working<br>5. Management Station has continuous ping running to 10.0.0.1<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`commit` |
| **Test Procedure** | 1. Start continuous ping from Management Station to 10.0.0.1 with timestamps: `ping -D -i 1 10.0.0.1`<br>2. Wait 10 seconds to establish baseline ping response times<br>3. Execute `request stack switchover` on the master (Unit 1) via console<br>4. Wait 180 seconds for switchover to complete<br>5. Stop continuous ping on Management Station and record results<br>6. Execute `run show stack` on the new master (Unit 2)<br>7. Initiate new SSH connection from Management Station: `ssh admin@10.0.0.1`<br>8. Execute `run show stack` through the SSH session |
| **Expected Results** | 1. Step 2: Baseline ping shows consistent response times (e.g., < 5 ms)<br>2. Step 5: Continuous ping log shows packet loss period — management downtime duration recorded. Downtime should not exceed 120 seconds<br>3. Step 6: Unit 2 is now master, Unit 1 is standby; all units in "Ready" state<br>4. Step 7: SSH connection to 10.0.0.1 established successfully after switchover<br>5. Step 8: `show stack` accessible via SSH, displaying updated roles |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2. Record exact management downtime in seconds for KPI tracking. |

---

##### 1.2.2.2 Inband recovery after stack member joins

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-06: Inband management recovery after member join |
| **Purpose Of The Test** | Verify that inband management remains stable and accessible when a new stack member joins the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2)`<br>`Member (Unit 3) — disconnected from stack`<br>`Management Station (10.0.0.100/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby — both operational<br>3. Unit 3 is powered off and disconnected from the stack<br>4. Inband management VLAN interface configured with IP 10.0.0.1/24<br>5. SSH session active from Management Station to 10.0.0.1<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`commit` |
| **Test Procedure** | 1. Start continuous ping from Management Station to 10.0.0.1: `ping -D -i 1 10.0.0.1`<br>2. Establish SSH session from Management Station: `ssh admin@10.0.0.1`<br>3. Wait 10 seconds to confirm stable management<br>4. Connect Unit 3 to the stack via stack cable and power on<br>5. Wait 120 seconds for Unit 3 to boot and join the stack<br>6. Execute `run show stack` through the existing SSH session<br>7. Stop continuous ping on Management Station and record results<br>8. Execute `run show interface vlan vlan1` through the SSH session |
| **Expected Results** | 1. Step 3: Ping and SSH session both stable with consistent response times<br>2. Step 6: `show stack` displays all three units — Unit 1 master, Unit 2 standby, Unit 3 member in "Ready" state<br>3. Step 7: Continuous ping shows zero or near-zero packet loss during member join event<br>4. Step 8: VLAN 1 SVI remains up with IP 10.0.0.1/24 — no disruption to management interface |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2 |

---

##### 1.2.2.3 Inband recovery after stack member leaves

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-07: Inband management recovery after member leave |
| **Purpose Of The Test** | Verify that inband management remains stable when a stack member is removed from the stack |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Management Station (10.0.0.100/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface configured with IP 10.0.0.1/24<br>4. SSH session active from Management Station to 10.0.0.1<br>5. Management uplink is connected to Unit 1 (master)<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`commit` |
| **Test Procedure** | 1. Start continuous ping from Management Station to 10.0.0.1: `ping -D -i 1 10.0.0.1`<br>2. Establish SSH session from Management Station: `ssh admin@10.0.0.1`<br>3. Execute `run show stack` through the SSH session to confirm 3 units<br>4. Disconnect Unit 3 from the stack by removing the stack cable<br>5. Wait 60 seconds for the master to detect member loss<br>6. Execute `run show stack` through the SSH session<br>7. Stop continuous ping on Management Station and record results<br>8. Execute `run show logging | tail 10` through the SSH session |
| **Expected Results** | 1. Step 3: Three units displayed in the stack<br>2. Step 6: `show stack` shows Unit 3 in "Absent" state or removed from the list; Unit 1 master and Unit 2 standby remain operational<br>3. Step 7: Continuous ping shows zero or near-zero packet loss during member leave event — management not disrupted<br>4. Step 8: Log messages indicate Unit 3 departure from the stack with timestamp |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2 |

---

##### 1.2.2.4 Inband behavior during stack link failure

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-08: Inband management during stack link failure |
| **Purpose Of The Test** | Verify inband management behavior when one of the inter-switch stack links fails, measuring any management disruption |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link A] ---- Standby (Unit 2) ---- [Stack Link B] ---- Member (Unit 3)`<br>`Master (Unit 1) ---- [Stack Link C] ---- Member (Unit 3) (ring topology)`<br>`Management Station (10.0.0.100/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Stack is in ring topology (3 stack links forming a ring)<br>4. Inband management VLAN interface configured with IP 10.0.0.1/24<br>5. SSH session active from Management Station to 10.0.0.1<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`commit` |
| **Test Procedure** | 1. Execute `run show stack topology` on the master to confirm ring topology<br>2. Start continuous ping from Management Station to 10.0.0.1: `ping -D -i 1 10.0.0.1`<br>3. Establish SSH session from Management Station: `ssh admin@10.0.0.1`<br>4. Wait 10 seconds to confirm stable baseline<br>5. Disconnect Stack Link A (cable between Unit 1 and Unit 2)<br>6. Wait 60 seconds for stack topology reconvergence<br>7. Execute `run show stack topology` through the SSH session<br>8. Execute `run show stack` through the SSH session<br>9. Stop continuous ping on Management Station and record results<br>10. Reconnect Stack Link A<br>11. Wait 60 seconds for ring topology restoration<br>12. Execute `run show stack topology` through the SSH session |
| **Expected Results** | 1. Step 1: Ring topology confirmed with 3 active stack links<br>2. Step 7: Stack topology shows degraded to chain topology; Unit 1 reaches Unit 2 via Unit 3<br>3. Step 8: All three units still present, roles unchanged, all in "Ready" state<br>4. Step 9: Continuous ping shows minimal packet loss (< 5 packets) during topology reconvergence<br>5. Step 12: Ring topology restored with 3 active stack links after cable reconnection |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2. Record exact packet loss count and reconvergence time. |

---

#### 1.2.3 Inband Stability

##### 1.2.3.1 Concurrent SSH sessions through inband during switchover

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-09: Concurrent SSH sessions during switchover |
| **Purpose Of The Test** | Verify behavior of multiple concurrent SSH sessions through the inband management interface during a master/standby switchover |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Management Station A (10.0.0.100/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br>`Management Station B (10.0.0.101/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br>`Management Station C (10.0.0.102/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface configured with IP 10.0.0.1/24<br>4. SSH service enabled, max-sessions set to allow at least 5 concurrent sessions<br>5. Three management stations available<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`set system services ssh max-sessions 10`<br>`commit` |
| **Test Procedure** | 1. Establish SSH session from Station A: `ssh admin@10.0.0.1` (Session 1)<br>2. Establish SSH session from Station B: `ssh admin@10.0.0.1` (Session 2)<br>3. Establish SSH session from Station C: `ssh admin@10.0.0.1` (Session 3)<br>4. Execute `run show stack` on each session simultaneously to confirm all three active<br>5. Execute `request stack switchover` on the master (Unit 1) via console<br>6. Wait 180 seconds for switchover to complete<br>7. Execute `run show stack` on each SSH session (attempt on all three)<br>8. Record which sessions survived the switchover and which dropped<br>9. Establish new SSH sessions from any disconnected stations: `ssh admin@10.0.0.1`<br>10. Execute `run show stack` through the new sessions |
| **Expected Results** | 1. Step 4: All three SSH sessions active and responsive, `show stack` returns correct output on each<br>2. Step 7: SSH sessions may drop during switchover (expected behavior)<br>3. Step 8: Record count of dropped sessions and time-to-drop<br>4. Step 9: New SSH sessions to 10.0.0.1 established successfully after switchover completes<br>5. Step 10: `show stack` on new sessions shows Unit 2 as master, Unit 1 as standby |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2. Document session survival rate and reconnection time. |

---

##### 1.2.3.2 Inband under high management traffic load

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-10: Inband stability under high management traffic |
| **Purpose Of The Test** | Verify that the inband management interface remains responsive under high management traffic load (concurrent SNMP polls, syslog output, and SSH sessions) |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`NMS Station (10.0.0.101/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br>`Management Station (10.0.0.100/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br>`Syslog Server (10.0.0.200/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface configured with IP 10.0.0.1/24<br>4. SSH, SNMP, and Syslog services enabled<br>5. NMS station has SNMP polling tool capable of rapid polling<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`set system services snmp community public authorization read-only`<br>`set system services snmp enable true`<br>`set system syslog host 10.0.0.200 facility any severity debug`<br>`commit` |
| **Test Procedure** | 1. Establish 5 concurrent SSH sessions from Management Station to 10.0.0.1<br>2. Start SNMP walk loop on NMS Station: `while true; do snmpwalk -v2c -c public 10.0.0.1 ifTable; done`<br>3. Configure syslog severity to "debug" to generate high syslog output volume<br>4. Start continuous ping from Management Station to 10.0.0.1: `ping -D -i 0.2 10.0.0.1` (5 pings/sec)<br>5. Wait 300 seconds under sustained load<br>6. Execute `run show stack` through one SSH session<br>7. Execute `run show system cpu` through one SSH session<br>8. Stop SNMP walk loop on NMS Station<br>9. Stop continuous ping and record results<br>10. Execute `run show interface vlan vlan1 counters` on the master |
| **Expected Results** | 1. Step 5: All 5 SSH sessions remain responsive throughout the 300-second load period<br>2. Step 6: `show stack` returns correct output with acceptable response time (< 5 seconds)<br>3. Step 7: CPU utilization remains below 90% — system not saturated by management traffic<br>4. Step 9: Continuous ping shows < 1% packet loss over the 300-second period<br>5. Step 10: VLAN 1 interface counters show high packet counts with no error increments |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P2 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2. Record CPU utilization peaks and SSH response latency. |

---

##### 1.2.3.3 Inband long-running stability — 24-hour continuous management

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-11: 24-hour continuous inband management stability |
| **Purpose Of The Test** | Verify that the inband management interface remains stable and responsive over a 24-hour continuous operation period |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Management Station (10.0.0.100/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br>`NMS Station (10.0.0.101/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface configured with IP 10.0.0.1/24<br>4. SSH and SNMP services enabled<br>5. Automated monitoring script prepared on Management Station<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`set system services snmp community public authorization read-only`<br>`set system services snmp enable true`<br>`commit` |
| **Test Procedure** | 1. Start continuous ping from Management Station to 10.0.0.1 with logging: `ping -D -i 5 10.0.0.1 > /tmp/ping_24h.log`<br>2. Start SNMP polling script on NMS Station polling sysUpTime every 60 seconds for 24 hours with logging<br>3. Establish SSH session from Management Station and start automated script executing `run show stack` every 300 seconds (5 minutes), logging output with timestamps<br>4. Wait 86400 seconds (24 hours)<br>5. Stop continuous ping and record results from `/tmp/ping_24h.log`<br>6. Stop SNMP polling script and record results<br>7. Stop SSH monitoring script and record results<br>8. Execute `run show system cpu` on the master<br>9. Execute `run show system memory` on the master<br>10. Execute `run show interface vlan vlan1 counters` on the master |
| **Expected Results** | 1. Step 5: 24-hour ping log shows > 99.9% success rate with no sustained outage > 30 seconds<br>2. Step 6: SNMP polling log shows all 1440 polls (every 60s for 24h) returned valid sysUpTime values, monotonically increasing<br>3. Step 7: SSH monitoring log shows all 288 `show stack` executions (every 5 min for 24h) returned valid output with all units in expected roles<br>4. Step 8: CPU utilization within normal range (< 50% idle-state average)<br>5. Step 9: Memory utilization shows no significant growth over 24 hours (no memory leak indication)<br>6. Step 10: VLAN 1 interface counters show no error increments over the 24-hour period |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P2 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2. Requires dedicated 24-hour test window. Record memory and CPU trends. |

---

##### 1.2.3.4 Inband with multiple management protocols simultaneously

| Field | Content |
|-------|---------|
| **Test Name** | INBAND-12: Multiple management protocols simultaneously |
| **Purpose Of The Test** | Verify that the inband management interface supports SSH, SNMP, Syslog, and NTP running simultaneously without conflict or performance degradation |
| **Test Topo & Precondition** | **Topology:**<br>`Master (Unit 1) ---- [Stack Link] ---- Standby (Unit 2) ---- [Stack Link] ---- Member (Unit 3)`<br>`Management Station (10.0.0.100/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br>`NMS Station (10.0.0.101/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br>`Syslog Server (10.0.0.200/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br>`NTP Server (10.0.0.201/24) ---- [L3 Network] ---- (VLAN 1 SVI: 10.0.0.1/24 on Stack)`<br><br>**Preconditions:**<br>1. PicOS 4.6 running on all switches<br>2. Unit 1 is master, Unit 2 is standby, Unit 3 is member — all operational<br>3. Inband management VLAN interface configured with IP 10.0.0.1/24<br>4. SSH, SNMP, Syslog, and NTP services enabled<br>5. NTP server at 10.0.0.201 synchronized and serving time<br><br>**Configuration:**<br>Master (Unit 1):<br>`set interface vlan vlan1 family inet address 10.0.0.1/24`<br>`set system services ssh enable true`<br>`set system services snmp community public authorization read-only`<br>`set system services snmp enable true`<br>`set system syslog host 10.0.0.200 facility any severity info`<br>`set system ntp server 10.0.0.201`<br>`set system ntp enable true`<br>`commit` |
| **Test Procedure** | 1. Establish SSH session from Management Station: `ssh admin@10.0.0.1`<br>2. Start SNMP polling from NMS Station: `snmpwalk -v2c -c public 10.0.0.1 system`<br>3. Start packet capture on Syslog Server filtering UDP port 514<br>4. Execute `run show system ntp associations` through the SSH session<br>5. Shutdown and re-enable interface ge-1/0/1 to generate syslog events: `set interface gigabit-ethernet ge-1/0/1 enable false` then `commit`, wait 5 seconds, `set interface gigabit-ethernet ge-1/0/1 enable true` then `commit`<br>6. Wait 30 seconds for all protocols to process<br>7. Execute `run show system services ssh` through the SSH session<br>8. Execute SNMP GET from NMS Station: `snmpget -v2c -c public 10.0.0.1 sysUpTimeInstance`<br>9. Stop packet capture on Syslog Server<br>10. Execute `run show system ntp status` through the SSH session<br>11. Execute `run show system cpu` through the SSH session |
| **Expected Results** | 1. Step 1: SSH session established and responsive<br>2. Step 2: SNMP walk returns complete system group MIB objects<br>3. Step 4: NTP associations show server 10.0.0.201 with "synchronized" or "reach" status<br>4. Step 8: SNMP GET returns valid sysUpTimeInstance value<br>5. Step 9: Syslog server packet capture contains interface down/up events from 10.0.0.1<br>6. Step 10: NTP status shows synchronization with 10.0.0.201, stratum value present, offset within acceptable range<br>7. Step 11: CPU utilization remains below 80% with all four management protocols active simultaneously |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-2 |

---

## Coverage Summary

### Module Coverage Matrix

| Module ID | Module Name | Sub-Feature | P0 Cases | P1 Cases | P2 Cases | Total |
|-----------|-------------|-------------|----------|----------|----------|-------|
| MOD-1 (1.1) | Port Pre-Configuration | 1.1.1 Basic Pre-Configuration | 3 | 1 | 0 | 4 |
| MOD-1 (1.1) | Port Pre-Configuration | 1.1.1 Basic Pre-Configuration (multi-port) | 1 | 0 | 0 | 1 |
| MOD-1 (1.1) | Port Pre-Configuration | 1.1.2 Module Feature Interaction | 0 | 5 | 0 | 5 |
| MOD-1 (1.1) | Port Pre-Configuration | 1.1.3 Pre-Config Persistence | 2 | 1 | 1 | 4 |
| MOD-1 (1.1) | Port Pre-Configuration | 1.1.3 Pre-Config Persistence (reboot) | 1 | 0 | 0 | 1 |
| MOD-2 (1.2) | Inband Management | 1.2.1 Basic Inband Connectivity | 2 | 2 | 0 | 4 |
| MOD-2 (1.2) | Inband Management | 1.2.2 Inband During Stack Events | 3 | 1 | 0 | 4 |
| MOD-2 (1.2) | Inband Management | 1.2.3 Inband Stability | 0 | 2 | 2 | 4 |

### Priority Distribution

| Priority | MOD-1 (Pre-Config) | MOD-2 (Inband) | Total |
|----------|---------------------|-----------------|-------|
| **P0** | 7 | 5 | **12** |
| **P1** | 6 | 5 | **11** |
| **P2** | 2 | 2 | **4** |
| **Total** | **15** | **12** | **27** |

### Feature Coverage Checklist

| # | Coverage Item | Status |
|---|---------------|--------|
| 1 | Pre-config basic port settings (speed, MTU, description) | Covered (PRECONFIG-01) |
| 2 | Pre-config VLAN assignment (access/trunk) | Covered (PRECONFIG-02, -05) |
| 3 | Pre-config L3 IP address | Covered (PRECONFIG-03) |
| 4 | Pre-config removal before member join | Covered (PRECONFIG-04) |
| 5 | Pre-config multiple ports on same member | Covered (PRECONFIG-05) |
| 6 | Pre-config ACL interaction | Covered (PRECONFIG-06) |
| 7 | Pre-config QoS interaction | Covered (PRECONFIG-07) |
| 8 | Pre-config LAG/port-channel interaction | Covered (PRECONFIG-08) |
| 9 | Pre-config STP interaction | Covered (PRECONFIG-09) |
| 10 | Pre-config OSPF interaction | Covered (PRECONFIG-10) |
| 11 | Pre-config survives switchover | Covered (PRECONFIG-11) |
| 12 | Pre-config retained on member leave | Covered (PRECONFIG-12) |
| 13 | Pre-config hardware mismatch | Covered (PRECONFIG-13) |
| 14 | Pre-config after stack reboot | Covered (PRECONFIG-14) |
| 15 | Pre-config consistency across members | Covered (PRECONFIG-15) |
| 16 | Inband SSH access | Covered (INBAND-01) |
| 17 | Inband SNMP access | Covered (INBAND-02) |
| 18 | Inband Syslog output | Covered (INBAND-03) |
| 19 | Inband non-default VLAN | Covered (INBAND-04) |
| 20 | Inband during switchover (downtime measurement) | Covered (INBAND-05) |
| 21 | Inband during member join | Covered (INBAND-06) |
| 22 | Inband during member leave | Covered (INBAND-07) |
| 23 | Inband during stack link failure | Covered (INBAND-08) |
| 24 | Concurrent SSH during switchover | Covered (INBAND-09) |
| 25 | Inband under high traffic load | Covered (INBAND-10) |
| 26 | Inband 24-hour stability | Covered (INBAND-11) |
| 27 | Inband multiple protocols simultaneously | Covered (INBAND-12) |

### Developer Requirement Traceability

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| **TP-1** (Port Pre-Configuration) | PRECONFIG-01 through PRECONFIG-15 | 15 cases |
| **TP-2** (Inband Management) | INBAND-01 through INBAND-12 | 12 cases |

---

*End of document — 27 test cases total*
