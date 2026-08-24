# Robo-Nexus — Humanoid Robot Fleet Management Database

**A full-stack database systems project: from ERD to enforced business rules to a custom Python ORM and service API.**

![MySQL](https://img.shields.io/badge/MySQL-8+-blue)
![Python](https://img.shields.io/badge/Python-3.13+-yellow)
![Database Design](https://img.shields.io/badge/Database-Design-3NF%20%7C%20Triggers-green)
![ORM](https://img.shields.io/badge/ORM-Custom%20(domain--specific)-orange)
![Course](https://img.shields.io/badge/CSC_675%2F775-SFSU-lightgrey)

> **Team Robo-Nexus** · CSC 675/775 Database Systems · San Francisco State University  
> **Author highlight:** [Kiran Khatri](https://github.com/khatri5034) — Team Lead · schema modeling · ORM relationships · integration & demos

---

## Why this project matters

Modern robot fleets need more than CRUD: **battery safety**, **task scheduling**, **maintenance locks**, **AI request pipelines**, and **auditability** must hold even when multiple apps talk to the same database. Robo-Nexus models that problem end-to-end—**integrity lives in the database**, and applications consume data through a **stable service layer**, not ad-hoc SQL.

This repo is a **semester-long, milestone-driven build** (requirements → normalized schema → triggers → custom ORM → presentation). It reads like real team software engineering, not a single homework script.

---

## Domain at a glance

| Area | Examples in the schema |
|------|-------------------------|
| **Fleet & deployment** | Robots, models, software versions, deployment locations (home, hospital, warehouse, factory) |
| **Operations** | Tasks, assignments, executions, charging sessions, energy status |
| **AI pipeline** | AI models, requests, responses, robot roles |
| **People & support** | Users, technicians, maintenance, alerts, support requests |
| **Interaction & analytics** | Interaction sessions, emotional records, performance metrics |

**Database name:** `robo_nexus` · **~47 tables** · **15 documented business rules** with MySQL triggers/procedures

---

## Milestone journey — what we built & what I learned

### Milestone 1 — Requirements & conceptual design (10 pts)
**Deliverables:** EER diagram (Draw.io), functional/non-functional requirements, competitive analysis, entity catalog.

**What I learned**
- How to turn a vague “fleet management” idea into **named entities, relationships, and constraints** before writing SQL.
- Why **deployment context** (home vs hospital vs warehouse) and **AI/emotion subsystems** belong in the model early—not bolted on later.
- Team coordination: shared `.drawio`, PR-based contributions, defending design choices in review.

**My contributions:** project description & TOC, competitive analysis, requirements for AI pipeline / robot roles / interaction sessions / deployment environments, ERD co-design.

---

### Milestone 2 — Normalization & logical schema (15 pts)
**Deliverables:** `Schema.sql`, normalization narrative, seed data (`inserts.sql`), 3NF-oriented table design.

**What I learned**
- **1NF → 3NF (and beyond where needed)** as a design conversation, not a checkbox—when to decompose vs when a join is acceptable.
- Modeling **many-to-many** and **lookup/associative** tables (e.g. task assignments linking robots, users, and tasks).
- **Foreign keys, ENUM domains, and CASCADE rules** as the contract between application and database.
- Translating EER → **executable MySQL DDL** in DataGrip/MySQL Workbench.

**Outcome:** Production-style schema with referential integrity across robots, tasks, AI flows, charging, maintenance, and support.

---

### Milestone 3 — Business rules in the database (20 pts)
**Deliverables:** `business_rules.md`, `business_rules.sql` (triggers/functions/procedures), `rules_testing.sql`.

**What I learned**
- **Why rules belong in the DB:** any client (Python, future REST API, admin tool) gets the same guarantees; triggers cannot be “forgotten” by app code.
- Implementing **BEFORE INSERT/UPDATE triggers**, `SIGNAL SQLSTATE '45000'`, and cross-table checks (e.g. latest battery from `EnergyStatus`, open AI request with no `AIResponse`).
- Testing **failure paths** deliberately—success inserts are easy; **rejected inserts** prove the design works.

**Sample rules enforced**
| Rule | Idea |
|------|------|
| Battery floor | No task execution below 20% battery |
| One active task | Robot cannot run overlapping active executions |
| Single open AI request | Second request blocked until first is answered |
| Task assignment gate | Execution requires a valid `TaskAssignment` |
| Maintenance / charging | Operational state conflicts blocked at insert time |

---

### Milestone 4 — Custom ORM & service API (15 pts)
**Deliverables:** Domain-specific Python ORM (`orm/`), models (`models/models.py`), public API (`services/services.py`), demo scripts & rule checks.

**What I learned**
- Building a **narrow ORM** (not SQLAlchemy)—`Base` CRUD, dynamic schema creation, connection lifecycle, **identity map**, lazy relationships, backreferences.
- **Three-layer separation:** ORM engine → domain models → **services** (the only surface app code should call).
- Mapping **MySQL types & FK names** to Python (e.g. `AIRequestsID` column ↔ `AIRequest` model).
- Writing **demonstration scripts** that prove relationships, filters, and service flows without raw SQL in callers.

**Architecture**

```text
Application / demos (tests.py, tests_services.py, constraintcheck.py)
        │
        ▼
services/services.py          ← public API (create_user, register_robot, assign_task_to_robot, …)
        │
        ▼
models/models.py              ← one class per table, Relationship() definitions
        │
        ▼
orm/                          ← base, columns, datatypes, relationships, migrations, db_connectors
        │
        ▼
MySQL (robo_nexus)            ← schema + triggers from Milestone 3
```

**My contributions (M4):** `Users`, `RobotRoles`, `RobotModels`, `DeploymentLocations` models; **`orm/relationships.py`** (lazy load, caching, backreferences); **`constraintcheck.py`** for live rule verification; test/service integration fixes.

---

### Milestone 5 — Presentation & ownership (10 pts)
**Deliverables:** Architecture walkthrough—schema ↔ rules ↔ ORM ↔ services, live demo, tradeoff discussion.

**What I learned**
- Explaining **why** (normalization choices, DB vs app validation) matters as much as **what** shipped—mirrors industry design reviews.

---

## Tech stack

| Layer | Tools |
|-------|--------|
| **Database** | MySQL 8+ |
| **Design** | Draw.io (EER), DataGrip / MySQL Workbench |
| **Application** | Python 3, `mysql-connector-python`, `python-dotenv` |
| **Process** | GitHub, PR reviews, team `contributions.md` per milestone |

---

## Repository layout

```text
milestones/
├── milestone1/          # Requirements, EER, contributions
├── milestone2/          # Schema.sql, normalization, seed data
├── milestone3/          # business_rules.md, business_rules.sql, rule tests
├── milestone4/          # ORM, models, services, demos
│   ├── orm/            # base, relationships, columns, datatypes, migrations
│   ├── models/models.py
│   ├── services/services.py
│   ├── tests.py        # ORM & relationship demos
│   ├── tests_services.py
│   └── constraintcheck.py   # live business-rule checks
└── milestone5/          # presentation notes
```

---

## Quick start

### 1. Database

Create and load schema (adjust host/user as needed):

```bash
mysql -u YOUR_USER -p < milestones/milestone2/Schema.sql
mysql -u YOUR_USER -p robo_nexus < milestones/milestone3/business_rules.sql
```

Optional seed data:

```bash
mysql -u YOUR_USER -p robo_nexus < milestones/milestone2/inserts.sql
```

### 2. Python environment

```bash
cd milestones/milestone4
python3 -m venv .venv
source .venv/bin/activate
pip install mysql-connector-python python-dotenv
```

Create `milestones/milestone4/.env`:

```env
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=robo_nexus
```

### 3. Run demos

```bash
# Service-layer workflow (users → robots → tasks → AI)
python tests_services.py

# ORM relationships, filters, backreferences
python tests.py

# Business rules: second AI request, role update, execution without assignment
python constraintcheck.py
```

---

## Skills demonstrated (recruiter checklist)

- **Relational modeling:** EER → normalized schema, FK design, ENUM domains  
- **SQL & integrity:** DDL, DML, triggers, cross-table validation  
- **Systems thinking:** enforce invariants at the DB boundary; expose safe APIs above it  
- **Python & tooling:** custom ORM patterns (registry, identity map, lazy loading)  
- **Team delivery:** milestone cadence, PR workflow, documented ownership  
- **Testing mindset:** happy-path demos + intentional constraint violation checks  

---

## Team — Robo-Nexus

| Member | GitHub | Role |
|--------|--------|------|
| **Kiran Khatri** | [khatri5034](https://github.com/khatri5034) | Team Lead |
| Ishaank Zalpuri | izalpuri-creator | |
| Kerry Yu | Kerry3616 | |
| Dias Almat | vincivv | |
| Etienne Ghashehbaba | Ahe4d | |
| Shadi Daher | shadii10 | |

Per-milestone details: `milestones/milestone*/contributions.md`

---

## Contact

**Kiran Khatri** · kkhatri@sfsu.edu · [GitHub](https://github.com/khatri5034)

---

*Developed as the capstone database project for CSC 675/775, San Francisco State University (2026).*
