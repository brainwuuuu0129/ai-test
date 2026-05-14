# PicOS Stacking Functional Test Cases — MOD-3, MOD-5, MOD-6

**Platform**: PicOS  
**Feature**: Forwarding Class / Bulk Config / Protocol-Config Concurrency  
**Generated**: 2026-03-16  
**Developer Requirement**: TP-3, TP-7, TP-8  
**Total Cases**: 28

---

## Table of Contents

- [1.3 Forwarding Class Bandwidth (MOD-3)](#13-forwarding-class-bandwidth-mod-3)
  - [1.3.1 Default Bandwidth Values](#131-default-bandwidth-values)
  - [1.3.2 Bandwidth Adjustment](#132-bandwidth-adjustment)
  - [1.3.3 Bandwidth Persistence](#133-bandwidth-persistence)
- [1.5 Bulk Configuration Reliability (MOD-5)](#15-bulk-configuration-reliability-mod-5)
  - [1.5.1 Bulk VLAN Operations](#151-bulk-vlan-operations)
  - [1.5.2 Bulk ACL/Policy Operations](#152-bulk-aclpolicy-operations)
  - [1.5.3 Configuration Reliability Metrics](#153-configuration-reliability-metrics)
- [1.6 Protocol Packet vs Config Concurrency (MOD-6)](#16-protocol-packet-vs-config-concurrency-mod-6)
  - [1.6.1 Config During Protocol Traffic](#161-config-during-protocol-traffic)
  - [1.6.2 Stress and Stability](#162-stress-and-stability)
- [Coverage Summary](#coverage-summary)

---

## 1.3 Forwarding Class Bandwidth (MOD-3)

### 1.3.1 Default Bandwidth Values

#### 1.3.1.1 Default FC Bandwidth Values Displayed Correctly on All Stack Members

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-001: Default FC bandwidth display on all members |
| **Purpose Of The Test** | Verify that after a stacking system is formed with default configuration, all Forwarding Class (BE, AF1, AF2, AF3, AF4, EF, NC1, NC2) bandwidth values are identical across master and all member switches. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. No custom QoS or FC bandwidth configuration applied (factory default)<br><br>**Configuration:**<br>Default stacking configuration only — no FC bandwidth overrides. |
| **Test Procedure** | 1. Execute `run show stack status` on SW1 to confirm stack is fully formed with all 3 members.<br>2. Execute `run show forwarding-class bandwidth` on SW1 (master).<br>3. Execute `run show forwarding-class bandwidth` on SW2 (standby) via `run show forwarding-class bandwidth member 2`.<br>4. Execute `run show forwarding-class bandwidth` on SW3 (member) via `run show forwarding-class bandwidth member 3`. |
| **Expected Results** | 1. `show stack status` displays 3 members: SW1 (Master), SW2 (Standby), SW3 (Member), all in "Ready" state.<br>2. SW1 shows default FC bandwidth values: BE=5%, AF1=10%, AF2=10%, AF3=10%, AF4=10%, EF=25%, NC1=15%, NC2=15% (or platform-defined defaults).<br>3. SW2 output shows identical FC bandwidth values to SW1.<br>4. SW3 output shows identical FC bandwidth values to SW1. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3 |

---

#### 1.3.1.2 Traffic Forwarded According to Default FC Scheduling Across Members

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-002: Default FC scheduling traffic validation across members |
| **Purpose Of The Test** | Verify that traffic ingressing on different stack members is forwarded according to the default Forwarding Class bandwidth scheduling, with each FC receiving its allocated share under congestion. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member) --- IXIA Port2`<br>Three switches in a ring stacking topology. IXIA traffic generator connected to SW1 ingress and SW3 egress.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. No custom FC bandwidth configuration (factory default)<br>4. IXIA configured with 8 traffic streams, each tagged with a different DSCP value mapping to each FC (BE, AF1, AF2, AF3, AF4, EF, NC1, NC2)<br>5. Egress port bandwidth set to create congestion (aggregate ingress > egress capacity)<br><br>**Configuration:**<br>SW1:<br>`set interface aggregate-ethernet ae1 family ethernet-switching port-mode trunk`<br>`set vlans vlan-id 100 interface ae1`<br>SW3:<br>`set interface xe-0/0/1 family ethernet-switching port-mode trunk`<br>`set vlans vlan-id 100 interface xe-0/0/1`<br>`set interface xe-0/0/1 speed 1g` |
| **Test Procedure** | 1. Start IXIA traffic with all 8 FC streams simultaneously at aggregate rate exceeding egress port capacity.<br>2. Wait 60 seconds for traffic rates to stabilize.<br>3. Execute `run show interface xe-0/0/1 queue statistics` on SW3.<br>4. Execute `run show forwarding-class bandwidth` on SW1.<br>5. Record per-FC throughput from IXIA statistics. |
| **Expected Results** | 1. All 8 traffic streams are forwarded through the stack without being dropped entirely.<br>2. Stabilized traffic rates visible after 60 seconds.<br>3. Queue statistics on SW3 show packets distributed across all 8 queues corresponding to the 8 FCs.<br>4. Per-FC throughput ratios measured by IXIA match the default bandwidth allocation percentages within ±5% tolerance (e.g., EF receives ~25% of total bandwidth, BE receives ~5%).<br>5. No queue starvation observed for any FC. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3 |

---

#### 1.3.1.3 Default Values Restored After FC Bandwidth Reset

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-003: Default FC bandwidth restore after reset |
| **Purpose Of The Test** | Verify that after custom FC bandwidth values are applied and then deleted (reset), all stack members revert to the platform default FC bandwidth values. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Custom FC bandwidth configuration has been applied: EF=40%, BE=10%, AF1-AF4=8% each, NC1=11%, NC2=7%<br><br>**Configuration:**<br>SW1 (pre-applied custom config):<br>`set class-of-service forwarding-class-bandwidth forwarding-class best-effort bandwidth-percent 10`<br>`set class-of-service forwarding-class-bandwidth forwarding-class expedited-forwarding bandwidth-percent 40`<br>`commit` |
| **Test Procedure** | 1. Execute `run show forwarding-class bandwidth` on SW1 to confirm custom values are active.<br>2. Execute `run show forwarding-class bandwidth member 2` and `run show forwarding-class bandwidth member 3` to confirm custom values on all members.<br>3. Execute `delete class-of-service forwarding-class-bandwidth` on SW1.<br>4. Execute `commit` on SW1.<br>5. Wait 10 seconds for configuration to propagate.<br>6. Execute `run show forwarding-class bandwidth` on SW1.<br>7. Execute `run show forwarding-class bandwidth member 2`.<br>8. Execute `run show forwarding-class bandwidth member 3`. |
| **Expected Results** | 1. Step 1: SW1 shows custom FC bandwidth values (EF=40%, BE=10%).<br>2. Step 2: SW2 and SW3 show the same custom values as SW1.<br>3. Step 6: SW1 shows platform default FC bandwidth values (BE=5%, AF1=10%, AF2=10%, AF3=10%, AF4=10%, EF=25%, NC1=15%, NC2=15%).<br>4. Step 7: SW2 shows identical default values to SW1.<br>5. Step 8: SW3 shows identical default values to SW1. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3 |

---

### 1.3.2 Bandwidth Adjustment

#### 1.3.2.1 Adjust FC Bandwidth on Master, Verify Applied to All Members

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-004: FC bandwidth adjustment synced to all members |
| **Purpose Of The Test** | Verify that when FC bandwidth percentages are modified on the master switch, the configuration is automatically synchronized and applied to all stack members (standby and line members). |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Default FC bandwidth configuration active on all members<br><br>**Configuration:**<br>None (default state). |
| **Test Procedure** | 1. Execute `run show forwarding-class bandwidth` on SW1 to record baseline default values.<br>2. Configure new FC bandwidth on SW1:<br>`set class-of-service forwarding-class-bandwidth forwarding-class best-effort bandwidth-percent 15`<br>`set class-of-service forwarding-class-bandwidth forwarding-class expedited-forwarding bandwidth-percent 30`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-1 bandwidth-percent 10`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-2 bandwidth-percent 10`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-3 bandwidth-percent 10`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-4 bandwidth-percent 5`<br>`set class-of-service forwarding-class-bandwidth forwarding-class network-control-1 bandwidth-percent 10`<br>`set class-of-service forwarding-class-bandwidth forwarding-class network-control-2 bandwidth-percent 10`<br>3. Execute `commit` on SW1.<br>4. Wait 10 seconds for sync.<br>5. Execute `run show forwarding-class bandwidth` on SW1.<br>6. Execute `run show forwarding-class bandwidth member 2`.<br>7. Execute `run show forwarding-class bandwidth member 3`. |
| **Expected Results** | 1. Step 1: Default values displayed (BE=5%, EF=25%, etc.).<br>2. Step 3: Commit succeeds without error.<br>3. Step 5: SW1 shows updated values: BE=15%, EF=30%, AF1=10%, AF2=10%, AF3=10%, AF4=5%, NC1=10%, NC2=10%.<br>4. Step 6: SW2 shows identical updated values to SW1.<br>5. Step 7: SW3 shows identical updated values to SW1. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3 |

---

#### 1.3.2.2 Adjust FC Bandwidth to Minimum Value (Boundary Test)

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-005: FC bandwidth minimum boundary value |
| **Purpose Of The Test** | Verify that FC bandwidth can be set to the minimum allowed value (1%) on the master and that this minimum value is synchronized and enforced across all stack members. Also verify that a value below minimum (0%) is rejected. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Default FC bandwidth configuration active<br><br>**Configuration:**<br>None (default state). |
| **Test Procedure** | 1. Configure FC bandwidth for BE to minimum value on SW1:<br>`set class-of-service forwarding-class-bandwidth forwarding-class best-effort bandwidth-percent 1`<br>2. Execute `commit` on SW1.<br>3. Wait 5 seconds.<br>4. Execute `run show forwarding-class bandwidth` on SW1.<br>5. Execute `run show forwarding-class bandwidth member 2`.<br>6. Execute `run show forwarding-class bandwidth member 3`.<br>7. Configure FC bandwidth for BE to 0 on SW1:<br>`set class-of-service forwarding-class-bandwidth forwarding-class best-effort bandwidth-percent 0`<br>8. Execute `commit` on SW1. |
| **Expected Results** | 1. Step 2: Commit with bandwidth-percent 1 succeeds without error.<br>2. Step 4: SW1 shows BE bandwidth = 1%.<br>3. Step 5: SW2 shows BE bandwidth = 1%.<br>4. Step 6: SW3 shows BE bandwidth = 1%.<br>5. Step 7-8: Commit with bandwidth-percent 0 is rejected with error message indicating value out of range (minimum is 1). |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3. Boundary test — minimum value. |

---

#### 1.3.2.3 Adjust FC Bandwidth to Maximum Value (Boundary Test)

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-006: FC bandwidth maximum boundary value |
| **Purpose Of The Test** | Verify that a single FC bandwidth can be set to the maximum allowed value (100%) on the master (when all other FCs are set to 0 or minimum, depending on platform constraints), and that this maximum value is synchronized across all stack members. Also verify that a value above 100% is rejected. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Default FC bandwidth configuration active<br><br>**Configuration:**<br>None (default state). |
| **Test Procedure** | 1. Configure FC bandwidth for EF to maximum value on SW1 while setting all others to minimum:<br>`set class-of-service forwarding-class-bandwidth forwarding-class expedited-forwarding bandwidth-percent 93`<br>`set class-of-service forwarding-class-bandwidth forwarding-class best-effort bandwidth-percent 1`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-1 bandwidth-percent 1`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-2 bandwidth-percent 1`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-3 bandwidth-percent 1`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-4 bandwidth-percent 1`<br>`set class-of-service forwarding-class-bandwidth forwarding-class network-control-1 bandwidth-percent 1`<br>`set class-of-service forwarding-class-bandwidth forwarding-class network-control-2 bandwidth-percent 1`<br>2. Execute `commit` on SW1.<br>3. Wait 5 seconds.<br>4. Execute `run show forwarding-class bandwidth` on SW1.<br>5. Execute `run show forwarding-class bandwidth member 2`.<br>6. Execute `run show forwarding-class bandwidth member 3`.<br>7. Configure FC bandwidth with total exceeding 100%:<br>`set class-of-service forwarding-class-bandwidth forwarding-class expedited-forwarding bandwidth-percent 101`<br>8. Execute `commit` on SW1. |
| **Expected Results** | 1. Step 2: Commit with EF=93% and all others=1% succeeds (total=100%).<br>2. Step 4: SW1 shows EF bandwidth = 93%, all other FCs = 1%.<br>3. Step 5: SW2 shows identical values to SW1.<br>4. Step 6: SW3 shows identical values to SW1.<br>5. Step 7-8: Commit with bandwidth-percent 101 is rejected with error message indicating value out of range (maximum is 100). |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3. Boundary test — maximum value. Total must equal 100%. |

---

#### 1.3.2.4 Multiple FC Bandwidth Changes in Single Commit

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-007: Multiple FC bandwidth changes in single commit |
| **Purpose Of The Test** | Verify that multiple Forwarding Class bandwidth changes submitted in a single commit transaction are atomically applied to all stack members, with the final state consistent across the stack. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Default FC bandwidth configuration active<br><br>**Configuration:**<br>None (default state). |
| **Test Procedure** | 1. Execute `run show forwarding-class bandwidth` on SW1 to record defaults.<br>2. Configure multiple FC bandwidth changes on SW1 without committing between each:<br>`set class-of-service forwarding-class-bandwidth forwarding-class best-effort bandwidth-percent 20`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-1 bandwidth-percent 5`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-2 bandwidth-percent 5`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-3 bandwidth-percent 5`<br>`set class-of-service forwarding-class-bandwidth forwarding-class assured-forwarding-4 bandwidth-percent 5`<br>`set class-of-service forwarding-class-bandwidth forwarding-class expedited-forwarding bandwidth-percent 40`<br>`set class-of-service forwarding-class-bandwidth forwarding-class network-control-1 bandwidth-percent 10`<br>`set class-of-service forwarding-class-bandwidth forwarding-class network-control-2 bandwidth-percent 10`<br>3. Execute `commit` on SW1 (single commit for all changes).<br>4. Wait 10 seconds for propagation.<br>5. Execute `run show forwarding-class bandwidth` on SW1.<br>6. Execute `run show forwarding-class bandwidth member 2`.<br>7. Execute `run show forwarding-class bandwidth member 3`.<br>8. Execute `run show system commit` on SW1 to confirm single commit transaction. |
| **Expected Results** | 1. Step 3: Single commit succeeds without error.<br>2. Step 5: SW1 shows all 8 FC bandwidth values updated: BE=20%, AF1=5%, AF2=5%, AF3=5%, AF4=5%, EF=40%, NC1=10%, NC2=10%.<br>3. Step 6: SW2 shows identical values to SW1 — no intermediate state visible.<br>4. Step 7: SW3 shows identical values to SW1.<br>5. Step 8: Only one commit entry recorded for all 8 FC changes (atomic transaction). |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3. Validates atomic commit behavior in stacking. |

---

### 1.3.3 Bandwidth Persistence

#### 1.3.3.1 FC Bandwidth Survives Master/Standby Switchover

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-008: FC bandwidth persistence after master-standby switchover |
| **Purpose Of The Test** | Verify that custom FC bandwidth configuration is preserved and remains active on all stack members after a master-to-standby failover event. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Custom FC bandwidth configured and committed: BE=20%, AF1=5%, AF2=5%, AF3=5%, AF4=5%, EF=40%, NC1=10%, NC2=10%<br>4. Configuration confirmed active on all 3 members<br><br>**Configuration:**<br>SW1 (pre-applied):<br>`set class-of-service forwarding-class-bandwidth forwarding-class best-effort bandwidth-percent 20`<br>`set class-of-service forwarding-class-bandwidth forwarding-class expedited-forwarding bandwidth-percent 40`<br>(...all 8 FCs configured as above...)<br>`commit` |
| **Test Procedure** | 1. Execute `run show forwarding-class bandwidth` on SW1 to confirm custom values active.<br>2. Execute `run show forwarding-class bandwidth member 2` to confirm SW2 has custom values.<br>3. Execute `run request stack master-switchover` on SW1 to trigger failover.<br>4. Wait 120 seconds for switchover to complete and stack to reconverge.<br>5. Execute `run show stack status` on the new master (SW2) to confirm roles.<br>6. Execute `run show forwarding-class bandwidth` on SW2 (new master).<br>7. Execute `run show forwarding-class bandwidth member 1` (SW1, now standby).<br>8. Execute `run show forwarding-class bandwidth member 3` (SW3, still member). |
| **Expected Results** | 1. Step 1-2: Custom FC bandwidth values confirmed active before switchover.<br>2. Step 5: SW2 is now Master, SW1 is now Standby, SW3 remains Member, all in "Ready" state.<br>3. Step 6: SW2 (new master) shows FC bandwidth: BE=20%, AF1=5%, AF2=5%, AF3=5%, AF4=5%, EF=40%, NC1=10%, NC2=10%.<br>4. Step 7: SW1 (new standby) shows identical custom FC bandwidth values.<br>5. Step 8: SW3 (member) shows identical custom FC bandwidth values. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3. Critical for stacking high-availability. |

---

#### 1.3.3.2 FC Bandwidth Applied to Newly Joined Member

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-009: FC bandwidth sync to newly joined stack member |
| **Purpose Of The Test** | Verify that when a new switch joins an existing stack with custom FC bandwidth configuration, the new member automatically receives and applies the stack's FC bandwidth settings. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== [empty port]`<br>`SW3 (standalone, not yet joined)`<br>Two switches in active stacking. SW3 is a standalone switch ready to join.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. SW1 (master) and SW2 (standby) form a 2-member stack<br>3. Custom FC bandwidth configured on stack: BE=20%, AF1=5%, AF2=5%, AF3=5%, AF4=5%, EF=40%, NC1=10%, NC2=10%<br>4. SW3 is powered on, running default configuration, with stacking enabled but not cabled to the stack<br><br>**Configuration:**<br>SW3 (standalone, pre-join):<br>`set system stack member-id 3`<br>`set system stack enabled true`<br>`commit` |
| **Test Procedure** | 1. Execute `run show forwarding-class bandwidth` on SW1 to confirm custom values.<br>2. Execute `run show stack status` on SW1 to confirm 2-member stack.<br>3. Connect SW3 stacking port cable to SW2's free stacking port.<br>4. Wait 120 seconds for SW3 to join the stack and synchronize.<br>5. Execute `run show stack status` on SW1 to confirm 3-member stack.<br>6. Execute `run show forwarding-class bandwidth member 3` on SW1. |
| **Expected Results** | 1. Step 1: Custom FC bandwidth values confirmed on master.<br>2. Step 2: Stack shows 2 members (SW1 Master, SW2 Standby).<br>3. Step 5: Stack shows 3 members: SW1 (Master), SW2 (Standby), SW3 (Member), all in "Ready" state.<br>4. Step 6: SW3 shows FC bandwidth values identical to master: BE=20%, AF1=5%, AF2=5%, AF3=5%, AF4=5%, EF=40%, NC1=10%, NC2=10%. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3. Validates config sync on member join. |

---

#### 1.3.3.3 FC Bandwidth Consistency After Stack Reboot

| Field | Content |
|-------|---------|
| **Test Name** | MOD3-010: FC bandwidth persistence after full stack reboot |
| **Purpose Of The Test** | Verify that custom FC bandwidth configuration persists across a full stack reboot (all members rebooted simultaneously) and is consistently applied on all members after the stack re-forms. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Custom FC bandwidth configured and committed: BE=20%, AF1=5%, AF2=5%, AF3=5%, AF4=5%, EF=40%, NC1=10%, NC2=10%<br>4. Configuration saved to startup config<br><br>**Configuration:**<br>SW1 (pre-applied):<br>All 8 FCs configured with custom bandwidth values.<br>`commit` |
| **Test Procedure** | 1. Execute `run show forwarding-class bandwidth` on SW1 to record custom values.<br>2. Execute `run show forwarding-class bandwidth member 2` and `member 3` to confirm consistency.<br>3. Execute `run request system reboot stack` on SW1 to reboot all stack members.<br>4. Wait 300 seconds for all members to boot and stack to fully re-form.<br>5. Execute `run show stack status` on the master to confirm stack reformation.<br>6. Execute `run show forwarding-class bandwidth` on the master.<br>7. Execute `run show forwarding-class bandwidth member 2`.<br>8. Execute `run show forwarding-class bandwidth member 3`. |
| **Expected Results** | 1. Step 1-2: Custom values confirmed before reboot.<br>2. Step 5: Stack status shows 3 members, all in "Ready" state. Master/standby roles re-established.<br>3. Step 6: Master shows FC bandwidth: BE=20%, AF1=5%, AF2=5%, AF3=5%, AF4=5%, EF=40%, NC1=10%, NC2=10%.<br>4. Step 7: Member 2 shows identical FC bandwidth values to master.<br>5. Step 8: Member 3 shows identical FC bandwidth values to master. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-3. Validates persistence across cold restart. |

---

## 1.5 Bulk Configuration Reliability (MOD-5)

### 1.5.1 Bulk VLAN Operations

#### 1.5.1.1 Create 1000 VLANs in Batch, Verify on All Members

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-001: Bulk creation of 1000 VLANs across stack |
| **Purpose Of The Test** | Verify that 1000 VLANs can be created in a single batch commit on the master and all VLANs are consistently provisioned across all stack members without errors or missing entries. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. No VLANs configured beyond default VLAN 1<br>4. Sufficient hardware table capacity for 1000 VLANs<br><br>**Configuration:**<br>None (clean state). |
| **Test Procedure** | 1. Execute `run show vlans` on SW1 to confirm only default VLAN exists.<br>2. Configure 1000 VLANs on SW1 (VLAN 100–1099) using a loop script or sequential commands:<br>`set vlans vlan-id 100`<br>`set vlans vlan-id 101`<br>...(through VLAN 1099)...<br>3. Execute `commit` on SW1.<br>4. Record the time taken for commit to complete.<br>5. Wait 30 seconds for propagation.<br>6. Execute `run show vlans | count` on SW1.<br>7. Execute `run show vlans | count` on SW2 via `run show vlans member 2 | count`.<br>8. Execute `run show vlans | count` on SW3 via `run show vlans member 3 | count`.<br>9. Execute `run show vlans vlan-id 100` on SW1 to spot-check first VLAN.<br>10. Execute `run show vlans vlan-id 1099` on SW1 to spot-check last VLAN. |
| **Expected Results** | 1. Step 1: Only VLAN 1 (default) exists.<br>2. Step 3: Commit completes successfully without error.<br>3. Step 4: Commit time recorded (baseline metric for MOD5).<br>4. Step 6: SW1 shows 1001 VLANs (1000 new + default VLAN 1).<br>5. Step 7: SW2 shows 1001 VLANs.<br>6. Step 8: SW3 shows 1001 VLANs.<br>7. Step 9: VLAN 100 exists with correct parameters.<br>8. Step 10: VLAN 1099 exists with correct parameters. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Bulk VLAN creation baseline. |

---

#### 1.5.1.2 Delete 1000 VLANs in Batch, Verify on All Members

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-002: Bulk deletion of 1000 VLANs across stack |
| **Purpose Of The Test** | Verify that 1000 VLANs can be deleted in a single batch commit on the master and all VLANs are consistently removed from all stack members without residual entries or errors. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. 1000 VLANs (100–1099) previously created and confirmed on all members (from MOD5-001)<br><br>**Configuration:**<br>1000 VLANs (100–1099) active on all stack members. |
| **Test Procedure** | 1. Execute `run show vlans | count` on SW1 to confirm 1001 VLANs present.<br>2. Delete all 1000 VLANs on SW1:<br>`delete vlans vlan-id 100`<br>`delete vlans vlan-id 101`<br>...(through VLAN 1099)...<br>3. Execute `commit` on SW1.<br>4. Record the time taken for commit to complete.<br>5. Wait 30 seconds for propagation.<br>6. Execute `run show vlans | count` on SW1.<br>7. Execute `run show vlans | count` on SW2 via `run show vlans member 2 | count`.<br>8. Execute `run show vlans | count` on SW3 via `run show vlans member 3 | count`.<br>9. Execute `run show vlans vlan-id 500` on SW1 to confirm mid-range VLAN is gone. |
| **Expected Results** | 1. Step 1: SW1 shows 1001 VLANs.<br>2. Step 3: Commit completes successfully without error.<br>3. Step 4: Commit time recorded (compare with creation time from MOD5-001).<br>4. Step 6: SW1 shows only 1 VLAN (default VLAN 1).<br>5. Step 7: SW2 shows only 1 VLAN.<br>6. Step 8: SW3 shows only 1 VLAN.<br>7. Step 9: `show vlans vlan-id 500` returns "VLAN not found" or empty output. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Bulk VLAN deletion baseline. |

---

#### 1.5.1.3 Create+Delete VLANs Repeatedly (3 Cycles), Verify Consistency

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-003: Repeated bulk VLAN create/delete cycles (3 rounds) |
| **Purpose Of The Test** | Verify that repeatedly creating and deleting 1000 VLANs in batch (3 full cycles) does not cause resource leaks, configuration drift, or inconsistency between stack members. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. No VLANs configured beyond default VLAN 1<br>4. Record baseline memory usage via `run show system memory`<br><br>**Configuration:**<br>None (clean state). |
| **Test Procedure** | 1. Execute `run show system memory` on SW1 to record baseline memory.<br>2. **Cycle 1 — Create**: Configure 1000 VLANs (100–1099) on SW1 and execute `commit`.<br>3. Wait 30 seconds. Execute `run show vlans | count` on SW1, SW2 (member 2), SW3 (member 3).<br>4. **Cycle 1 — Delete**: Delete all 1000 VLANs on SW1 and execute `commit`.<br>5. Wait 30 seconds. Execute `run show vlans | count` on SW1, SW2, SW3.<br>6. **Cycle 2 — Create**: Repeat step 2.<br>7. Wait 30 seconds. Execute `run show vlans | count` on SW1, SW2, SW3.<br>8. **Cycle 2 — Delete**: Repeat step 4.<br>9. Wait 30 seconds. Execute `run show vlans | count` on SW1, SW2, SW3.<br>10. **Cycle 3 — Create**: Repeat step 2.<br>11. Wait 30 seconds. Execute `run show vlans | count` on SW1, SW2, SW3.<br>12. **Cycle 3 — Delete**: Repeat step 4.<br>13. Wait 30 seconds. Execute `run show vlans | count` on SW1, SW2, SW3.<br>14. Execute `run show system memory` on SW1 to record post-test memory. |
| **Expected Results** | 1. Step 1: Baseline memory recorded.<br>2. After each Create commit: All 3 members show 1001 VLANs.<br>3. After each Delete commit: All 3 members show 1 VLAN (default only).<br>4. All 6 commits (3 create + 3 delete) succeed without error.<br>5. VLAN counts are identical across all 3 members after every operation.<br>6. Step 14: Post-test memory on SW1 is within 5% of baseline — no memory leak detected. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Stress test for resource leak detection. |

---

### 1.5.2 Bulk ACL/Policy Operations

#### 1.5.2.1 Deploy 500 ACL Rules in Batch

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-004: Bulk deployment of 500 ACL rules across stack |
| **Purpose Of The Test** | Verify that 500 ACL rules can be deployed in a single batch commit on the master and all rules are consistently programmed into the hardware TCAM on all stack members. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. No ACLs configured<br>4. Sufficient TCAM capacity for 500 rules<br><br>**Configuration:**<br>None (clean state). |
| **Test Procedure** | 1. Execute `run show firewall` on SW1 to confirm no ACL rules exist.<br>2. Configure 500 ACL rules on SW1 under a single filter:<br>`set firewall filter BULK-ACL term rule-1 from source-address 10.0.0.0/24`<br>`set firewall filter BULK-ACL term rule-1 then accept`<br>`set firewall filter BULK-ACL term rule-2 from source-address 10.0.1.0/24`<br>`set firewall filter BULK-ACL term rule-2 then accept`<br>...(through rule-500, each with unique source-address 10.0.0.0/24 to 10.1.243.0/24)...<br>3. Execute `commit` on SW1.<br>4. Record the time taken for commit to complete.<br>5. Wait 60 seconds for TCAM programming on all members.<br>6. Execute `run show firewall filter BULK-ACL | count` on SW1.<br>7. Execute `run show firewall filter BULK-ACL member 2 | count`.<br>8. Execute `run show firewall filter BULK-ACL member 3 | count`.<br>9. Execute `run show firewall filter BULK-ACL term rule-1` on SW1 to spot-check first rule.<br>10. Execute `run show firewall filter BULK-ACL term rule-500` on SW1 to spot-check last rule. |
| **Expected Results** | 1. Step 1: No firewall filters configured.<br>2. Step 3: Commit completes successfully without error or TCAM overflow warning.<br>3. Step 4: Commit time recorded.<br>4. Step 6: SW1 shows 500 ACL terms in filter BULK-ACL.<br>5. Step 7: SW2 shows 500 ACL terms.<br>6. Step 8: SW3 shows 500 ACL terms.<br>7. Step 9: rule-1 shows source-address 10.0.0.0/24, action accept.<br>8. Step 10: rule-500 shows correct source-address, action accept. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Bulk ACL deployment baseline. |

---

#### 1.5.2.2 Deploy 200 Route-Map Entries in Batch

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-005: Bulk deployment of 200 route-map entries across stack |
| **Purpose Of The Test** | Verify that 200 route-map entries can be deployed in a single batch commit on the master and all entries are consistently applied across all stack members. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. No route-maps configured<br>4. 200 prefix-lists pre-configured (PL-1 through PL-200) for route-map match clauses<br><br>**Configuration:**<br>SW1 (prefix-lists pre-configured):<br>`set policy prefix-list PL-1 10.1.0.0/24`<br>`set policy prefix-list PL-2 10.2.0.0/24`<br>...(through PL-200)...<br>`commit` |
| **Test Procedure** | 1. Execute `run show route-map` on SW1 to confirm no route-maps exist.<br>2. Configure 200 route-map entries on SW1:<br>`set policy route-map BULK-RM permit sequence 10 match ip-address prefix-list PL-1`<br>`set policy route-map BULK-RM permit sequence 10 set local-preference 100`<br>`set policy route-map BULK-RM permit sequence 20 match ip-address prefix-list PL-2`<br>`set policy route-map BULK-RM permit sequence 20 set local-preference 200`<br>...(through sequence 2000, incrementing by 10, each matching a different prefix-list)...<br>3. Execute `commit` on SW1.<br>4. Record the time taken for commit to complete.<br>5. Wait 30 seconds for propagation.<br>6. Execute `run show route-map BULK-RM | count` on SW1.<br>7. Execute `run show route-map BULK-RM member 2 | count`.<br>8. Execute `run show route-map BULK-RM member 3 | count`.<br>9. Execute `run show route-map BULK-RM permit sequence 10` on SW1. |
| **Expected Results** | 1. Step 1: No route-maps configured.<br>2. Step 3: Commit completes successfully without error.<br>3. Step 4: Commit time recorded.<br>4. Step 6: SW1 shows 200 route-map sequences in BULK-RM.<br>5. Step 7: SW2 shows 200 route-map sequences.<br>6. Step 8: SW3 shows 200 route-map sequences.<br>7. Step 9: Sequence 10 shows match on PL-1, set local-preference 100. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Bulk route-map deployment. |

---

#### 1.5.2.3 Mixed ACL + Route-Map + Prefix-List Bulk Deployment

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-006: Mixed bulk deployment of ACL, route-map, and prefix-list |
| **Purpose Of The Test** | Verify that a mixed bulk deployment of 200 ACL rules, 100 route-map entries, and 150 prefix-list entries in a single commit succeeds and is consistently applied across all stack members. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. No ACLs, route-maps, or prefix-lists configured<br><br>**Configuration:**<br>None (clean state). |
| **Test Procedure** | 1. Execute `run show firewall`, `run show route-map`, `run show ip prefix-list` on SW1 to confirm clean state.<br>2. Configure mixed policy objects on SW1 in a single edit session:<br>— 150 prefix-lists: `set policy prefix-list MIX-PL-1 10.10.0.0/24` through MIX-PL-150<br>— 200 ACL rules: `set firewall filter MIX-ACL term mix-rule-1 from source-address 172.16.0.0/24` ... `then accept` through mix-rule-200<br>— 100 route-map entries: `set policy route-map MIX-RM permit sequence 10 match ip-address prefix-list MIX-PL-1` ... `set local-preference 100` through sequence 1000<br>3. Execute `commit` on SW1.<br>4. Record the time taken for commit to complete.<br>5. Wait 60 seconds for propagation and TCAM programming.<br>6. Execute `run show ip prefix-list | count` on SW1, member 2, member 3.<br>7. Execute `run show firewall filter MIX-ACL | count` on SW1, member 2, member 3.<br>8. Execute `run show route-map MIX-RM | count` on SW1, member 2, member 3. |
| **Expected Results** | 1. Step 1: All show commands return empty/no entries.<br>2. Step 3: Single commit succeeds without error for all 450 policy objects.<br>3. Step 4: Commit time recorded.<br>4. Step 6: All 3 members show 150 prefix-lists.<br>5. Step 7: All 3 members show 200 ACL terms in MIX-ACL.<br>6. Step 8: All 3 members show 100 route-map sequences in MIX-RM. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Mixed policy object bulk deployment. |

---

### 1.5.3 Configuration Reliability Metrics

#### 1.5.3.1 Measure Config Deployment Success Rate (Must Be 100%)

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-007: Configuration deployment success rate measurement |
| **Purpose Of The Test** | Verify that the configuration deployment success rate is 100% for a batch of 50 sequential commit operations, each deploying a distinct configuration block (VLANs, interfaces, ACLs), with no commit failures or partial deployments. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Clean configuration (no VLANs, ACLs, or interfaces beyond defaults)<br>4. Script prepared to execute 50 sequential commits and record success/failure<br><br>**Configuration:**<br>None (clean state). |
| **Test Procedure** | 1. Execute a scripted sequence of 50 commits on SW1, each containing a different configuration block:<br>— Commits 1–20: Create VLANs (20 VLANs each commit, VLAN 100–499)<br>— Commits 21–35: Create ACL rules (10 rules each commit, 150 rules total)<br>— Commits 36–50: Create prefix-lists (10 entries each commit, 150 entries total)<br>2. Record the exit code and output of each `commit` command.<br>3. Wait 60 seconds after the last commit.<br>4. Execute `run show vlans | count` on SW1.<br>5. Execute `run show firewall filter | count` on SW1.<br>6. Execute `run show ip prefix-list | count` on SW1.<br>7. Execute `run show vlans | count` on member 2 and member 3.<br>8. Execute `run show system commit` on SW1 to count commit entries. |
| **Expected Results** | 1. All 50 commits succeed with exit code 0 — no errors, warnings, or timeouts.<br>2. Success rate = 50/50 = 100%.<br>3. Step 4: SW1 shows 401 VLANs (400 created + default).<br>4. Step 5: SW1 shows 150 ACL rules.<br>5. Step 6: SW1 shows 150 prefix-lists.<br>6. Step 7: SW2 and SW3 show identical counts to SW1 for all three object types.<br>7. Step 8: 50 commit entries recorded in commit history. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. 100% success rate is a hard requirement. |

---

#### 1.5.3.2 Monitor CPU/Memory During Bulk Config Deployment

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-008: CPU and memory monitoring during bulk config deployment |
| **Purpose Of The Test** | Verify that CPU utilization does not exceed 90% and memory usage does not exceed 85% of total capacity during a large bulk configuration deployment on the stacking master, and that no OOM (Out of Memory) events occur on any member. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Clean configuration state<br>4. Monitoring script prepared to poll CPU/memory every 5 seconds during deployment<br><br>**Configuration:**<br>None (clean state). |
| **Test Procedure** | 1. Execute `run show system cpu` and `run show system memory` on SW1, SW2, SW3 to record baseline.<br>2. Start background monitoring: poll `run show system cpu` and `run show system memory` on all 3 members every 5 seconds, logging timestamps and values.<br>3. Configure 1000 VLANs + 500 ACL rules on SW1 in a single edit session.<br>4. Execute `commit` on SW1.<br>5. Continue monitoring for 120 seconds after commit completes.<br>6. Stop monitoring and collect all logged data.<br>7. Execute `run show logging | grep -i "oom\|out of memory\|kill"` on SW1, SW2, SW3. |
| **Expected Results** | 1. Step 1: Baseline CPU < 20%, baseline memory usage < 50%.<br>2. Peak CPU on SW1 (master) during commit does not exceed 90%.<br>3. Peak CPU on SW2 and SW3 during sync does not exceed 80%.<br>4. Peak memory on all members does not exceed 85% of total.<br>5. CPU returns to within 10% of baseline within 60 seconds after commit completes.<br>6. Memory returns to within 5% of baseline within 120 seconds after commit completes.<br>7. Step 7: No OOM or process-kill log entries on any member. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Resource consumption thresholds. |

---

#### 1.5.3.3 Configuration Consistency Between Master and All Members After Bulk Deploy

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-009: Config consistency verification post bulk deployment |
| **Purpose Of The Test** | Verify that the running configuration on every stack member is byte-for-byte identical to the master's running configuration after a large bulk deployment, with no missing or extraneous entries on any member. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Bulk deployment completed: 1000 VLANs, 500 ACL rules, 200 route-map entries, 200 prefix-lists<br>4. All commits succeeded<br><br>**Configuration:**<br>All bulk objects from MOD5-001 through MOD5-006 deployed and committed. |
| **Test Procedure** | 1. Execute `run show configuration` on SW1 and save output to file (master-config.txt).<br>2. Execute `run show configuration member 2` and save output to file (member2-config.txt).<br>3. Execute `run show configuration member 3` and save output to file (member3-config.txt).<br>4. Diff master-config.txt against member2-config.txt (excluding member-specific fields like member-id and hostname).<br>5. Diff master-config.txt against member3-config.txt (excluding member-specific fields).<br>6. Execute `run show vlans | count` on all 3 members.<br>7. Execute `run show firewall filter | count` on all 3 members.<br>8. Execute `run show route-map | count` on all 3 members. |
| **Expected Results** | 1. Step 4: Diff between master and member 2 shows zero differences (after excluding member-specific fields).<br>2. Step 5: Diff between master and member 3 shows zero differences (after excluding member-specific fields).<br>3. Step 6: All 3 members report identical VLAN count.<br>4. Step 7: All 3 members report identical ACL rule count.<br>5. Step 8: All 3 members report identical route-map count. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Configuration consistency is a hard stacking requirement. |

---

#### 1.5.3.4 Configuration Rollback After Partial Bulk Deployment Failure

| Field | Content |
|-------|---------|
| **Test Name** | MOD5-010: Config rollback after simulated partial bulk failure |
| **Purpose Of The Test** | Verify that if a bulk configuration deployment fails mid-way (e.g., due to TCAM exhaustion), the system performs a clean rollback to the previous consistent state on all stack members without configuration drift. |
| **Test Topo & Precondition** | **Topology:**<br>`SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member)`<br>Three switches connected in a ring stacking topology via dedicated stacking ports.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. Baseline configuration: 100 VLANs (100–199) deployed and confirmed on all members<br>4. TCAM partially consumed — remaining capacity known<br><br>**Configuration:**<br>SW1 (baseline):<br>`set vlans vlan-id 100` through `set vlans vlan-id 199`<br>`commit` |
| **Test Procedure** | 1. Execute `run show vlans | count` on SW1 to confirm 101 VLANs (100 + default).<br>2. Execute `run show forwarding-table tcam-usage` on SW1 to record current TCAM utilization.<br>3. Configure ACL rules designed to exceed remaining TCAM capacity (e.g., 10000 complex ACL rules with multiple match conditions):<br>`set firewall filter OVERFLOW-ACL term rule-1 from source-address 192.168.0.0/24 destination-address 10.0.0.0/24 protocol tcp destination-port 80`<br>`set firewall filter OVERFLOW-ACL term rule-1 then accept`<br>...(10000 rules with complex match criteria)...<br>4. Execute `commit` on SW1.<br>5. Wait 30 seconds.<br>6. Execute `run show vlans | count` on SW1, member 2, member 3.<br>7. Execute `run show firewall filter OVERFLOW-ACL | count` on SW1.<br>8. Execute `run show configuration | compare rollback 1` on SW1. |
| **Expected Results** | 1. Step 4: Commit fails with TCAM overflow or resource exhaustion error message.<br>2. Step 6: All 3 members still show 101 VLANs — baseline configuration intact, no partial VLAN loss.<br>3. Step 7: OVERFLOW-ACL filter does not exist (rolled back) or shows 0 rules.<br>4. Step 8: No configuration difference between current and rollback 1 — clean rollback to pre-commit state.<br>5. No error logs indicating configuration inconsistency between members. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-7. Rollback integrity after failure. |

---

## 1.6 Protocol Packet vs Config Concurrency (MOD-6)

### 1.6.1 Config During Protocol Traffic

#### 1.6.1.1 Deploy Configuration While ARP Packets Flood at CoPP Limit Rate

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-001: Config deployment under ARP packet flood at CoPP limit |
| **Purpose Of The Test** | Verify that configuration deployment (100 VLANs) succeeds without error while the control plane is processing ARP packets at the CoPP rate limit, and that neither configuration sync nor ARP processing is interrupted. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member) --- IXIA Port2`<br>Three switches in a ring stacking topology. IXIA connected to SW1 and SW3 edge ports for traffic generation.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. CoPP configured with ARP rate limit (e.g., 500 pps) — using default or explicit CoPP policy<br>4. IXIA configured to generate ARP request packets targeting SW1 at 2× CoPP limit (1000 pps) to saturate CoPP ARP queue<br>5. Clean configuration state (no extra VLANs)<br><br>**Configuration:**<br>SW1 (CoPP):<br>`set system copp-profile arp rate 500`<br>`commit` |
| **Test Procedure** | 1. Execute `run show system copp-profile` on SW1 to confirm ARP CoPP rate limit = 500 pps.<br>2. Start IXIA ARP flood at 1000 pps towards SW1.<br>3. Wait 10 seconds for CoPP policing to stabilize.<br>4. Execute `run show system copp-profile statistics` on SW1 to confirm ARP packets being rate-limited.<br>5. While ARP flood continues, configure 100 VLANs on SW1:<br>`set vlans vlan-id 200` through `set vlans vlan-id 299`<br>6. Execute `commit` on SW1.<br>7. Record commit duration.<br>8. Wait 30 seconds.<br>9. Execute `run show vlans | count` on SW1, member 2, member 3.<br>10. Stop IXIA ARP flood.<br>11. Execute `run show system copp-profile statistics` on SW1 to record ARP packet counters. |
| **Expected Results** | 1. Step 4: CoPP statistics show ARP packets received > 500 pps and policer drop counter incrementing.<br>2. Step 6: Commit completes successfully without error or timeout.<br>3. Step 7: Commit duration recorded (compare with no-flood baseline in later analysis).<br>4. Step 9: All 3 members show 101 VLANs (100 new + default).<br>5. Step 11: ARP CoPP policer counters show packets accepted at ~500 pps rate and excess dropped — CoPP functioning correctly throughout config deployment. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-8. ARP flood vs config concurrency. |

---

#### 1.6.1.2 Deploy Configuration While OSPF Packets Flood at CoPP Limit Rate

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-002: Config deployment under OSPF packet flood at CoPP limit |
| **Purpose Of The Test** | Verify that configuration deployment (100 VLANs) succeeds without error while the control plane is processing OSPF Hello/LSA packets at the CoPP rate limit, and that OSPF adjacency remains stable during and after configuration deployment. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master, OSPF) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member, OSPF) --- IXIA Port2`<br>Three switches in a ring stacking topology. IXIA connected to SW1 for OSPF packet injection. SW1 and SW3 have OSPF enabled with an external OSPF neighbor (or IXIA simulating OSPF).<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. OSPF configured on SW1 with area 0, neighbor adjacency established<br>4. CoPP configured with OSPF rate limit (e.g., 1000 pps)<br>5. IXIA configured to inject OSPF Hello packets at 2× CoPP limit (2000 pps)<br>6. Clean VLAN state<br><br>**Configuration:**<br>SW1 (OSPF):<br>`set protocols ospf area 0.0.0.0 interface xe-0/0/1`<br>`set protocols ospf router-id 1.1.1.1`<br>`commit` |
| **Test Procedure** | 1. Execute `run show protocols ospf neighbor` on SW1 to confirm OSPF adjacency is "Full".<br>2. Execute `run show system copp-profile` on SW1 to confirm OSPF CoPP rate limit.<br>3. Start IXIA OSPF packet flood at 2000 pps towards SW1.<br>4. Wait 10 seconds for CoPP policing to stabilize.<br>5. Execute `run show system copp-profile statistics` on SW1 to confirm OSPF packets being rate-limited.<br>6. While OSPF flood continues, configure 100 VLANs on SW1:<br>`set vlans vlan-id 300` through `set vlans vlan-id 399`<br>7. Execute `commit` on SW1.<br>8. Record commit duration.<br>9. Wait 30 seconds.<br>10. Execute `run show vlans | count` on SW1, member 2, member 3.<br>11. Execute `run show protocols ospf neighbor` on SW1 to confirm adjacency state.<br>12. Stop IXIA OSPF flood. |
| **Expected Results** | 1. Step 1: OSPF adjacency is in "Full" state.<br>2. Step 5: OSPF CoPP policer drop counter incrementing.<br>3. Step 7: Commit completes successfully without error.<br>4. Step 8: Commit duration recorded.<br>5. Step 10: All 3 members show 101 VLANs (100 new + default).<br>6. Step 11: OSPF adjacency is still in "Full" state — no adjacency flap during config deployment. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-8. OSPF flood vs config concurrency. |

---

#### 1.6.1.3 Deploy Configuration While BGP Packets Flood at CoPP Limit Rate

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-003: Config deployment under BGP packet flood at CoPP limit |
| **Purpose Of The Test** | Verify that configuration deployment (100 VLANs) succeeds without error while the control plane is processing BGP UPDATE/KEEPALIVE packets at the CoPP rate limit, and that BGP sessions remain established during and after configuration deployment. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master, BGP AS65001) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member) --- IXIA Port2 (BGP AS65002)`<br>Three switches in a ring stacking topology. IXIA Port2 simulates an eBGP peer connected to SW3. IXIA Port1 injects BGP packets towards SW1.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. BGP session established between SW3 and IXIA (AS65002), state = Established<br>4. CoPP configured with BGP rate limit (e.g., 1000 pps)<br>5. IXIA configured to inject BGP UPDATE packets at 2× CoPP limit (2000 pps) towards SW1<br>6. Clean VLAN state<br><br>**Configuration:**<br>SW1 (BGP):<br>`set protocols bgp local-as 65001`<br>`set protocols bgp neighbor 10.0.0.2 remote-as 65002`<br>`commit` |
| **Test Procedure** | 1. Execute `run show protocols bgp summary` on SW1 to confirm BGP session is "Established".<br>2. Execute `run show system copp-profile` on SW1 to confirm BGP CoPP rate limit.<br>3. Start IXIA BGP packet flood at 2000 pps towards SW1.<br>4. Wait 10 seconds for CoPP policing to stabilize.<br>5. Execute `run show system copp-profile statistics` on SW1 to confirm BGP packets being rate-limited.<br>6. While BGP flood continues, configure 100 VLANs on SW1:<br>`set vlans vlan-id 400` through `set vlans vlan-id 499`<br>7. Execute `commit` on SW1.<br>8. Record commit duration.<br>9. Wait 30 seconds.<br>10. Execute `run show vlans | count` on SW1, member 2, member 3.<br>11. Execute `run show protocols bgp summary` on SW1 to confirm BGP session state.<br>12. Stop IXIA BGP flood. |
| **Expected Results** | 1. Step 1: BGP session is "Established" with IXIA peer.<br>2. Step 5: BGP CoPP policer drop counter incrementing.<br>3. Step 7: Commit completes successfully without error.<br>4. Step 8: Commit duration recorded.<br>5. Step 10: All 3 members show 101 VLANs (100 new + default).<br>6. Step 11: BGP session remains "Established" — no session reset or flap during config deployment. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-8. BGP flood vs config concurrency. |

---

#### 1.6.1.4 Deploy Configuration While Mixed Protocol Packets Flood Simultaneously

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-004: Config deployment under simultaneous mixed protocol flood |
| **Purpose Of The Test** | Verify that configuration deployment succeeds while ARP, OSPF, BGP, LACP, and STP packets simultaneously flood the control plane at their respective CoPP rate limits, and that all protocol sessions remain stable. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master, OSPF+BGP) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member, OSPF+BGP) --- IXIA Port2`<br>`IXIA Port3 --- SW2 (additional port for LACP/STP injection)`<br>Three switches in a ring stacking topology. Multiple IXIA ports connected for multi-protocol traffic injection.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. OSPF adjacency established (area 0), BGP session established (eBGP), LACP bundle active, STP running<br>4. CoPP rate limits configured for ARP (500 pps), OSPF (1000 pps), BGP (1000 pps), LACP (500 pps), STP (500 pps)<br>5. IXIA configured to flood all 5 protocol types simultaneously at 2× their respective CoPP limits<br>6. Clean VLAN state<br><br>**Configuration:**<br>SW1: OSPF area 0, BGP AS65001, LACP ae1, STP enabled on all ports.<br>`commit` |
| **Test Procedure** | 1. Execute `run show protocols ospf neighbor`, `run show protocols bgp summary`, `run show lacp interfaces`, `run show spanning-tree bridge` on SW1 to confirm all protocol states are stable.<br>2. Start IXIA simultaneous flood: ARP (1000 pps) + OSPF (2000 pps) + BGP (2000 pps) + LACP (1000 pps) + STP (1000 pps).<br>3. Wait 15 seconds for CoPP policing to stabilize across all protocol queues.<br>4. Execute `run show system copp-profile statistics` on SW1 to confirm all 5 protocol types are being rate-limited.<br>5. While mixed flood continues, configure 100 VLANs on SW1:<br>`set vlans vlan-id 500` through `set vlans vlan-id 599`<br>6. Execute `commit` on SW1.<br>7. Record commit duration.<br>8. Wait 30 seconds.<br>9. Execute `run show vlans | count` on SW1, member 2, member 3.<br>10. Execute `run show protocols ospf neighbor`, `run show protocols bgp summary`, `run show lacp interfaces`, `run show spanning-tree bridge` on SW1.<br>11. Stop all IXIA traffic streams. |
| **Expected Results** | 1. Step 1: All protocol sessions/states stable before flood.<br>2. Step 4: CoPP statistics show drop counters incrementing for all 5 protocol types.<br>3. Step 6: Commit completes successfully without error or timeout.<br>4. Step 7: Commit duration recorded (expected to be longer than single-protocol flood scenarios).<br>5. Step 9: All 3 members show 101 VLANs.<br>6. Step 10: OSPF adjacency remains "Full", BGP session remains "Established", LACP bundle remains active, STP topology unchanged (no topology change notifications). |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-8. Worst-case concurrent protocol flood vs config deployment. |

---

### 1.6.2 Stress and Stability

#### 1.6.2.1 Measure Config Deployment Delay Under Protocol Packet Storm

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-005: Config deployment latency measurement under protocol storm |
| **Purpose Of The Test** | Quantify the impact of protocol packet storms on configuration deployment latency by comparing commit times with and without protocol flood, establishing an acceptable delay threshold. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member) --- IXIA Port2`<br>Three switches in a ring stacking topology. IXIA connected to SW1 for protocol flood generation.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. CoPP configured with default rate limits<br>4. IXIA configured with mixed protocol flood (ARP + OSPF + BGP) at 2× aggregate CoPP limit<br>5. Clean configuration state for each measurement iteration<br><br>**Configuration:**<br>None (clean state for each measurement). |
| **Test Procedure** | 1. **Baseline (no flood)**: Configure 100 VLANs (VLAN 100–199) on SW1. Execute `commit`. Record commit duration (T_baseline). Delete VLANs and commit. Wait 30 seconds.<br>2. **Under flood**: Start IXIA mixed protocol flood (ARP 1000 pps + OSPF 2000 pps + BGP 2000 pps). Wait 10 seconds.<br>3. Configure 100 VLANs (VLAN 100–199) on SW1. Execute `commit`. Record commit duration (T_flood). Delete VLANs and commit.<br>4. Stop IXIA flood.<br>5. Wait 30 seconds.<br>6. **Repeat**: Perform steps 1–4 two more times (3 iterations total).<br>7. Calculate average T_baseline and average T_flood across all iterations.<br>8. Calculate delay ratio: T_flood / T_baseline. |
| **Expected Results** | 1. All 6 commits (3 baseline + 3 under flood) succeed without error.<br>2. T_flood is consistently measurable and finite (no commit timeout).<br>3. Delay ratio (T_flood / T_baseline) does not exceed 2.0× — config deployment under flood takes no more than double the baseline time.<br>4. Standard deviation of T_flood across 3 iterations is within 20% of mean — consistent performance, not erratic. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-8. Performance regression benchmark. |

---

#### 1.6.2.2 CPU Utilization: Protocol Processing Must Not Starve Config Channel

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-006: CPU utilization — config channel not starved by protocol processing |
| **Purpose Of The Test** | Verify that protocol packet processing under CoPP-limited flood does not consume so much CPU that the configuration management channel is starved, by monitoring CPU allocation between protocol processing and config sync threads. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member) --- IXIA Port2`<br>Three switches in a ring stacking topology. IXIA connected to SW1 for protocol flood generation.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. CoPP configured with default rate limits<br>4. IXIA configured with mixed protocol flood at maximum aggregate CoPP throughput<br>5. CPU monitoring prepared (polling every 2 seconds)<br><br>**Configuration:**<br>None. |
| **Test Procedure** | 1. Execute `run show system cpu detail` on SW1 to record baseline per-process CPU usage.<br>2. Start IXIA mixed protocol flood (ARP + OSPF + BGP + LACP + STP) at maximum CoPP rates.<br>3. Wait 30 seconds for CPU usage to stabilize under flood.<br>4. Execute `run show system cpu detail` on SW1 every 5 seconds for 60 seconds (12 samples). Record protocol-related process CPU and config-sync process CPU.<br>5. While flood continues, configure 50 VLANs on SW1 and execute `commit`.<br>6. During commit, execute `run show system cpu detail` on SW1 every 2 seconds for 30 seconds.<br>7. Record whether commit completes within expected time frame.<br>8. Stop IXIA flood.<br>9. Wait 60 seconds. Execute `run show system cpu detail` on SW1 to confirm recovery. |
| **Expected Results** | 1. Step 4: Protocol processing CPU usage stabilizes; total CPU does not exceed 80% under flood alone.<br>2. Step 5: Commit succeeds without error.<br>3. Step 6: During commit, total CPU may spike to ~90% but the config-sync process receives at least 10% CPU allocation — it is not starved.<br>4. Step 7: Commit completes within 2× baseline time (no starvation-induced timeout).<br>5. Step 9: CPU returns to baseline levels within 60 seconds after flood stops. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-8. CPU scheduling fairness between protocol and config paths. |

---

#### 1.6.2.3 Sustained Protocol Flood (1 Hour) + Periodic Config Changes

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-007: 1-hour sustained protocol flood with periodic config changes |
| **Purpose Of The Test** | Verify that the stacking system remains stable during a sustained 1-hour protocol packet flood with configuration changes deployed every 10 minutes, with no memory leaks, CPU runaway, process crashes, or configuration drift. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member) --- IXIA Port2`<br>Three switches in a ring stacking topology. IXIA connected to SW1 for sustained protocol flood.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. CoPP configured with default rate limits<br>4. IXIA configured with mixed protocol flood at 2× CoPP aggregate limit<br>5. Baseline CPU and memory recorded on all members<br>6. Automated script prepared to deploy 20 VLANs every 10 minutes (create, wait, delete, wait) for 1 hour<br><br>**Configuration:**<br>None (clean state at start). |
| **Test Procedure** | 1. Execute `run show system cpu` and `run show system memory` on SW1, SW2, SW3 to record baseline.<br>2. Start IXIA mixed protocol flood (ARP + OSPF + BGP) at 2× CoPP aggregate limit.<br>3. Start automated config change script on SW1: every 10 minutes, create 20 VLANs (batch), commit, wait 2 minutes, delete 20 VLANs, commit.<br>4. Start background monitoring: poll `run show system cpu`, `run show system memory`, and `run show stack status` on all members every 60 seconds for 1 hour.<br>5. Wait 60 minutes.<br>6. Stop IXIA flood.<br>7. Stop config change script and monitoring.<br>8. Execute `run show system cpu` and `run show system memory` on SW1, SW2, SW3 to record post-test values.<br>9. Execute `run show stack status` on SW1 to confirm stack integrity.<br>10. Execute `run show vlans | count` on SW1, member 2, member 3 to confirm clean state.<br>11. Execute `run show logging | grep -i "crash\|core\|panic\|oom\|restart"` on all members. |
| **Expected Results** | 1. All 12 commit operations (6 create + 6 delete over 1 hour) succeed without error.<br>2. Stack remains fully formed throughout — `show stack status` always shows 3 members in "Ready" state during all 60 monitoring intervals.<br>3. CPU usage on all members stays below 85% throughout the test (no CPU runaway).<br>4. Memory usage trend remains flat (±3% from baseline) — no memory leak detected.<br>5. Step 8: Post-test CPU and memory within 5% of baseline.<br>6. Step 9: Stack status shows 3 members, all "Ready".<br>7. Step 10: All members show only default VLAN (clean state after final delete).<br>8. Step 11: No crash, core dump, panic, OOM, or process restart log entries. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P0 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-8. Long-duration stability test. |

---

#### 1.6.2.4 Stack Stability After Prolonged Concurrent Protocol Flood + Config Operations

| Field | Content |
|-------|---------|
| **Test Name** | MOD6-008: Stack stability post prolonged concurrent flood and config |
| **Purpose Of The Test** | Verify that after a prolonged period (2 hours) of concurrent protocol flood and configuration operations, the stacking system returns to a fully healthy state: all protocols re-converge, stack roles are correct, and subsequent configuration operations succeed without degradation. |
| **Test Topo & Precondition** | **Topology:**<br>`IXIA Port1 --- SW1 (Master, OSPF+BGP) ==stack-port== SW2 (Standby) ==stack-port== SW3 (Member, OSPF+BGP) --- IXIA Port2`<br>Three switches in a ring stacking topology. IXIA connected to SW1 and SW3 for protocol flood and neighbor simulation.<br><br>**Preconditions:**<br>1. All switches running PicOS 4.6<br>2. Stack is fully formed with SW1 as master, SW2 as standby, SW3 as member<br>3. OSPF adjacency established, BGP session established<br>4. CoPP configured with default rate limits<br>5. Test has been preceded by MOD6-007 (1-hour sustained test) or equivalent 2-hour stress period with protocol flood + periodic config changes<br>6. IXIA flood and config script have been stopped<br><br>**Configuration:**<br>SW1: OSPF area 0, BGP AS65001 with IXIA peer, CoPP defaults.<br>`commit` |
| **Test Procedure** | 1. Wait 120 seconds after stopping all flood traffic and config scripts (recovery period).<br>2. Execute `run show stack status` on SW1 to confirm stack roles and member states.<br>3. Execute `run show protocols ospf neighbor` on SW1 to confirm OSPF adjacency state.<br>4. Execute `run show protocols bgp summary` on SW1 to confirm BGP session state.<br>5. Execute `run show system cpu` and `run show system memory` on SW1, SW2, SW3.<br>6. Configure 50 VLANs (VLAN 700–749) on SW1 and execute `commit`. Record commit duration.<br>7. Execute `run show vlans | count` on SW1, member 2, member 3.<br>8. Delete the 50 VLANs and execute `commit`. Record commit duration.<br>9. Execute `run show vlans | count` on SW1, member 2, member 3.<br>10. Execute `run show logging | grep -i "error\|warning\|fail"` on SW1 — scan for degradation indicators. |
| **Expected Results** | 1. Step 2: Stack shows 3 members: SW1 (Master), SW2 (Standby), SW3 (Member), all "Ready" — no role changes or member loss.<br>2. Step 3: OSPF adjacency is "Full" — fully re-converged after flood stops.<br>3. Step 4: BGP session is "Established" — no session reset.<br>4. Step 5: CPU < 20% and memory within 5% of pre-stress baseline on all members — resources fully recovered.<br>5. Step 6: Commit succeeds. Commit duration within 10% of pre-stress baseline — no performance degradation.<br>6. Step 7: All 3 members show 51 VLANs.<br>7. Step 8: Delete commit succeeds. Duration within 10% of baseline.<br>8. Step 9: All 3 members show 1 VLAN (default only).<br>9. Step 10: No critical error or failure log entries during recovery and post-recovery operations. |
| **Automated or Not** | Not Yet |
| **Related Scripts** | N/A |
| **Level** | P1 |
| **Hardware Model** | All PicOS Switches |
| **Version** | PicOS 4.6 |
| **Actual Results** | |
| **Test Results** | |
| **Remark** | Developer requirement TP-8. Post-stress health validation. |

---

## Coverage Summary

### Test Case Count by Module

| Module | Sub-Section | P0 | P1 | P2 | Total |
|--------|------------|----|----|-----|-------|
| **MOD-3**: Forwarding Class Bandwidth | 1.3.1 Default Values | 2 | 1 | 0 | 3 |
| | 1.3.2 Bandwidth Adjustment | 2 | 2 | 0 | 4 |
| | 1.3.3 Bandwidth Persistence | 3 | 0 | 0 | 3 |
| **MOD-3 Subtotal** | | **7** | **3** | **0** | **10** |
| **MOD-5**: Bulk Config Reliability | 1.5.1 Bulk VLAN Operations | 2 | 1 | 0 | 3 |
| | 1.5.2 Bulk ACL/Policy Operations | 1 | 2 | 0 | 3 |
| | 1.5.3 Config Reliability Metrics | 2 | 2 | 0 | 4 |
| **MOD-5 Subtotal** | | **5** | **5** | **0** | **10** |
| **MOD-6**: Protocol vs Config Concurrency | 1.6.1 Config During Protocol Traffic | 4 | 0 | 0 | 4 |
| | 1.6.2 Stress and Stability | 1 | 3 | 0 | 4 |
| **MOD-6 Subtotal** | | **5** | **3** | **0** | **8** |
| **Grand Total** | | **17** | **11** | **0** | **28** |

### Developer Requirement Traceability

| Developer TP | Module | Test Cases | Coverage |
|-------------|--------|------------|----------|
| TP-3 | MOD-3: Forwarding Class Bandwidth | MOD3-001 through MOD3-010 | Default values, adjustment (including boundary), persistence across switchover/join/reboot |
| TP-7 | MOD-5: Bulk Configuration Reliability | MOD5-001 through MOD5-010 | VLAN/ACL/policy bulk ops, success rate, resource monitoring, consistency, rollback |
| TP-8 | MOD-6: Protocol Packet vs Config Concurrency | MOD6-001 through MOD6-008 | Per-protocol flood, mixed flood, latency measurement, CPU fairness, 1-hour endurance, post-stress recovery |

### Key Verification Commands Referenced

| Command | Purpose | Used In |
|---------|---------|---------|
| `run show stack status` | Stack member roles and readiness | All modules |
| `run show forwarding-class bandwidth` | FC bandwidth allocation per member | MOD-3 |
| `run show vlans \| count` | VLAN count verification | MOD-5, MOD-6 |
| `run show firewall filter` | ACL rule verification | MOD-5 |
| `run show route-map` | Route-map entry verification | MOD-5 |
| `run show system cpu` / `cpu detail` | CPU utilization monitoring | MOD-5, MOD-6 |
| `run show system memory` | Memory usage monitoring | MOD-5, MOD-6 |
| `run show system copp-profile statistics` | CoPP rate-limit counters | MOD-6 |
| `run show protocols ospf neighbor` | OSPF adjacency state | MOD-6 |
| `run show protocols bgp summary` | BGP session state | MOD-6 |
| `run show configuration` | Full running config for diff | MOD-5 |
| `run show logging` | System event / error log scan | MOD-5, MOD-6 |
