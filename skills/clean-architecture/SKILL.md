---
name: clean-architecture
description: Use for reviewing or refactoring codebases with clean architecture, layer boundaries, dependency direction, and business-rule isolation.
---

# Clean Architecture

## Overview

Use this skill to review an existing codebase through boundary ownership and dependency direction, then propose the smallest structural changes that make responsibilities clearer.

Default to incremental cleanup. Do not recommend a full rewrite when adapters, seams, or boundary extraction can fix the problem with less risk.

## Core Workflow

1. Identify the concrete surface being reviewed: feature, module, service, route, screen, or job.
2. List the current responsibilities before trusting folder names.
3. Classify code into `domain`, `application`, `interface/adapters`, or `infrastructure/presentation` based on what it does.
4. Trace dependencies inward and note every place where outer concerns leak into inner layers.
5. Recommend the minimum refactor that restores dependency direction and reduces coupling.

## Default Layer Model

Use these terms by default:
- `domain`
- `application` or `use case`
- `interface/adapters`
- `infrastructure` or `presentation`

Map repo-specific terms into this model instead of forcing a rename immediately.

Examples:
- `core`, `model`, or `entities` often map to `domain`
- `services`, `actions`, or `usecases` often map to `application`
- `controllers`, `presenters`, `mappers`, or `gateways` often map to `interface/adapters`
- `http`, `db`, `orm`, `ui`, `framework`, or `sdk` often map to `infrastructure/presentation`

## Classify Responsibilities

### Domain

Treat code as `domain` when it represents business rules, invariants, policies, or concepts that should survive framework changes.

Common examples:
- Entities
- Value objects
- Domain services
- Validation rules tied to business meaning
- Policy calculations

`domain` may know:
- Domain concepts
- Business rules
- Stable abstractions that do not expose technical details

`domain` must not know:
- HTTP
- Database drivers or ORM models
- UI framework state
- Queue clients
- File system details

### Application / Use Case

Treat code as `application` when it coordinates work to fulfill a user or system action.

Common examples:
- Create order
- Sync account
- Approve invoice
- Load dashboard use case
- Export report workflow

`application` may know:
- Domain types and rules
- Ports or repository interfaces
- Transaction or orchestration policy
- Input and output models for use cases

`application` must not know:
- Concrete transport details
- Controller objects
- ORM-specific query APIs
- UI widget trees

### Interface / Adapters

Treat code as `interface/adapters` when it translates between external shapes and inner use-case shapes.

Common examples:
- Controllers
- Presenters
- View models
- Repository adapters
- DTO mappers
- Serializer/deserializer boundaries

Use adapters for:
- Translating request and response formats
- Converting persistence models to domain models
- Preparing UI-facing state from use-case output

Adapters should remain thin. If business policy starts living here, move it inward.

### Infrastructure / Presentation

Treat code as `infrastructure/presentation` when it depends directly on frameworks, runtimes, or external systems.

Common examples:
- Database implementations
- HTTP framework handlers
- SDK clients
- Filesystem access
- Message broker producers
- UI framework components and screens

Outer layers may depend inward. Inner layers must not depend outward.

## Dependency Direction Rules

Prefer this direction:
- `infrastructure/presentation` -> `interface/adapters` -> `application` -> `domain`

Allow direct calls into inner layers only when they preserve this direction.

Reject these patterns:
- `domain` importing framework or transport code
- `application` importing controllers, SDK clients, or ORM models
- Adapters reaching across layers to execute business decisions on their own
- Shared utility packages becoming a hidden backdoor for outer-layer concerns

If a dependency is necessary but points outward, introduce a port, interface, or mapper at the inner boundary and implement it outside.

## Review Heuristics

When reviewing a file or module, ask:
- Is this code making a business decision or only translating data?
- Would this code still make sense if the framework changed?
- Does this dependency point inward or outward?
- Is this module named after technical shape instead of responsibility?
- Is one component mixing orchestration, transport, and persistence at once?

Use responsibility over location. A file in `domain/` is not domain code if it imports controllers or SQL models.

## Common Violations

Watch for these failures:
- Domain models annotated with persistence or transport concerns
- Use cases returning framework-specific response types
- Controllers performing business branching instead of delegating to use cases
- Repositories exposing ORM entities directly to the application or domain layer
- UI or API handlers reaching into database code without an application boundary
- “Shared” helpers importing everything and creating implicit coupling
- Validation split across controller, adapter, and domain with no clear ownership

## Minimal Refactor Strategy

When the architecture is messy:

1. Keep the current behavior stable.
2. Extract one clear use-case boundary around a real workflow.
3. Move business rules inward into `domain` or `application`.
4. Add adapters to translate outer models into inner models.
5. Hide concrete DB, HTTP, UI, or SDK calls behind outward implementations of inward-facing interfaces.
6. Rename and relocate only after the responsibilities are actually separated.

Prefer transitional seams over broad restructuring:
- Add a mapper before replacing an entire module.
- Introduce a repository interface before changing storage.
- Wrap framework objects at the edge before rewriting business logic.

## Naming and Ownership

Name modules by responsibility, not mechanism.

Prefer:
- `ApproveInvoice`
- `OrderRepository`
- `ProfilePresenter`
- `SyncAccountUseCase`

Avoid:
- `Utils`
- `Helpers`
- `Manager`
- `CommonService`

Let each layer own what naturally belongs there:
- `domain` owns business meaning and invariants
- `application` owns workflow coordination
- `interface/adapters` own translation at boundaries
- `infrastructure/presentation` own framework and runtime details

## Testing Guidance

Use the architecture to decide test focus:
- Test `domain` with fast rule-focused unit tests
- Test `application` with use-case tests over ports/fakes
- Test adapters with mapping and translation tests
- Test infrastructure with integration tests against real frameworks or systems when needed

Do not force heavy end-to-end tests to validate logic that belongs in inner layers.

## Anti-Patterns

Reject these moves:
- Putting every class behind an interface without a boundary need
- Creating layers as folders only, while dependencies still point the wrong way
- Calling a module `clean` while business rules still live in controllers or UI
- Building a “shared” package that mixes domain rules, transport helpers, and persistence code
- Splitting a simple feature into too many layers when there is no meaningful boundary

If a proposed architecture creates more ceremony than clarity, simplify it.

## Review Checklist

Before finishing, verify:
- Business rules are isolated from framework details
- Dependencies point inward
- Ports and interfaces exist only where they protect a real boundary
- Application workflows are visible and not buried in controllers or infrastructure
- Adapters translate instead of owning policy
- The suggested refactor is smaller and safer than a rewrite

## Trigger Examples

Use this skill for requests like:
- “Review service ini, ada pelanggaran clean architecture nggak?”
- “Cari dependency yang salah arah antara domain dan infra.”
- “Bantu rapihin boundary use case, adapter, dan repository.”
- “Audit codebase ini, business rule bocor ke controller atau framework nggak?”
- “Pisahin orchestration, adapter, dan persistence tanpa rewrite besar.”
