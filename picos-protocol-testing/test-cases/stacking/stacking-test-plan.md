# PicOS Stacking Test Plan

**Platform**: PicOS  
**Feature**: Stacking (堆叠)  
**Created**: 2026-03-16  
**Status**: Draft  

---

## 1. Background

Based on developer-provided expected test points (no formal PRD/TD), this plan covers systematic testing of PicOS stacking functionality. Stacking virtualizes multiple physical switches into a single logical device, requiring verification across control plane, data plane, and management plane.

## 2. Developer Expected Test Points

| ID | Test Point | Priority |
|----|-----------|----------|
| TP-1 | Port pre-configuration support across all modules | P0 |
| TP-2 | Inband functionality under master/standby switchover | P0 |
| TP-3 | Forwarding Class Bandwidth adjustment values | P1 |
| TP-4 | Stacking CoPP rate per device = display value / number of stacked devices | P0 |
| TP-5 | Compare with Ruijie stacking: single vs multi-device capability differences | P1 |
| TP-6 | CoPP allocation mechanism: current PicOS (total/N) vs Ruijie (each device full rate, master scheduling) | P0 |
| TP-7 | Bulk configuration deployment reliability (no failures) | P0 |
| TP-8 | High-volume protocol packets must not cause configuration deployment failure | P0 |

## 3. Test Modules

| Module | Name | Test Points | Priority | Est. Cases |
|--------|------|-------------|----------|------------|
| MOD-1 | Port Pre-Configuration | TP-1 | P0 | 15-20 |
| MOD-2 | Inband Management | TP-2 | P0 | 12-15 |
| MOD-3 | Forwarding Class Bandwidth | TP-3 | P1 | 10-12 |
| MOD-4 | CoPP Stacking Rate Allocation | TP-4, TP-5, TP-6 | P0 | 25-30 |
| MOD-5 | Bulk Configuration Reliability | TP-7 | P0 | 10-12 |
| MOD-6 | Protocol Packet vs Config Concurrency | TP-8 | P0 | 8-10 |

## 4. Test Phases

- **Phase 1 (2-3 days)**: MOD-1, MOD-2 basic scenarios
- **Phase 2 (3-5 days)**: MOD-3, MOD-4 core functional verification
- **Phase 3 (2-3 days)**: MOD-5, MOD-6 stress and reliability
- **Phase 4 (1-2 days)**: Ruijie comparison + full regression

## 5. Environment Requirements

- 4x PicOS switches (same model) for 2/3/4 device stacking
- 1x Traffic generator (Spirent / IXIA / open-source)
- 1x Management server for Inband and bulk config testing

## 6. Risk Assessment

| Risk | Level | Impact | Mitigation |
|------|-------|--------|------------|
| CoPP rate imbalance causes protocol flap | P0 | Neighbor disruption on some members | Measure actual rate per device |
| Bulk config causes stack split | P0 | Full service outage | Monitor stack state before/after |
| CoPP/Bandwidth config lost after failover | P0 | Traffic control failure | Compare show output before/after |
| Inband management downtime too long | P1 | Cannot manage during switchover | Measure exact interruption time |
| No formal docs causes coverage gaps | P1 | Missing critical scenarios | Continuous developer communication |
| No Ruijie device for comparison | P2 | TP-5/TP-6 gap | Use public docs or developer info |

## 7. Deliverables

- Test plan document (this file)
- Detailed test cases per module (.docx format)
- CoPP rate measurement data table
- Test report with bug list and risk assessment

## 8. Out of Scope (Pending Confirmation)

- Basic stacking formation/teardown (assumed covered by existing tests)
- In-Service Software Upgrade (ISSU)
- Stacking loop detection
- Cross-version stacking compatibility
