# GitHub Project Blueprint: Cebu Loop Operations

**Objective**: Persistent, mobile-friendly task tracking for Joy (Cebu) and Brian (Hawaii).

---

## 1. Setup Instructions

1. Go to your GitHub Repository: `Io-kai/Cebu-Loop-Web`.
2. Click the **Projects** tab -> **New Project**.
3. Select **Board** template.
4. Link it to this repository.

---

## 2. Column Structure (The 16-Week Flow)

Rename the default columns to match the Field Manual phases:

1. 📋 **Phase 0: The Bag Builder** (Immediate Backlog)
2. 🔴 **Phase 1: Legal Shield** (Active - Week 1-3)
3. 🟡 **Phase 2: Paper Hub** (Weeks 4-6)
4. 🟠 **Phase 3: Asset Commitment** (Weeks 7-10)
5. 🟢 **Phase 4: Launch Sprint** (Weeks 11-16)
6. ✅ **CONCLUDED** (Archive)

---

## 3. Custom Fields (Add these)

* **Owner** (Single Select): `Joy`, `Brian`, `Liaison`.
* **Gate Condition** (Checkbox): Marks if this task is a "Gate" (Blocker) for the next phase.
* **Location** (Text): `Marco Polo`, `SEC`, `BYD`, `Ayala`, `LTFRB`.

---

## 4. Recommended Views

* **Operations View** (Board): Grouped by **Status**. Use this for daily field work.
* **Roadmap View** (Chart/Timeline): Use this for the Tuesday/Thursday syncs to see the 16-week burn-down.
* **Gatekeeper View** (Table): Filter for `Gate Condition = Checked`. This shows exactly what must be done to unlock capital spend ($).

---

## 5. Automation Rules

* When a new issue is added with label `legal` -> Move to **Phase 1**.
* When a task is moved to **CONCLUDED** -> Update field `Status` to `Done`.
