# CRITICAL DECISIONS LOG

**Status**: Open Questions for Founder Review
**Date**: January 2026

This document tracks high-stakes decisions that require debate or selection between Option A and Option B. These decisions block specific phases of the `MASTER_EXECUTION_FIELD_MANUAL`.

---

## 1. STRATEGY: The "Airport Drain" Solution

**Context**: High demand for Airport -> City trips will leave the Airport hub empty and the City hub full. We need a rebalancing mechanism.

* **Option A: The Reverse Incentive (User-Led)**
  * *Mechanism*: Offer 50% discount to customers willing to drive City -> Airport.
  * *Pro*: Zero operational cost.
  * *Con*: Unreliable. Users fly when they need to, not when we pay them to.
* **Option B: The Deadhead Run (Staff-Led)**
  * *Mechanism*: Fleet Runner drives car to Airport, takes Angkas (MotoTaxi) back.
  * *Pro*: Guaranteed availability.
  * *Con*: Cost of Angkas fare (~₱150) + Staff time.
* **Required Decision Date**: Week 11 (Before App Config)

---

## 2. TECHNOLOGY: The Core Platform Vendor

**Context**: We need a white-label rental platform for bookings, payments, and digital keys.

* **Option A: RentCentric**
  * *Status*: Industry veteran.
  * *Pro*: Deep feature set, proven API for keyless entry.
  * *Con*: Older UI, potentially expensive per-vehicle pricing.
* **Option B: Navotar**
  * *Status*: Newer challenger.
  * *Pro*: Mobile-first design, potentially better "modern" feel.
  * *Con*: Integration with Teltonika hardware for remote unlock needs verification.
* **Required Decision Date**: Week 5 (See Roadmap)

---

## 3. LEGAL: Regulatory Classification

**Context**: We are operating a chauffeured service ("Rent-a-Car with Driver") but using an App.

* **Option A: Pure "Rent-a-Car" (The Loophole)**
  * *Mechanism*: Every booking is a "Lease Contract".
  * *Risk*: If customers perceive it as a Taxi (TNVS), LTFRB may crackdown.
  * *Defense*: We do not charge per km/minute, we charge per "Block" (Lease).
* **Option B: TNVS (The "Grab" Route)**
  * *Mechanism*: Apply for TNC accreditation.
  * *Risk*: Extremely long timeline, moratoriums, high competition with Grab.
* **Recommendation**: Stick to Option A (Rental) for Launch.

---

## 4. FINANCE: The "Brian Veto" Threshold

**Context**: Current policy requires Brian's digital approval for any expense > ₱10,000.

* **Question**: Is this too low?
  * *Scenario*: If a car needs 4 tires (₱15k), Joy visits valid vendor, but Brian is asleep (Hawaii time).
  * *Risk*: Operations halt for 8 hours.
  * *Proposal*: Raise auto-approval limit to ₱20,000 for "Emergency Repairs" specifically?

---

## 5. ASSETS: The Typhoon "Safe Haven"

**Context**: We need a high-ground parking garage during Signal No. 1.

* **Option A: Ayala Center Cebu (Level 5+)**
  * *Pro*: Massive capacity, secure.
  * *Con*: Public access, paid hourly parking.
* **Option B: Marco Polo Hotel (Nivel Hills)**
  * *Pro*: Brian's residence, very high ground (mountain).
  * *Con*: Limited slots, might annoy HOA if we dump 5 branded cars there.

---
