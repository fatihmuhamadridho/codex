---
name: atomic-design
description: Use for reviewing or refactoring UI with Atomic Design, including atoms, molecules, organisms, templates, and pages.
---

# Atomic Design

## Overview

Use this skill to classify UI pieces into atomic layers, choose the right extraction boundary, and refactor incrementally without turning the component tree into abstraction noise.

Prefer the smallest structural change that produces a clearer ownership model. Do not force every component into a deeper layer if the result reduces readability or creates prop plumbing.

## Core Workflow

1. Identify the user-facing surface being changed or reviewed.
2. List the visible parts and their responsibilities before touching structure.
3. Classify each part as atom, molecule, organism, template, or page based on responsibility, not file size.
4. Extract only the unstable or repeated boundaries first.
5. Re-check data flow, styling ownership, and naming after each split.

## Classify Components

### Atom

Treat a unit as an atom when it is a basic UI primitive with minimal business meaning.

Common examples:
- Button
- Input
- Label
- Icon
- Avatar
- Badge

Use atoms for:
- Single-purpose visual primitives
- Tiny wrappers around native elements
- Token-driven styling surfaces

Do not make an atom responsible for:
- Fetching data
- Layout orchestration across sections
- Domain-specific behavior that only makes sense in one feature

### Molecule

Treat a unit as a molecule when it combines a few atoms into a meaningful control.

Common examples:
- Search field with input and button
- Form field with label, hint, and error text
- Product card header
- Navigation item with icon and label

Use molecules for:
- Small composite controls
- Repeated interaction patterns
- Groups whose meaning appears only after atoms are combined

Do not make a molecule responsible for:
- Full-page layout
- Cross-section coordination
- Feature workflows spanning multiple panels

### Organism

Treat a unit as an organism when it coordinates multiple molecules or atoms into a substantial section.

Common examples:
- Header bar
- Sidebar navigation
- Pricing table section
- Checkout summary panel
- Comment list section

Use organisms for:
- Distinct sections on a screen
- Stateful sections with several child components
- Composition boundaries that appear in multiple templates or pages

Allow an organism to own local section behavior, but keep page routing, screen-level fetching, and global orchestration outside unless the existing architecture requires a temporary adapter.

### Template

Treat a unit as a template when it defines structure and placement without being the final screen instance.

Common examples:
- Dashboard shell
- Marketing landing layout
- Product detail layout
- Auth page layout

Use templates for:
- Reusable screen skeletons
- Slot-based arrangement of organisms
- Layout rules shared by multiple pages

Keep templates light on content-specific decisions. They should define where things go, not encode final copy or one-off scenario logic.

### Page

Treat a unit as a page when it represents a concrete screen instance with real content, routing context, and feature-specific data wiring.

Use pages for:
- Route-level composition
- Final data selection and screen state
- One-off screen decisions that should not become reusable library rules

Prefer pages to assemble templates and organisms rather than bypassing them with direct primitive composition unless the screen is too small to justify more structure.

## Extraction Rules

Extract a new component only when at least one of these is true:
- The UI chunk has a stable responsibility and a clear name
- The same pattern appears in multiple places
- The parent component mixes unrelated concerns
- A section needs isolated tests or isolated state
- Styling ownership is easier to understand after extraction

Keep logic in place when:
- The candidate component would only forward props with no meaningful boundary
- The name would be vague, such as `Section`, `Wrapper`, or `ContentBlock`
- The split creates more indirection than reuse
- The structure is still changing rapidly and the boundary is not stable

## Naming and Ownership

Name components by role, not shape.

Prefer:
- `ProductCard`
- `CheckoutSummary`
- `ProfileHeader`
- `SearchField`

Avoid:
- `BoxOne`
- `Container2`
- `ThingWrapper`
- `LeftPart`

Let each level own the concerns that naturally belong to it:
- Atoms own primitive presentation and token application
- Molecules own compact interaction groupings
- Organisms own section composition and local section state
- Templates own layout composition
- Pages own route context, concrete content, and page-level data decisions

## Data and Styling Heuristics

Keep data flow as high as practical, then pass only what each layer needs.

Prefer:
- Pages selecting feature data
- Templates receiving slots or structured child content
- Organisms handling local interaction state for their section
- Atoms exposing predictable style and behavior surfaces

Avoid:
- Atoms reading feature stores directly
- Molecules depending on route objects
- Organisms importing page-only constants
- Templates owning ad hoc business logic

If styling rules are shared across many screens, push them downward into reusable layers. If styling exists only for one screen story, keep it at template or page level.

## Refactor Strategy

When migrating an existing screen:

1. Mark obvious page-only logic and keep it in the page.
2. Identify large repeated sections and extract them into organisms.
3. Reduce each organism into smaller molecules only where the subparts are meaningful.
4. Convert generic primitives into atoms only after their API is stable.
5. Rename files and folders to reflect responsibility after the structure settles.

Prefer incremental migration over a full rewrite. Preserve behavior first, then improve boundaries.

## Anti-Patterns

Watch for these failures:
- Over-fragmentation where every three lines become a new component
- “Atoms” that encode product-specific rules
- Molecules used as full-screen layouts
- Organisms directly coupled to one page's routing or fetch layer
- Templates filled with final copy and feature branching
- Pages bypassing the system and composing dozens of atoms directly without need

If a proposed split makes the mental model harder to explain, reject it.

## Review Checklist

Before finishing, verify:
- Each extracted component has one clear responsibility
- Reuse claims are real, not hypothetical
- Names describe role and domain meaning
- Props match the abstraction level
- Page-specific logic does not leak into lower layers
- The resulting tree is easier to navigate than before

## Trigger Examples

Use this skill for requests like:
- “Refactor komponen dashboard ini ke atomic design.”
- “Pisahin screen ini jadi atom, molecule, dan organism yang masuk akal.”
- “Review struktur component library ini, ada boundary yang salah nggak?”
- “Bantu migrasi UI lama ke atomic design tanpa over-engineering.”
- “Rapihin folder komponen biar page concern tidak bocor ke reusable layer.”
