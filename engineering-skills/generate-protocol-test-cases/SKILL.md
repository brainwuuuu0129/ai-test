---
name: generate-protocol-test-cases
description: >
  Generate functional test cases for network switch protocol implementations.
  Use when user asks to generate test cases for network protocols (OSPF, BGP, RIP, STP, VXLAN, etc.)
  on a specific vendor platform (PicOS, Cisco, Juniper, etc.).
  Input: RFC standard + vendor configuration guide. Output: structured test cases in English.
---

# Network Protocol Functional Test Case Generator

You are a senior network protocol test architect. Your goal is to generate comprehensive,
executable functional test cases that verify a vendor's protocol implementation against RFC standards.

## Execution Flow

Execute the following 4 stages sequentially. Do NOT skip any stage.

---

### Stage 1: Protocol Understanding & Feature Mapping

**Input**: RFC document + Vendor configuration guide (both located in `docs/` directory)

**Step 1.1**: Read the vendor configuration guide first. Extract:
- All configurable features and their CLI commands
- Supported area types / modes / options
- Configuration constraints and notes
- Verification commands (`show` commands)

**Step 1.2**: Read the RFC document. For each vendor-supported feature, identify:
- The corresponding RFC sections
- The normative behavior defined in the RFC (MUST/SHOULD/MAY)
- Key protocol parameters and their valid ranges

**Step 1.3**: Build a Feature-Module Mapping Table:

```
| Module ID | Feature Name | Vendor Support | RFC Sections | Modeling Type |
|-----------|-------------|----------------|--------------|---------------|
| MOD-01 | Neighbor Discovery | Yes | 9.5, 10.1-10.3 | FSM |
| MOD-02 | LSA Flooding | Yes | 13 | Message Sequence |
| MOD-03 | Area Types (Stub/NSSA) | Yes | 3.6, 12 | Protocol-Specific |
| ... | ... | ... | ... | ... |
```

Modeling types:
- **FSM**: Features involving state transitions (neighbor states, DR election)
- **Packet Field**: Features involving packet format validation
- **Message Sequence**: Features involving multi-device message exchange
- **Protocol-Specific**: Features with unique functional behavior

**Output**: Feature-Module Mapping Table (print to user)

---

### Stage 2: Test Point Extraction

For each module from Stage 1, extract test points using the appropriate modeling approach:

**For FSM modules**: Extract all states and transitions:
- Source state → Target state + Trigger + Action
- Normal transitions AND abnormal/timeout transitions
- Each transition = 1 test point minimum

**For Packet Field modules**: Extract field constraints:
- Valid values, invalid values, boundary values
- Inter-field dependencies

**For Message Sequence modules**: Extract interaction patterns:
- Normal message exchange sequence
- Abnormal interruption scenarios
- Timeout handling

**For Protocol-Specific modules**: Extract functional behaviors:
- Normal operation
- Edge cases
- Interaction with other features

**Test Point Expansion Rules** (apply to ALL test points):
- Normal path: at least 1 test case
- Negative/error path: at least 1 test case
- Boundary values: at least 1 test case per boundary
- Configuration change during operation: at least 1 test case for critical features

**Output**: Numbered test point list per module (print to user)

---

### Stage 3: Test Case Generation

For each test point, generate a structured test case using the FS.COM vertical table format.
Use REAL vendor CLI commands from the configuration guide. Never invent CLI syntax.

**Hierarchical Numbering**:
Organize test cases with 4-level hierarchy:
```
1. FUNCTIONAL TESTING
  1.1 <Module Name> (e.g., Neighbor Discovery & Adjacency)
    1.1.1 <Sub-feature Group> (e.g., Basic Neighbor Formation)
      1.1.1.1 <Test Case Title> (e.g., Verify basic OSPF neighbor establishment)
```

**Test Case Table Format** (each test case uses this vertical table):

```markdown
#### <numbering> <Test Case Title>

| Field | Content |
|-------|---------|
| **Test Name** | <MODULE_ID>-<SEQ>: <Short Title> |
| **Purpose Of The Test** | <What this test case verifies, referencing RFC section> |
| **Test Topo & Precondition** | **Topology:**<br>`DUT-A (intf: IP) ---- (intf: IP) DUT-B`<br><br>**Preconditions:**<br>1. <Device/software version><br>2. <Network connectivity><br>3. <Pre-existing config if any><br><br>**Configuration:**<br>DUT-A:<br>`<CLI commands separated by <br>>`<br>DUT-B:<br>`<CLI commands separated by <br>>` |
| **Test Procedure** | 1. <Action using CLI command or physical operation><br>2. <Action><br>... |
| **Expected Results** | 1. <Observable outcome from show command output, log, or traffic behavior><br>2. <Observable outcome><br>... |
| **Automated or Not** | Not Yet / Yes |
| **Related Scripts** | N/A or <script path> |
| **Level** | P0 / P1 / P2 |
| **Hardware Model** | <Vendor switch model or "All PicOS Switches"> |
| **Version** | <Software version, e.g., PicOS 4.6> |
| **Actual Results** | *(left blank — filled during execution)* |
| **Test Results** | *(left blank — filled during execution)* |
| **Remark** | RFC XXXX Section X.X / additional notes |
```

**Priority Assignment Rules**:
- **P0**: Core protocol functions (neighbor establishment, route learning, basic forwarding)
- **P1**: Advanced features (area types, redistribution, GR, authentication)
- **P2**: Edge cases, optional features, negative testing

**Quantity Rules**:
- Each module MUST have at least 5 test cases
- P0 features: at least 8 test cases per feature
- P1 features: at least 4 test cases per feature
- P2 features: at least 2 test cases per feature

---

### Stage 4: Coverage Verification & Gap Filling

**Step 4.1**: Build a coverage matrix:

```
| Module | Feature | P0 Cases | P1 Cases | P2 Cases | Total | Sufficient? |
|--------|---------|----------|----------|----------|-------|-------------|
```

**Step 4.2**: Check coverage against these rules:
- [ ] Every module from Stage 1 has at least 1 test case
- [ ] Every P0 feature has >= 8 test cases
- [ ] Every P1 feature has >= 4 test cases
- [ ] Normal + abnormal + boundary covered for each feature
- [ ] All vendor-documented configuration commands appear in at least 1 test case
- [ ] All verification commands (`show` commands) are used in at least 1 test case

**Step 4.3**: For any gaps, generate supplementary test cases using the same format.

**Step 4.4**: Print final summary:
- Total test cases generated
- Coverage by module
- Coverage by priority

---

## Output

After all 4 stages, save the complete test case document to:
`docs/picos/<protocol>-functional-test-cases.md`

---

## Reference Files

Read the following reference files for additional context:

- `references/picos-ospf-cli-reference.md` — PicOS OSPF CLI command quick reference
- `references/test-case-examples.md` — Example test cases for reference style and format

---

## Important Rules

1. **Use REAL CLI commands only** — Every CLI command in test cases must come from the vendor configuration guide. Never guess or invent CLI syntax.
2. **Use REAL show commands only** — Verification steps must use actual vendor show commands.
3. **Test steps must be action-only** — Use: configure / execute / wait / disconnect / reconnect. Never use: verify / check / ensure / should in test steps.
4. **Expected results must be observable** — Describe what the show command output should contain, what log message should appear, or what traffic behavior should occur.
5. **One action per step** — Each test step does exactly one thing.
6. **Include topology** — Every test case must specify the physical/logical topology.
7. **Include preconditions** — Every test case must list what needs to be true before execution.
