# PicOS Stacking Functional Test Cases — MOD-4: CoPP Rate Allocation

**Platform**: PicOS  
**Feature**: Stacking CoPP Rate Division  
**Generated**: 2026-03-16  
**Developer Requirement**: TP-4, TP-5, TP-6  
**Total Cases**: 25

---

## Table of Contents

- [1.4 CoPP Rate Allocation in Stacking](#14-copp-rate-allocation-in-stacking)
  - [1.4.1 Basic CoPP Rate Division](#141-basic-copp-rate-division)
    - [1.4.1.1 Two-Device Stack Rate Division](#1411-two-device-stack-rate-division)
    - [1.4.1.2 Three-Device Stack Rate Division](#1412-three-device-stack-rate-division)
    - [1.4.1.3 Four-Device Stack Rate Division](#1413-four-device-stack-rate-division)
    - [1.4.1.4 All Members Sending Simultaneously Total Rate](#1414-all-members-sending-simultaneously-total-rate)
    - [1.4.1.5 Dynamic Rate Adjustment on Member Count Change](#1415-dynamic-rate-adjustment-on-member-count-change)
  - [1.4.2 Per-Queue CoPP Verification](#142-per-queue-copp-verification)
    - [1.4.2.1 ARP Queue Rate in Stacking](#1421-arp-queue-rate-in-stacking)
    - [1.4.2.2 OSPF Queue Rate in Stacking](#1422-ospf-queue-rate-in-stacking)
    - [1.4.2.3 BGP Queue Rate in Stacking](#1423-bgp-queue-rate-in-stacking)
    - [1.4.2.4 ICMP Queue Rate in Stacking](#1424-icmp-queue-rate-in-stacking)
    - [1.4.2.5 LACP Queue Rate in Stacking](#1425-lacp-queue-rate-in-stacking)
    - [1.4.2.6 STP/BPDU Queue Rate in Stacking](#1426-stpbpdu-queue-rate-in-stacking)
  - [1.4.3 CoPP Rate After Stack Events](#143-copp-rate-after-stack-events)
    - [1.4.3.1 Rate After Master/Standby Switchover](#1431-rate-after-masterstandby-switchover)
    - [1.4.3.2 Rate After Member Joins Stack](#1432-rate-after-member-joins-stack)
    - [1.4.3.3 Rate After Member Leaves Stack](#1433-rate-after-member-leaves-stack)
    - [1.4.3.4 Rate After CoPP Limit Value Modification](#1434-rate-after-copp-limit-value-modification)
    - [1.4.3.5 Rate Consistency Across All Members After Config Change](#1435-rate-consistency-across-all-members-after-config-change)
  - [1.4.4 CoPP Burst and Stress](#144-copp-burst-and-stress)
    - [1.4.4.1 Single Member Exceeds Its Rate Share](#1441-single-member-exceeds-its-rate-share)
    - [1.4.4.2 All Members Simultaneously Exceed Display Value](#1442-all-members-simultaneously-exceed-display-value)
    - [1.4.4.3 Protocol Flap Under CoPP Limiting in Stack](#1443-protocol-flap-under-copp-limiting-in-stack)
    - [1.4.4.4 Long-Duration CoPP Rate Accuracy](#1444-long-duration-copp-rate-accuracy)
  - [1.4.5 PicOS vs Ruijie Comparison Points](#145-picos-vs-ruijie-comparison-points)
    - [1.4.5.1 PicOS Single Member Rate Equals Total Divided by N](#1451-picos-single-member-rate-equals-total-divided-by-n)
    - [1.4.5.2 Document Expected Ruijie Behavior for Comparison](#1452-document-expected-ruijie-behavior-for-comparison)
    - [1.4.5.3 PicOS Behavior When Only One Member Receives All Traffic](#1453-picos-behavior-when-only-one-member-receives-all-traffic)
    - [1.4.5.4 Total System Capacity Across All Members](#1454-total-system-capacity-across-all-members)
    - [1.4.5.5 Impact on Protocol Convergence Under CoPP Limiting](#1455-impact-on-protocol-convergence-under-copp-limiting)
- [Coverage Summary](#coverage-summary)

---

## 1.4 CoPP Rate Allocation in Stacking

### 1.4.1 Basic CoPP Rate Division

#### 1.4.1.1 Two-Device Stack Rate Division

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-001: Verify CoPP rate per device equals total/2 in a 2-device stack |
| **Purpose Of The Test** | Verify that when 2 devices form a stack and the CoPP rate limit is configured to 500 pps, each individual device enforces a rate limit of 250 pps (500/2) for control plane traffic |
| **Test Topo & Precondition** | **Topology:**<br>`Traffic Generator TG1 ---- (port 1) Stack-Member-1 (Master) ==stack-link== Stack-Member-2 (Standby) (port 1) ---- Traffic Generator TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master and Member-2 as standby<br>3. Stack is fully formed and stable (all members in ready state)<br>4. Traffic generators TG1 and TG2 connected to ports on Member-1 and Member-2 respectively<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 500`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record the configured rate-limit value<br>2. Execute `run show stack status` to confirm 2 members are active in the stack<br>3. Configure TG1 to send ARP-request broadcast traffic at 400 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` on the stack master to record received/dropped packet counters for Member-1<br>6. Stop TG1 traffic<br>7. Configure TG2 to send ARP-request broadcast traffic at 400 pps towards Member-2 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics` on the stack master to record received/dropped packet counters for Member-2<br>10. Stop TG2 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays rate-limit as 500 pps<br>2. `run show stack status` shows 2 active members<br>3. Member-1 copp statistics show approximately 250 pps received by CPU and approximately 150 pps dropped (400 - 250 = 150 dropped)<br>4. Member-2 copp statistics show approximately 250 pps received by CPU and approximately 150 pps dropped (400 - 250 = 150 dropped)<br>5. Per-device effective rate is 500/2 = 250 pps (±5% tolerance) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. Core CoPP rate division behavior. |

---

#### 1.4.1.2 Three-Device Stack Rate Division

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-002: Verify CoPP rate per device equals total/3 in a 3-device stack |
| **Purpose Of The Test** | Verify that when 3 devices form a stack and the CoPP rate limit is configured to 600 pps, each individual device enforces a rate limit of 200 pps (600/3) for control plane traffic |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 (Member) (port 1) ---- TG3`<br>`TG2 ---- (port 1) Member-2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all three switches<br>2. Three switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable (all members in ready state)<br>4. Traffic generators TG1, TG2, and TG3 connected to ports on Member-1, Member-2, and Member-3 respectively<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 600`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record the configured rate-limit value<br>2. Execute `run show stack status` to confirm 3 members are active in the stack<br>3. Configure TG1 to send ARP-request broadcast traffic at 300 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` on the stack master to record received/dropped packet counters for Member-1<br>6. Stop TG1 traffic<br>7. Configure TG2 to send ARP-request broadcast traffic at 300 pps towards Member-2 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics` on the stack master to record received/dropped packet counters for Member-2<br>10. Stop TG2 traffic<br>11. Configure TG3 to send ARP-request broadcast traffic at 300 pps towards Member-3 port 1<br>12. Wait 30 seconds for rate to stabilize<br>13. Execute `run show copp statistics` on the stack master to record received/dropped packet counters for Member-3<br>14. Stop TG3 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays rate-limit as 600 pps<br>2. `run show stack status` shows 3 active members<br>3. Member-1 copp statistics show approximately 200 pps received by CPU and approximately 100 pps dropped<br>4. Member-2 copp statistics show approximately 200 pps received by CPU and approximately 100 pps dropped<br>5. Member-3 copp statistics show approximately 200 pps received by CPU and approximately 100 pps dropped<br>6. Per-device effective rate is 600/3 = 200 pps (±5% tolerance) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. Core CoPP rate division behavior. |

---

#### 1.4.1.3 Four-Device Stack Rate Division

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-003: Verify CoPP rate per device equals total/4 in a 4-device stack |
| **Purpose Of The Test** | Verify that when 4 devices form a stack and the CoPP rate limit is configured to 500 pps, each individual device enforces a rate limit of 125 pps (500/4) for control plane traffic |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 ==stack-link== Member-4 (port 1) ---- TG4`<br>`TG2 ---- (port 1) Member-2`<br>`TG3 ---- (port 1) Member-3`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all four switches<br>2. Four switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable (all members in ready state)<br>4. Traffic generators TG1–TG4 connected to ports on Member-1 through Member-4 respectively<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 500`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record the configured rate-limit value<br>2. Execute `run show stack status` to confirm 4 members are active in the stack<br>3. Configure TG1 to send ARP-request broadcast traffic at 200 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` on the stack master to record received/dropped counters for Member-1<br>6. Stop TG1 traffic<br>7. Repeat steps 3–6 for TG2 targeting Member-2, TG3 targeting Member-3, and TG4 targeting Member-4<br>8. Execute `run show copp statistics` on the stack master to record final counters for all members |
| **Expected Results** | 1. `run show copp rate-limit` displays rate-limit as 500 pps<br>2. `run show stack status` shows 4 active members<br>3. Each member's copp statistics show approximately 125 pps received by CPU and approximately 75 pps dropped (200 - 125 = 75)<br>4. Per-device effective rate is 500/4 = 125 pps (±5% tolerance) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. Core CoPP rate division behavior. This is the canonical example from the CoPP stacking design document. |

---

#### 1.4.1.4 All Members Sending Simultaneously Total Rate

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-004: Verify total CPU rate across all members does not exceed display value when all members send simultaneously |
| **Purpose Of The Test** | Verify that when all stack members receive control plane traffic simultaneously, the aggregate rate reaching the CPU across all members does not exceed the configured CoPP rate-limit display value |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 ==stack-link== Member-4 (port 1) ---- TG4`<br>`TG2 ---- (port 1) Member-2`<br>`TG3 ---- (port 1) Member-3`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all four switches<br>2. Four switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. Traffic generators TG1–TG4 connected to Member-1 through Member-4 respectively<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 500`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master<br>2. Execute `run show stack status` to confirm 4 members active<br>3. Execute `run show copp statistics` on the stack master to record baseline counters for all members<br>4. Configure TG1, TG2, TG3, and TG4 to simultaneously send ARP-request broadcast traffic at 200 pps each (800 pps total) towards their respective member ports<br>5. Wait 60 seconds for rates to stabilize<br>6. Execute `run show copp statistics` on the stack master to record counters for all members<br>7. Calculate aggregate CPU-received rate across all 4 members from counter deltas<br>8. Stop all traffic generators |
| **Expected Results** | 1. `run show copp rate-limit` displays 500 pps<br>2. Each member receives approximately 125 pps to CPU (500/4 = 125 pps per device)<br>3. Each member drops approximately 75 pps (200 - 125 = 75)<br>4. Aggregate CPU-received rate across all 4 members is approximately 500 pps (±5% tolerance)<br>5. Total aggregate CPU rate does NOT exceed the configured 500 pps display value |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. Critical system-level constraint validation. |

---

#### 1.4.1.5 Dynamic Rate Adjustment on Member Count Change

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-005: Verify CoPP rate per device adjusts dynamically when stack member count changes |
| **Purpose Of The Test** | Verify that when a stack member is added or removed, the per-device CoPP rate is automatically recalculated to total/N where N is the new member count, without requiring manual reconfiguration |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) (port 1) ---- TG2`<br>`Member-3 (not yet stacked, standalone) ---- (stacking cable available)`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all three switches<br>2. Member-1 and Member-2 configured as a 2-device stack<br>3. Member-3 is pre-configured for stacking but not yet connected<br>4. Stack is fully formed and stable with 2 members<br>5. TG1 and TG2 connected to Member-1 and Member-2<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 600`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send ARP-request broadcast traffic at 400 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` on the stack master to record Member-1 CPU-received rate<br>6. Stop TG1 traffic<br>7. Connect Member-3 stacking cable to the stack ring<br>8. Wait 120 seconds for Member-3 to join the stack and reach ready state<br>9. Execute `run show stack status` to confirm 3 members are now active<br>10. Configure TG1 to send ARP-request broadcast traffic at 400 pps towards Member-1 port 1<br>11. Wait 30 seconds for rate to stabilize<br>12. Execute `run show copp statistics` on the stack master to record Member-1 CPU-received rate<br>13. Stop TG1 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays 600 pps<br>2. With 2 members: Member-1 CPU-received rate is approximately 300 pps (600/2)<br>3. `run show stack status` confirms Member-3 joined successfully (3 active members)<br>4. With 3 members: Member-1 CPU-received rate drops to approximately 200 pps (600/3)<br>5. Rate adjustment is automatic — no manual reconfiguration required<br>6. Rate change takes effect within the stack convergence window (≤120 seconds after member joins) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4, TP-5. Dynamic rate recalculation is critical for stacking CoPP correctness. |

---

### 1.4.2 Per-Queue CoPP Verification

#### 1.4.2.1 ARP Queue Rate in Stacking

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-006: Verify ARP queue CoPP rate division in stacking |
| **Purpose Of The Test** | Verify that the ARP-specific CoPP queue rate is correctly divided among stack members (rate per device = ARP queue limit / N) and that ARP packets exceeding the per-device rate are dropped |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1, VLAN 100) Member-1 (Master) ==stack-link== Member-2 (Standby) (port 1, VLAN 100) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. VLAN 100 configured with SVI IP on both members<br>5. TG1 and TG2 connected to Member-1 and Member-2 ports in VLAN 100<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp queue arp rate-limit 400`<br>`set vlans vlan-id 100`<br>`set interface vlan100 address 10.1.1.1/24`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record ARP queue rate-limit<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send ARP-request packets (src MAC: 00:01:00:00:00:01, target IP: 10.1.1.1) at 300 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics queue arp` on the stack master to record ARP queue counters for Member-1<br>6. Stop TG1 traffic<br>7. Configure TG2 to send ARP-request packets at 300 pps towards Member-2 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics queue arp` on the stack master to record ARP queue counters for Member-2<br>10. Stop TG2 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays ARP queue rate-limit as 400 pps<br>2. Member-1 ARP queue statistics show approximately 200 pps received by CPU (400/2) and approximately 100 pps dropped<br>3. Member-2 ARP queue statistics show approximately 200 pps received by CPU (400/2) and approximately 100 pps dropped<br>4. ARP responses are generated only for packets within the per-device rate (200 pps) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. ARP is critical for L2/L3 reachability. |

---

#### 1.4.2.2 OSPF Queue Rate in Stacking

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-007: Verify OSPF queue CoPP rate division in stacking |
| **Purpose Of The Test** | Verify that the OSPF-specific CoPP queue rate is correctly divided among stack members and OSPF Hello/LSA packets exceeding the per-device rate are dropped |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1, IP: 10.1.1.2/24) Member-1 (Master, IP: 10.1.1.1/24) ==stack-link== Member-2 (Standby, IP: 10.2.2.1/24) (port 1, IP: 10.2.2.2/24) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. OSPF is configured on Member-1 port 1 (area 0.0.0.0) and Member-2 port 1 (area 0.0.0.0)<br>5. TG1 and TG2 capable of generating OSPF protocol packets (Hello, protocol 89, dst 224.0.0.5)<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp queue ospf rate-limit 300`<br>`set protocols ospf area 0.0.0.0 interface ge-1/1/1`<br>`set protocols ospf area 0.0.0.0 interface ge-2/1/1`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record OSPF queue rate-limit<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send crafted OSPF Hello packets (protocol 89, dst 224.0.0.5) at 250 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics queue ospf` on the stack master to record OSPF queue counters for Member-1<br>6. Stop TG1 traffic<br>7. Configure TG2 to send crafted OSPF Hello packets at 250 pps towards Member-2 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics queue ospf` on the stack master to record OSPF queue counters for Member-2<br>10. Stop TG2 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays OSPF queue rate-limit as 300 pps<br>2. Member-1 OSPF queue statistics show approximately 150 pps received by CPU (300/2) and approximately 100 pps dropped<br>3. Member-2 OSPF queue statistics show approximately 150 pps received by CPU (300/2) and approximately 100 pps dropped<br>4. Drop counters increment for packets exceeding the per-device share |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. OSPF is a critical routing protocol — excessive drops may cause adjacency flaps. |

---

#### 1.4.2.3 BGP Queue Rate in Stacking

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-008: Verify BGP queue CoPP rate division in stacking |
| **Purpose Of The Test** | Verify that the BGP-specific CoPP queue rate is correctly divided among stack members and BGP packets (TCP port 179) exceeding the per-device rate are dropped |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1, IP: 10.1.1.2/24) Member-1 (Master, IP: 10.1.1.1/24) ==stack-link== Member-2 (Standby, IP: 10.2.2.1/24) (port 1, IP: 10.2.2.2/24) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. BGP is configured on the stack with neighbors reachable via Member-1 and Member-2 ports<br>5. TG1 and TG2 capable of generating TCP packets with dst port 179<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp queue bgp rate-limit 200`<br>`set protocols bgp local-as 65001`<br>`set protocols bgp neighbor 10.1.1.2 remote-as 65002`<br>`set protocols bgp neighbor 10.2.2.2 remote-as 65003`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record BGP queue rate-limit<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send TCP packets with dst port 179 at 150 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics queue bgp` on the stack master to record BGP queue counters for Member-1<br>6. Stop TG1 traffic<br>7. Configure TG2 to send TCP packets with dst port 179 at 150 pps towards Member-2 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics queue bgp` on the stack master to record BGP queue counters for Member-2<br>10. Stop TG2 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays BGP queue rate-limit as 200 pps<br>2. Member-1 BGP queue statistics show approximately 100 pps received by CPU (200/2) and approximately 50 pps dropped<br>3. Member-2 BGP queue statistics show approximately 100 pps received by CPU (200/2) and approximately 50 pps dropped<br>4. Drop counters increment proportionally to excess traffic above 100 pps per device |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. BGP session stability depends on CoPP allowing sufficient BGP traffic. |

---

#### 1.4.2.4 ICMP Queue Rate in Stacking

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-009: Verify ICMP queue CoPP rate division in stacking |
| **Purpose Of The Test** | Verify that the ICMP-specific CoPP queue rate is correctly divided among stack members and ICMP echo-request packets exceeding the per-device rate are dropped |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1, IP: 10.1.1.2/24) Member-1 (Master, IP: 10.1.1.1/24) ==stack-link== Member-2 (Standby, IP: 10.2.2.1/24) (port 1, IP: 10.2.2.2/24) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. L3 interfaces configured on both member ports with IP addresses<br>5. TG1 and TG2 capable of generating ICMP echo-request packets at configurable rates<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp queue icmp rate-limit 1000`<br>`set interface ge-1/1/1 address 10.1.1.1/24`<br>`set interface ge-2/1/1 address 10.2.2.1/24`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record ICMP queue rate-limit<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send ICMP echo-request packets (dst 10.1.1.1) at 800 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics queue icmp` on the stack master to record ICMP queue counters for Member-1<br>6. Stop TG1 traffic<br>7. Configure TG2 to send ICMP echo-request packets (dst 10.2.2.1) at 800 pps towards Member-2 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics queue icmp` on the stack master to record ICMP queue counters for Member-2<br>10. Stop TG2 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays ICMP queue rate-limit as 1000 pps<br>2. Member-1 ICMP queue statistics show approximately 500 pps received by CPU (1000/2) and approximately 300 pps dropped<br>3. Member-2 ICMP queue statistics show approximately 500 pps received by CPU (1000/2) and approximately 300 pps dropped<br>4. ICMP echo-reply is only generated for packets within the per-device rate (500 pps) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. ICMP is lower priority but important for troubleshooting and monitoring. |

---

#### 1.4.2.5 LACP Queue Rate in Stacking

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-010: Verify LACP queue CoPP rate division in stacking |
| **Purpose Of The Test** | Verify that the LACP-specific CoPP queue rate is correctly divided among stack members and LACP PDU packets exceeding the per-device rate are dropped |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1, LAG member) Member-1 (Master) ==stack-link== Member-2 (Standby) (port 1, LAG member) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. LACP is configured on ports connected to TG1 and TG2<br>5. TG1 and TG2 capable of generating LACP PDU packets (dst MAC: 01:80:C2:00:00:02, EtherType: 0x8809)<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp queue lacp rate-limit 200`<br>`set interface ge-1/1/1 ether-options 802.3ad ae1`<br>`set interface ge-2/1/1 ether-options 802.3ad ae1`<br>`set interface ae1 aggregated-ether-options lacp active`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record LACP queue rate-limit<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send LACP PDU packets (EtherType 0x8809, subtype 0x01, dst 01:80:C2:00:00:02) at 150 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics queue lacp` on the stack master to record LACP queue counters for Member-1<br>6. Stop TG1 traffic<br>7. Configure TG2 to send LACP PDU packets at 150 pps towards Member-2 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics queue lacp` on the stack master to record LACP queue counters for Member-2<br>10. Stop TG2 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays LACP queue rate-limit as 200 pps<br>2. Member-1 LACP queue statistics show approximately 100 pps received by CPU (200/2) and approximately 50 pps dropped<br>3. Member-2 LACP queue statistics show approximately 100 pps received by CPU (200/2) and approximately 50 pps dropped<br>4. LACP session state may flap if legitimate LACP PDUs are dropped due to rate limiting |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. LACP timeout depends on receiving PDUs — CoPP drops can break LAG. |

---

#### 1.4.2.6 STP/BPDU Queue Rate in Stacking

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-011: Verify STP/BPDU queue CoPP rate division in stacking |
| **Purpose Of The Test** | Verify that the STP/BPDU-specific CoPP queue rate is correctly divided among stack members and BPDU packets exceeding the per-device rate are dropped |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1, STP enabled) Member-1 (Master) ==stack-link== Member-2 (Standby) (port 1, STP enabled) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. RSTP (Rapid Spanning Tree Protocol) enabled on Member-1 and Member-2 ports<br>5. TG1 and TG2 capable of generating BPDU packets (dst MAC: 01:80:C2:00:00:00, LLC SSAP/DSAP 0x42)<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp queue stp rate-limit 300`<br>`set protocols rstp interface ge-1/1/1`<br>`set protocols rstp interface ge-2/1/1`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record STP queue rate-limit<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send BPDU packets (dst 01:80:C2:00:00:00) at 250 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics queue stp` on the stack master to record STP queue counters for Member-1<br>6. Stop TG1 traffic<br>7. Configure TG2 to send BPDU packets at 250 pps towards Member-2 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics queue stp` on the stack master to record STP queue counters for Member-2<br>10. Stop TG2 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays STP queue rate-limit as 300 pps<br>2. Member-1 STP queue statistics show approximately 150 pps received by CPU (300/2) and approximately 100 pps dropped<br>3. Member-2 STP queue statistics show approximately 150 pps received by CPU (300/2) and approximately 100 pps dropped<br>4. STP topology may become unstable if legitimate BPDUs are dropped due to rate limiting |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. STP convergence relies on timely BPDU reception — CoPP division directly affects loop prevention. |

---

### 1.4.3 CoPP Rate After Stack Events

#### 1.4.3.1 Rate After Master/Standby Switchover

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-012: Verify CoPP rate per device remains correct after master/standby switchover |
| **Purpose Of The Test** | Verify that after a master/standby switchover event, the CoPP rate division (total/N) is maintained correctly on all stack members and the new master enforces the same per-device rate |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master, priority 200) ==stack-link== Member-2 (Standby, priority 150) (port 1) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master (priority 200), Member-2 as standby (priority 150)<br>3. Stack is fully formed and stable<br>4. TG1 and TG2 connected to Member-1 and Member-2 respectively<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 500`<br>`set stack member 1 priority 200`<br>`set stack member 2 priority 150`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master to record rate-limit (500 pps)<br>2. Execute `run show stack status` to confirm Member-1 is master and Member-2 is standby<br>3. Configure TG1 to send ARP-request traffic at 400 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` on the stack master to record Member-1 CPU-received rate (baseline)<br>6. Stop TG1 traffic<br>7. Execute `run request stack master-switchover` on the stack master to trigger switchover<br>8. Wait 120 seconds for switchover to complete and stack to restabilize<br>9. Execute `run show stack status` on the new master (Member-2) to confirm Member-2 is now master<br>10. Configure TG1 to send ARP-request traffic at 400 pps towards Member-1 port 1<br>11. Wait 30 seconds for rate to stabilize<br>12. Execute `run show copp statistics` on the new master (Member-2) to record Member-1 CPU-received rate<br>13. Execute `run show copp rate-limit` on the new master (Member-2)<br>14. Stop TG1 traffic |
| **Expected Results** | 1. Before switchover: Member-1 CPU-received rate is approximately 250 pps (500/2)<br>2. `run show stack status` confirms Member-2 is now master after switchover<br>3. After switchover: `run show copp rate-limit` on new master still shows 500 pps<br>4. After switchover: Member-1 CPU-received rate remains approximately 250 pps (500/2)<br>5. CoPP rate division is preserved across the switchover event — no rate change or temporary unlimited window |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-5. Switchover must not create a CoPP bypass window. |

---

#### 1.4.3.2 Rate After Member Joins Stack

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-013: Verify CoPP rate recalculates when a new member joins the stack |
| **Purpose Of The Test** | Verify that when a new member joins an existing stack, the CoPP per-device rate automatically decreases from total/N to total/(N+1) on all existing and new members |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) (port 1) ---- TG2`<br>`Member-3 (standalone, stacking cable disconnected)`<br>`TG3 ---- (port 1) Member-3`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all three switches<br>2. Member-1 and Member-2 form a 2-device stack<br>3. Member-3 is standalone, pre-configured for stacking, stacking cable not yet connected<br>4. Stack is fully formed and stable with 2 members<br>5. TG1 connected to Member-1, TG2 to Member-2, TG3 to Member-3<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 600`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send ARP-request traffic at 400 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` to record Member-1 CPU-received rate<br>6. Stop TG1 traffic<br>7. Connect Member-3 stacking cable to the stack ring<br>8. Wait 120 seconds for Member-3 to join and reach ready state<br>9. Execute `run show stack status` to confirm 3 members active<br>10. Configure TG1 to send ARP-request traffic at 400 pps towards Member-1 port 1<br>11. Wait 30 seconds for rate to stabilize<br>12. Execute `run show copp statistics` to record Member-1 CPU-received rate after join<br>13. Stop TG1 traffic<br>14. Configure TG3 to send ARP-request traffic at 400 pps towards Member-3 port 1<br>15. Wait 30 seconds for rate to stabilize<br>16. Execute `run show copp statistics` to record Member-3 CPU-received rate<br>17. Stop TG3 traffic |
| **Expected Results** | 1. With 2 members: Member-1 CPU-received rate is approximately 300 pps (600/2)<br>2. `run show stack status` confirms 3 active members after Member-3 joins<br>3. With 3 members: Member-1 CPU-received rate decreases to approximately 200 pps (600/3)<br>4. Member-3 (newly joined) CPU-received rate is also approximately 200 pps (600/3)<br>5. Rate recalculation occurs automatically upon member join |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-5. New member must receive the correct divided rate immediately upon joining. |

---

#### 1.4.3.3 Rate After Member Leaves Stack

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-014: Verify CoPP rate recalculates when a member leaves the stack |
| **Purpose Of The Test** | Verify that when a stack member is removed (cable disconnect or shutdown), the CoPP per-device rate automatically increases from total/N to total/(N-1) on remaining members |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 (Member) (port 1) ---- TG3`<br>`TG2 ---- (port 1) Member-2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all three switches<br>2. Three switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable with 3 members<br>4. TG1, TG2, TG3 connected to Member-1, Member-2, Member-3 respectively<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 600`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master<br>2. Execute `run show stack status` to confirm 3 members active<br>3. Configure TG1 to send ARP-request traffic at 300 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` to record Member-1 CPU-received rate with 3 members<br>6. Stop TG1 traffic<br>7. Disconnect Member-3 stacking cable from the stack ring<br>8. Wait 120 seconds for Member-3 to be detected as departed and stack to reconverge<br>9. Execute `run show stack status` to confirm only 2 members remain active<br>10. Configure TG1 to send ARP-request traffic at 400 pps towards Member-1 port 1<br>11. Wait 30 seconds for rate to stabilize<br>12. Execute `run show copp statistics` to record Member-1 CPU-received rate with 2 members<br>13. Stop TG1 traffic |
| **Expected Results** | 1. With 3 members: Member-1 CPU-received rate is approximately 200 pps (600/3)<br>2. `run show stack status` confirms only 2 active members after Member-3 leaves<br>3. With 2 members: Member-1 CPU-received rate increases to approximately 300 pps (600/2)<br>4. Rate recalculation occurs automatically upon member departure<br>5. No CoPP bypass window during the reconvergence period |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-5. Remaining members must get higher per-device rates after a member departs. |

---

#### 1.4.3.4 Rate After CoPP Limit Value Modification

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-015: Verify per-device CoPP rate updates when CoPP limit value is modified on running stack |
| **Purpose Of The Test** | Verify that when the CoPP rate-limit value is changed via CLI on a running stack, all members immediately adopt the new per-device rate (new_total/N) without requiring a stack restart |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) (port 1) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. Initial CoPP rate-limit configured to 400 pps<br>5. TG1 connected to Member-1<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 400`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` to confirm initial rate-limit is 400 pps<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Configure TG1 to send ARP-request traffic at 300 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` to record Member-1 CPU-received rate (expected ~200 pps = 400/2)<br>6. Stop TG1 traffic<br>7. Configure new CoPP rate-limit on the stack master:<br>`set protocols copp rate-limit 800`<br>`commit`<br>8. Wait 10 seconds for configuration to propagate<br>9. Execute `run show copp rate-limit` to confirm new rate-limit is 800 pps<br>10. Configure TG1 to send ARP-request traffic at 500 pps towards Member-1 port 1<br>11. Wait 30 seconds for rate to stabilize<br>12. Execute `run show copp statistics` to record Member-1 CPU-received rate (expected ~400 pps = 800/2)<br>13. Stop TG1 traffic |
| **Expected Results** | 1. Initial `run show copp rate-limit` shows 400 pps<br>2. With rate-limit 400 pps and 2 members: Member-1 CPU-received rate is approximately 200 pps (400/2)<br>3. After modification: `run show copp rate-limit` shows 800 pps<br>4. With rate-limit 800 pps and 2 members: Member-1 CPU-received rate increases to approximately 400 pps (800/2)<br>5. Configuration change takes effect immediately without stack restart |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-6. Runtime CoPP modification must propagate to all members. |

---

#### 1.4.3.5 Rate Consistency Across All Members After Config Change

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-016: Verify CoPP rate is consistent across all stack members after configuration change |
| **Purpose Of The Test** | Verify that after changing the CoPP rate-limit on the master, all stack members (master, standby, and regular members) enforce the identical per-device rate — no member has stale or inconsistent rate values |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 (Member) (port 1) ---- TG3`<br>`TG2 ---- (port 1) Member-2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all three switches<br>2. Three switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. TG1, TG2, TG3 connected to Member-1, Member-2, Member-3 respectively<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 300`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` to confirm initial rate-limit is 300 pps<br>2. Execute `run show stack status` to confirm 3 members active<br>3. Configure new CoPP rate-limit:<br>`set protocols copp rate-limit 900`<br>`commit`<br>4. Wait 10 seconds for configuration to propagate to all members<br>5. Execute `run show copp rate-limit` to confirm new rate-limit is 900 pps<br>6. Configure TG1 to send ARP-request traffic at 500 pps towards Member-1 port 1<br>7. Wait 30 seconds for rate to stabilize<br>8. Execute `run show copp statistics` to record Member-1 CPU-received rate<br>9. Stop TG1 traffic<br>10. Configure TG2 to send ARP-request traffic at 500 pps towards Member-2 port 1<br>11. Wait 30 seconds for rate to stabilize<br>12. Execute `run show copp statistics` to record Member-2 CPU-received rate<br>13. Stop TG2 traffic<br>14. Configure TG3 to send ARP-request traffic at 500 pps towards Member-3 port 1<br>15. Wait 30 seconds for rate to stabilize<br>16. Execute `run show copp statistics` to record Member-3 CPU-received rate<br>17. Stop TG3 traffic |
| **Expected Results** | 1. `run show copp rate-limit` shows 900 pps after change<br>2. Member-1 CPU-received rate is approximately 300 pps (900/3)<br>3. Member-2 CPU-received rate is approximately 300 pps (900/3)<br>4. Member-3 CPU-received rate is approximately 300 pps (900/3)<br>5. All three members enforce identical per-device rates (no stale configuration)<br>6. Deviation between any two members is less than 5% |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-6. Configuration consistency across stack is critical — stale rates on any member can cause unpredictable CoPP behavior. |

---

### 1.4.4 CoPP Burst and Stress

#### 1.4.4.1 Single Member Exceeds Its Rate Share

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-017: Verify single member drops excess traffic when receiving more than its CoPP share (total/N) |
| **Purpose Of The Test** | Verify that when a single stack member receives control plane traffic exceeding its per-device CoPP share (total/N), the excess packets are dropped locally and do not affect other members' CoPP budgets |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 ==stack-link== Member-4 (port 1) ---- TG4`<br>`TG2 ---- (port 1) Member-2`<br>`TG3 ---- (port 1) Member-3`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all four switches<br>2. Four switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. TG1–TG4 connected to Member-1 through Member-4<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 500`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master (500 pps, per-device = 125 pps)<br>2. Execute `run show stack status` to confirm 4 members active<br>3. Configure TG1 to send ARP-request traffic at 500 pps towards Member-1 port 1 (4x its share)<br>4. Configure TG2 to send ARP-request traffic at 50 pps towards Member-2 port 1 (under its share)<br>5. Start TG1 and TG2 simultaneously<br>6. Wait 60 seconds for rate to stabilize<br>7. Execute `run show copp statistics` to record CPU-received and dropped counters for Member-1 and Member-2<br>8. Stop all traffic |
| **Expected Results** | 1. Member-1 CPU-received rate is approximately 125 pps (500/4), NOT 500 pps — drops approximately 375 pps<br>2. Member-2 CPU-received rate is approximately 50 pps (below its 125 pps share) — drops 0 pps<br>3. Member-1's excess traffic does NOT consume Member-2's unused CoPP budget<br>4. Each member's rate limiting is independent and enforced locally<br>5. `run show copp statistics` on Member-1 shows a high drop counter; Member-2 shows zero or near-zero drops |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. PicOS design: rate is divided and enforced per device. Unused budget on one member cannot be borrowed by another. |

---

#### 1.4.4.2 All Members Simultaneously Exceed Display Value

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-018: Verify CoPP behavior when all members simultaneously receive traffic exceeding the display value |
| **Purpose Of The Test** | Verify system stability when all stack members simultaneously receive control plane traffic that, in aggregate, far exceeds the configured CoPP rate-limit display value — each member should independently enforce its share |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 ==stack-link== Member-4 (port 1) ---- TG4`<br>`TG2 ---- (port 1) Member-2`<br>`TG3 ---- (port 1) Member-3`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all four switches<br>2. Four switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. TG1–TG4 connected to Member-1 through Member-4<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 500`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` on the stack master (500 pps)<br>2. Execute `run show stack status` to confirm 4 members active<br>3. Configure TG1, TG2, TG3, and TG4 to each send ARP-request traffic at 1000 pps towards their respective member ports (4000 pps total, 8x display value)<br>4. Start all four traffic generators simultaneously<br>5. Wait 60 seconds for rate to stabilize<br>6. Execute `run show copp statistics` to record CPU-received and dropped counters for all 4 members<br>7. Execute `run show cpu-utilization` on the stack master to record CPU usage<br>8. Execute `run show stack status` to confirm stack stability (no member departures)<br>9. Stop all traffic generators<br>10. Wait 30 seconds<br>11. Execute `run show stack status` to confirm stack remains stable |
| **Expected Results** | 1. Each member's CPU-received rate is approximately 125 pps (500/4 = 125 pps)<br>2. Each member drops approximately 875 pps (1000 - 125 = 875)<br>3. Total aggregate CPU-received rate across all members is approximately 500 pps<br>4. CPU utilization on stack master does not exceed critical threshold (e.g., 90%)<br>5. `run show stack status` shows all 4 members remain active — no member ejected due to overload<br>6. Stack remains stable throughout the stress test |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4, TP-5. Stress test for extreme overload scenario. Stack stability under sustained attack-level traffic is critical. |

---

#### 1.4.4.3 Protocol Flap Under CoPP Limiting in Stack

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-019: Verify protocol session stability under CoPP rate limiting in a stack environment |
| **Purpose Of The Test** | Verify that OSPF adjacency and LACP bundle remain stable when legitimate protocol traffic competes with high-volume control plane noise under CoPP rate limiting in a stack |
| **Test Topo & Precondition** | **Topology:**<br>`Router-A (OSPF, IP: 10.1.1.2/24) ---- (port 1) Member-1 (Master, IP: 10.1.1.1/24) ==stack-link== Member-2 (Standby) (port 1, LAG ae1) ---- Partner-Switch (LAG)`<br>`TG1 ---- (port 2) Member-1`<br>`TG2 ---- (port 1) Member-2 (port 2) ---- TG3`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both stack members<br>2. Two switches configured as a stack with Member-1 as master<br>3. OSPF adjacency established between Member-1 port 1 and Router-A<br>4. LACP bundle (ae1) established between Member-2 port 1 and Partner-Switch<br>5. TG1 connected to Member-1 port 2, TG2/TG3 connected to Member-2 ports<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 200`<br>`set protocols ospf area 0.0.0.0 interface ge-1/1/1`<br>`set interface ge-2/1/1 ether-options 802.3ad ae1`<br>`set interface ae1 aggregated-ether-options lacp active`<br>`commit` |
| **Test Procedure** | 1. Execute `run show ospf neighbor` to confirm OSPF adjacency is FULL with Router-A<br>2. Execute `run show lacp interface ae1` to confirm LACP bundle is active<br>3. Execute `run show copp rate-limit` to confirm 200 pps (per-device = 100 pps)<br>4. Configure TG1 to send mixed broadcast/multicast traffic (ARP + random multicast) at 500 pps towards Member-1 port 2<br>5. Configure TG2 to send mixed broadcast/multicast traffic at 500 pps towards Member-2<br>6. Start TG1 and TG2 simultaneously<br>7. Wait 300 seconds (5 minutes) with traffic running<br>8. Execute `run show ospf neighbor` to record OSPF adjacency state<br>9. Execute `run show lacp interface ae1` to record LACP bundle state<br>10. Execute `run show copp statistics` to record drop counters for all queues<br>11. Execute `run show log messages` to search for OSPF adjacency flap or LACP timeout log entries<br>12. Stop all traffic generators |
| **Expected Results** | 1. CoPP drops noise traffic — drop counters show significant drops on both members<br>2. OSPF adjacency state: If OSPF Hello rate fits within the 100 pps per-device OSPF queue allocation, adjacency remains FULL; if OSPF queue is shared with noise and drops OSPF Hellos, adjacency may flap — log entries show "OSPF neighbor down"<br>3. LACP bundle state: If LACP PDU rate fits within the per-device LACP queue allocation, bundle remains active; if LACP PDUs are dropped, bundle may flap — log entries show "LACP timeout"<br>4. Protocol flap behavior is documented: specific queue saturation conditions that cause flaps are identified<br>5. `run show log messages` entries correlate with CoPP drop events |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4, TP-6. This test documents the threshold at which CoPP rate division causes protocol instability. Critical for capacity planning. |

---

#### 1.4.4.4 Long-Duration CoPP Rate Accuracy

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-020: Verify CoPP rate accuracy remains stable over 1-hour sustained traffic |
| **Purpose Of The Test** | Verify that the per-device CoPP rate (total/N) is maintained accurately over a sustained 1-hour period without drift, memory leak, or counter overflow affecting the rate enforcement |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) (port 1) ---- TG2`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on both switches<br>2. Two switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. TG1 and TG2 connected to Member-1 and Member-2 respectively<br>5. System uptime > 10 minutes (past initial stabilization)<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 500`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` to confirm 500 pps<br>2. Execute `run show stack status` to confirm 2 members active<br>3. Execute `run show copp statistics` to record baseline counters (T0)<br>4. Configure TG1 to send ARP-request traffic at 400 pps towards Member-1 port 1<br>5. Configure TG2 to send ARP-request traffic at 400 pps towards Member-2 port 1<br>6. Start TG1 and TG2 simultaneously<br>7. Wait 900 seconds (15 minutes)<br>8. Execute `run show copp statistics` to record counters (T1)<br>9. Wait 900 seconds (15 minutes, cumulative 30 minutes)<br>10. Execute `run show copp statistics` to record counters (T2)<br>11. Wait 900 seconds (15 minutes, cumulative 45 minutes)<br>12. Execute `run show copp statistics` to record counters (T3)<br>13. Wait 900 seconds (15 minutes, cumulative 60 minutes)<br>14. Execute `run show copp statistics` to record counters (T4)<br>15. Execute `run show cpu-utilization` to record CPU usage after 1 hour<br>16. Execute `run show system memory` to record memory usage after 1 hour<br>17. Stop all traffic generators |
| **Expected Results** | 1. At each 15-minute interval (T1, T2, T3, T4), Member-1 CPU-received rate is approximately 250 pps (500/2) — calculated as delta/interval<br>2. At each interval, Member-2 CPU-received rate is approximately 250 pps (500/2)<br>3. Rate deviation between any two intervals is less than 5%<br>4. No rate drift over time (T4 rate ≈ T1 rate)<br>5. CPU utilization remains stable — no gradual increase indicating a leak<br>6. Memory usage remains stable — no gradual increase indicating a leak<br>7. CoPP counters do not overflow (64-bit counters expected) |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. Long-duration stability test. Counter overflow or memory leaks may not surface in short tests. |

---

### 1.4.5 PicOS vs Ruijie Comparison Points

#### 1.4.5.1 PicOS Single Member Rate Equals Total Divided by N

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-021: Document and verify PicOS CoPP behavior — single member rate equals total/N |
| **Purpose Of The Test** | Explicitly verify and document the PicOS CoPP stacking design: in an N-device stack, each device's effective CoPP rate is CLI_display_value / N. This is the defining behavioral characteristic of the PicOS implementation |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 ==stack-link== Member-4 (port 1) ---- TG4`<br>`TG2 ---- (port 1) Member-2`<br>`TG3 ---- (port 1) Member-3`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all four switches<br>2. Four switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. TG1 connected to Member-1 only (single member targeted)<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 1000`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` to confirm 1000 pps<br>2. Execute `run show stack status` to confirm 4 members active<br>3. Configure TG1 to send ARP-request traffic at 500 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `run show copp statistics` to record Member-1 CPU-received rate<br>6. Stop TG1 traffic<br>7. Configure TG1 to send ARP-request traffic at 250 pps towards Member-1 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `run show copp statistics` to record Member-1 CPU-received rate<br>10. Stop TG1 traffic<br>11. Configure TG1 to send ARP-request traffic at 200 pps towards Member-1 port 1<br>12. Wait 30 seconds for rate to stabilize<br>13. Execute `run show copp statistics` to record Member-1 CPU-received rate<br>14. Stop TG1 traffic |
| **Expected Results** | 1. `run show copp rate-limit` displays 1000 pps (CLI display value)<br>2. At 500 pps input: Member-1 CPU-received rate is approximately 250 pps (1000/4 = 250), drops approximately 250 pps — NOT 500 pps or 1000 pps<br>3. At 250 pps input: Member-1 CPU-received rate is approximately 250 pps (at its limit, 0 drops)<br>4. At 200 pps input: Member-1 CPU-received rate is approximately 200 pps (below its limit, 0 drops)<br>5. **PicOS behavior confirmed**: Each device is hard-limited to total/N regardless of other members' utilization |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. Reference test for PicOS vs Ruijie comparison. This documents PicOS's fixed-division model. |

---

#### 1.4.5.2 Document Expected Ruijie Behavior for Comparison

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-022: Document expected Ruijie CoPP behavior — each member full rate with master scheduling |
| **Purpose Of The Test** | Document the Ruijie CoPP stacking design for comparison: in Ruijie's implementation, each device can send up to the full CLI display rate to the CPU, and the master handles scheduling. This test documents the behavioral difference from PicOS |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Ruijie-Member-1 (Master) ==stack-link== Ruijie-Member-2 (Standby) ==stack-link== Ruijie-Member-3 ==stack-link== Ruijie-Member-4 (port 1) ---- TG4`<br>`TG2 ---- (port 1) Ruijie-Member-2`<br>`TG3 ---- (port 1) Ruijie-Member-3`<br><br>**Preconditions:**<br>1. Ruijie switch platform with stacking CoPP support<br>2. Four switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. TG1 connected to Member-1 only (single member targeted)<br>5. **NOTE**: This test is for documentation/comparison only — execute only if Ruijie hardware is available<br><br>**Configuration:**<br>Stack Master:<br>`cpu-protect policy`<br>`rate-limit arp 1000` (Ruijie CLI syntax — adjust per actual platform)<br>`exit` |
| **Test Procedure** | 1. Execute `show cpu-protect policy` (Ruijie CLI) to confirm rate-limit is 1000 pps<br>2. Execute `show switch` (Ruijie CLI) to confirm 4 members active<br>3. Configure TG1 to send ARP-request traffic at 1500 pps towards Member-1 port 1<br>4. Wait 30 seconds for rate to stabilize<br>5. Execute `show cpu-protect statistics` (Ruijie CLI) to record Member-1 CPU-received rate<br>6. Stop TG1 traffic<br>7. Configure TG1 to send ARP-request traffic at 800 pps towards Member-1 port 1<br>8. Wait 30 seconds for rate to stabilize<br>9. Execute `show cpu-protect statistics` (Ruijie CLI) to record Member-1 CPU-received rate<br>10. Stop TG1 traffic |
| **Expected Results** | 1. `show cpu-protect policy` displays rate-limit as 1000 pps<br>2. **Ruijie expected behavior**: At 1500 pps input, Member-1 CPU-received rate is approximately 1000 pps (full display value, NOT 250 pps = 1000/4)<br>3. At 800 pps input: Member-1 CPU-received rate is approximately 800 pps (below limit, 0 drops)<br>4. **Ruijie design**: Each member can individually consume up to the full CLI display rate; the master handles aggregate scheduling across the stack<br>5. **Comparison conclusion**: PicOS allows 250 pps per device in a 4-stack with 1000 pps limit; Ruijie allows 1000 pps per device with master scheduling |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P2 |
| **Hardware Model** | Ruijie Stack-capable Switches (comparison reference) |
| **Version** | Ruijie OS (version TBD) |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. Comparison documentation only. Execute if Ruijie hardware is available. Results inform PicOS design trade-off analysis. |

---

#### 1.4.5.3 PicOS Behavior When Only One Member Receives All Traffic

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-023: Verify PicOS CoPP behavior when only one member receives all control plane traffic |
| **Purpose Of The Test** | Verify that in PicOS, when only one stack member receives control plane traffic and other members are idle, the receiving member is still limited to total/N — it cannot use other members' unused CoPP budget (unlike Ruijie where the single member could use the full rate) |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 ==stack-link== Member-4`<br>(No traffic generators connected to Member-2, Member-3, Member-4)<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all four switches<br>2. Four switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. Only TG1 is connected to Member-1; no external traffic sources on other members<br>5. Member-2, Member-3, Member-4 have zero control plane traffic ingress<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 1000`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` to confirm 1000 pps<br>2. Execute `run show stack status` to confirm 4 members active<br>3. Execute `run show copp statistics` to confirm zero traffic counters on Members 2, 3, and 4<br>4. Configure TG1 to send ARP-request traffic at 1000 pps towards Member-1 port 1<br>5. Wait 60 seconds for rate to stabilize<br>6. Execute `run show copp statistics` to record CPU-received and dropped counters for Member-1<br>7. Execute `run show copp statistics` to confirm Members 2, 3, 4 still have zero or near-zero traffic<br>8. Stop TG1 traffic |
| **Expected Results** | 1. Member-1 CPU-received rate is approximately 250 pps (1000/4 = 250) — NOT 1000 pps<br>2. Member-1 drops approximately 750 pps (1000 - 250 = 750)<br>3. Members 2, 3, 4 have zero CPU-received and zero drops<br>4. **PicOS design limitation confirmed**: Unused CoPP budget on idle members (750 pps total unused) is NOT redistributable to Member-1<br>5. Total effective system capacity is 250 pps (only 1 out of 4 shares utilized) despite 1000 pps configured<br>6. **Contrast with Ruijie**: In Ruijie's implementation, Member-1 would receive up to 1000 pps in this scenario |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. This is the key behavioral difference from Ruijie. Documents the worst-case scenario for PicOS CoPP in stacking. |

---

#### 1.4.5.4 Total System Capacity Across All Members

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-024: Verify total CoPP system capacity across all stack members equals CLI display value |
| **Purpose Of The Test** | Verify that when all stack members are simultaneously receiving traffic and each is exactly at its per-device CoPP limit, the total aggregate CPU-received rate across the entire stack equals the CLI display value |
| **Test Topo & Precondition** | **Topology:**<br>`TG1 ---- (port 1) Member-1 (Master) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 ==stack-link== Member-4 (port 1) ---- TG4`<br>`TG2 ---- (port 1) Member-2`<br>`TG3 ---- (port 1) Member-3`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all four switches<br>2. Four switches configured as a stack with Member-1 as master<br>3. Stack is fully formed and stable<br>4. TG1–TG4 connected to Member-1 through Member-4 respectively<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 1000`<br>`commit` |
| **Test Procedure** | 1. Execute `run show copp rate-limit` to confirm 1000 pps<br>2. Execute `run show stack status` to confirm 4 members active<br>3. Execute `run show copp statistics` to record baseline counters for all members (T0)<br>4. Configure TG1, TG2, TG3, TG4 to each send ARP-request traffic at exactly 250 pps towards their respective member ports (per-device share = 1000/4 = 250 pps)<br>5. Start all four traffic generators simultaneously<br>6. Wait 60 seconds for rate to stabilize<br>7. Execute `run show copp statistics` to record counters for all members (T1)<br>8. Calculate per-member CPU-received rate and aggregate rate from counter deltas<br>9. Stop all traffic generators<br>10. Configure TG1, TG2, TG3, TG4 to each send at 300 pps (above per-device share)<br>11. Start all four traffic generators simultaneously<br>12. Wait 60 seconds for rate to stabilize<br>13. Execute `run show copp statistics` to record counters for all members (T2)<br>14. Calculate per-member and aggregate rates<br>15. Stop all traffic generators |
| **Expected Results** | 1. At 250 pps per member (at exact share): Each member CPU-received rate is approximately 250 pps, drops are 0 or near-zero; aggregate rate is approximately 1000 pps (= CLI display value)<br>2. At 300 pps per member (above share): Each member CPU-received rate is approximately 250 pps, drops approximately 50 pps each; aggregate rate is approximately 1000 pps (= CLI display value)<br>3. **PicOS total system capacity**: When all members are fully utilized, the aggregate rate equals the CLI display value — the display value represents the TOTAL system budget, not a per-device budget<br>4. This confirms the PicOS formula: per-device rate = CLI_display / N, total system capacity = CLI_display |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4. Validates the fundamental CoPP stacking equation. Contrast with Ruijie where total system capacity = CLI_display × N. |

---

#### 1.4.5.5 Impact on Protocol Convergence Under CoPP Limiting

| Field | Content |
|-------|---------|
| **Test Name** | MOD4-025: Verify impact of PicOS CoPP rate division on protocol convergence time in stack |
| **Purpose Of The Test** | Measure the impact of the PicOS CoPP rate division on OSPF convergence time after a link failure event. In a 4-device stack with rate-limit 1000 pps, each device's OSPF queue allows only 1/4 of the configured rate — this may slow convergence compared to non-stacked or Ruijie-style implementations |
| **Test Topo & Precondition** | **Topology:**<br>`Router-A (OSPF, area 0, IP: 10.1.1.2/24) ---- (port 1) Member-1 (Master, IP: 10.1.1.1/24) ==stack-link== Member-2 (Standby) ==stack-link== Member-3 ==stack-link== Member-4 (IP: 10.4.4.1/24) (port 1) ---- Router-B (OSPF, area 0, IP: 10.4.4.2/24)`<br>`TG1 ---- (port 2) Member-1`<br>`TG2 ---- (port 1) Member-2`<br>`TG3 ---- (port 1) Member-3`<br>`TG4 ---- (port 2) Member-4`<br><br>**Preconditions:**<br>1. PicOS 4.6 installed on all four stack switches<br>2. Four switches configured as a stack with Member-1 as master<br>3. OSPF area 0 configured between stack and Router-A / Router-B<br>4. OSPF adjacencies are FULL and routes are stable<br>5. Router-B advertises prefix 192.168.0.0/16 via OSPF<br>6. TG1–TG4 generate background CoPP-targeted traffic (ARP broadcast)<br>7. Data-plane traffic from Router-A to 192.168.0.0/16 via stack to Router-B<br><br>**Configuration:**<br>Stack Master:<br>`set protocols copp rate-limit 400`<br>`set protocols ospf area 0.0.0.0 interface ge-1/1/1`<br>`set protocols ospf area 0.0.0.0 interface ge-4/1/1`<br>`commit` |
| **Test Procedure** | 1. Execute `run show ospf neighbor` to confirm FULL adjacency with Router-A and Router-B<br>2. Execute `run show ospf route 192.168.0.0/16` to confirm route is present via Router-B<br>3. Execute `run show copp rate-limit` to confirm 400 pps (per-device = 100 pps in 4-stack)<br>4. Configure TG1, TG2, TG3, TG4 to each send ARP-request broadcast at 200 pps towards their respective member ports (saturating CoPP per-device share)<br>5. Start all traffic generators<br>6. Wait 60 seconds for CoPP rates to stabilize<br>7. Execute `run show copp statistics queue ospf` to record OSPF queue drop counters<br>8. Shutdown the link between Member-4 and Router-B:<br>`set interface ge-4/1/1 disable`<br>`commit`<br>9. Start a timer to measure convergence<br>10. Execute `run show ospf neighbor` repeatedly at 1-second intervals to detect when Router-B adjacency transitions to Down<br>11. Execute `run show ospf route 192.168.0.0/16` repeatedly at 1-second intervals to detect when the route is withdrawn<br>12. Record the convergence time (from link shutdown to route withdrawal)<br>13. Stop all traffic generators<br>14. Re-enable the link:<br>`delete interface ge-4/1/1 disable`<br>`commit`<br>15. Wait 60 seconds for OSPF adjacency to re-establish |
| **Expected Results** | 1. OSPF adjacencies are FULL before the test<br>2. With CoPP background traffic: `run show copp statistics queue ospf` shows non-zero drops on Member-4 (OSPF LSA floods competing with background noise)<br>3. Convergence time after link shutdown is recorded — expected to be longer than non-stacked baseline due to OSPF queue receiving only 100 pps (400/4) instead of 400 pps<br>4. Route 192.168.0.0/16 is eventually withdrawn — convergence completes even under CoPP pressure<br>5. Convergence time is documented for comparison with: (a) non-stacked single device with 400 pps CoPP, (b) Ruijie stack where each device gets full 400 pps OSPF queue<br>6. OSPF adjacency re-establishes after link is restored<br>7. **Documented trade-off**: PicOS CoPP division may increase convergence time proportionally to stack size |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-4, TP-6. Critical for understanding the operational impact of PicOS CoPP division on network convergence. Results should be compared with Ruijie baseline if available. |

---

## Coverage Summary

### Coverage by Sub-Area

| Sub-Area | Description | Test Cases | P0 | P1 | P2 |
|----------|-------------|------------|-----|-----|-----|
| 1.4.1 | Basic CoPP Rate Division | 5 | 4 | 0 | 0 |
| 1.4.2 | Per-Queue CoPP Verification | 6 | 5 | 1 | 0 |
| 1.4.3 | CoPP Rate After Stack Events | 5 | 3 | 2 | 0 |
| 1.4.4 | CoPP Burst and Stress | 4 | 2 | 2 | 0 |
| 1.4.5 | PicOS vs Ruijie Comparison Points | 5 | 3 | 1 | 1 |
| **Total** | | **25** | **17** | **6** | **1** |

### Coverage by Priority

| Priority | Count | Percentage |
|----------|-------|------------|
| P0 | 17 | 68% |
| P1 | 6 | 24% |
| P2 | 1 | 4% |
| **Total** | **25** | **100%** |

### Coverage by Developer Requirement

| Requirement | Description | Covered By Test Cases |
|-------------|-------------|-----------------------|
| TP-4 | CoPP rate division formula (total/N) | MOD4-001 through MOD4-011, MOD4-017 through MOD4-025 |
| TP-5 | Dynamic rate adjustment on stack topology change | MOD4-005, MOD4-012 through MOD4-014, MOD4-018 |
| TP-6 | Runtime CoPP configuration change propagation | MOD4-015, MOD4-016, MOD4-019, MOD4-025 |

### Risk Coverage Matrix

| Risk Area | Risk Level | Test Cases Covering | Count | Sufficient? |
|-----------|------------|---------------------|-------|-------------|
| Rate division correctness | P0 | MOD4-001,002,003,004,005,021,023,024 | 8 | Yes (≥8) |
| Per-queue enforcement | P0 | MOD4-006,007,008,009,010,011 | 6 | Yes (≥5) |
| Stack event handling | P0 | MOD4-012,013,014,015,016 | 5 | Yes (≥5) |
| Stress/overload stability | P1 | MOD4-017,018,019,020 | 4 | Yes (≥4) |
| Vendor comparison documentation | P2 | MOD4-022 | 1 | N/A (documentation) |
| Protocol convergence impact | P1 | MOD4-019,025 | 2 | Yes (≥2) |

### Show Commands Coverage

| Show Command | Used In Test Cases |
|--------------|--------------------|
| `run show copp rate-limit` | All 25 test cases |
| `run show copp statistics` | MOD4-001 through MOD4-025 |
| `run show copp statistics queue <name>` | MOD4-006 through MOD4-011, MOD4-019, MOD4-025 |
| `run show stack status` | All 25 test cases |
| `run show cpu-utilization` | MOD4-018, MOD4-020 |
| `run show system memory` | MOD4-020 |
| `run show ospf neighbor` | MOD4-019, MOD4-025 |
| `run show lacp interface` | MOD4-019 |
| `run show ospf route` | MOD4-025 |
| `run show log messages` | MOD4-019 |

### Key PicOS vs Ruijie Design Differences (Documented)

| Aspect | PicOS Behavior | Ruijie Behavior |
|--------|---------------|-----------------|
| Per-device CoPP rate | CLI_display / N | CLI_display (full rate) |
| Total system capacity | CLI_display | CLI_display × N |
| Rate redistribution | Not supported (fixed division) | Master scheduling allows dynamic allocation |
| Single-member traffic scenario | Limited to CLI_display / N | Can use full CLI_display |
| Impact on protocol convergence | Proportional to N (more members = lower per-device rate) | Minimal (each member has full rate) |
