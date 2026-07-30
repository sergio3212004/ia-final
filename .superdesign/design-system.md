# OptiLab — Design System

## Product context

OptiLab is a Spanish-language educational repository for studying three metaheuristics: Genetic Algorithms, Tabu Search, and Ant Colony Optimization. The frontend is a Vue/Vite application. Python will execute the algorithms behind an API boundary; the web UI configures runs, streams structured logs, plots objective progress, and preserves run history.

Primary users are university students and instructors performing desktop tests (“pruebas de escritorio”). The interface must make every state transition explainable, not merely show the final answer.

## Information architecture

- Dashboard: overview of the three algorithms, recent executions, and quick comparison.
- Algorithm workspace: one reusable view with algorithm-specific parameters.
- Execution detail: summary, convergence/objective chart, current solution visualization, structured log timeline, and raw JSON export.
- History: searchable list of executions with algorithm, status, seed, duration, best objective, and timestamp.
- Method guide: compact explanation of terminology and parameter effects.
- Class exercise presets: faithful, inspectable reproductions of the supplied poster and desktop-test guide.

The initial design target is the Algorithm workspace for a running Genetic Algorithm, with the other two algorithms represented in persistent navigation.

## UX rules

1. Every execution uses a visible random seed so a run can be reproduced.
2. The primary run controls are Configure, Run, Pause, Step, Resume, and Stop.
3. “Step” advances exactly one pedagogical unit: one generation for Genetic, one iteration for Tabu, and one iteration/ant-cycle for ACO.
4. Logs are append-only during a run and include timestamp, sequence, algorithm, phase, iteration/generation, operation, inputs, outputs, objective values, best-so-far, and human-readable explanation.
5. The default log view is structured and readable; raw JSON is secondary.
6. Chart and log selection are synchronized: selecting a point highlights the related log group, and selecting a log focuses its chart point.
7. The objective chart shows current objective, best-so-far, and optionally mean/population objective. Axes and optimization direction must be labeled.
8. A run cannot start until parameters pass validation. Errors are shown beside the field and in an execution preflight summary.
9. The UI must never imply that a heuristic found the global optimum unless a known optimum was provided and matched.
10. Each algorithm keeps comparable metadata while preserving algorithm-specific vocabulary.
11. Genetic Algorithm runs provide two source presets: an 8-bit `[-1,1]` poster example and a 10-bit `[-5,5]` desktop-test guide.
12. A discrepancy between a supplied source value and a recalculated value is shown explicitly; values are never silently corrected.

## Visual direction

Use a reality-first, technical modernist aesthetic adapted from the selected “SaaS Landing Page for Developer Tool” library direction. This is a dense application workspace, not a marketing page.

- Strict grid and visible panel boundaries.
- Flat surfaces; no gradients, glass effects, or decorative shadows.
- Use color sparingly to encode active state, improvement, warnings, and errors.
- Rectangular controls with small 4–6px radii for usability; avoid pill-shaped containers except compact status badges.
- Data and logs take visual priority over decoration.

## Color tokens

Light mode is the initial target.

- `--canvas: #E9E8E3` — page background.
- `--surface: #F7F6F2` — primary panels.
- `--surface-strong: #FFFFFF` — chart and active working areas.
- `--ink: #141414` — primary text.
- `--ink-secondary: #4D4C49` — supporting text.
- `--ink-muted: #77756F` — labels and metadata.
- `--border: #C9C7C0` — grid and panel divisions.
- `--border-strong: #A6A39A`.
- `--accent: #1351AA` — selected algorithm, primary actions, best-so-far line.
- `--accent-soft: #DCE8F8`.
- `--positive: #16744A` — objective improvement/success.
- `--positive-soft: #DDF1E7`.
- `--warning: #A45B00`.
- `--warning-soft: #F6E8D1`.
- `--danger: #B52A2A`.
- `--danger-soft: #F5DDDD`.
- `--log-bg: #171A1F`.
- `--log-ink: #D8DEE9`.
- `--log-muted: #8892A0`.

Algorithm identities use restrained markers, never full-page recoloring:

- Genetic: cobalt `#1351AA`.
- Tabu: amber `#A45B00`.
- Ant Colony: green `#16744A`.

## Typography

Use locally available system fonts only.

- UI sans: `Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif`.
- Data/log mono: `"IBM Plex Mono", "SFMono-Regular", Consolas, monospace`, falling back safely.
- Page title: 30px / 1.1 / 700 / -0.03em.
- Section heading: 18px / 1.25 / 700.
- Panel heading: 14px / 1.3 / 700.
- Body: 14px / 1.5 / 400.
- Label: 11px / 1.3 / 700 / uppercase / 0.12em tracking.
- Data/log: 12px / 1.55 / 400.
- Large metric: 28px / 1 / 700, tabular numbers.

## Layout

- Responsive workspace optimized for desktop, tablet, and mobile.
- Desktop reference: 1440×900. Tablet references: 1024×768 and 768×1024. Mobile references: 390×844 and 360×800.
- Persistent left navigation: 224px.
- Top status bar: 56px.
- Main workspace uses a 12-column grid with 16px gutters and 20px outer padding.
- Algorithm header and run controls span the full content width.
- Left configuration panel: 3 columns.
- Center convergence chart and solution summary: 5 columns.
- Right structured log timeline: 4 columns.
- At widths below 1180px, use a two-column content grid; configuration becomes a drawer and logs move below the chart/table area.
- At widths below 768px, replace the sidebar with a compact top bar and bottom navigation for Dashboard, Algorithms, Run, Logs, and More.
- Mobile is fully functional, not read-only. Users can configure, run, pause, advance a phase/generation, inspect tables, and review logs.
- Mobile content uses a single-column flow with sticky execution controls and a segmented workspace switcher: `Gráfico`, `Tabla`, `Pasos`, `Logs`.
- Tables never shrink columns until unreadable. On mobile, each row becomes a labeled data card by default, with an optional horizontally scrollable “tabla original” view.
- Charts use a minimum 280px height on mobile, responsive labels, fewer tick marks, and touch-sized points.
- Parameter groups become accordions. Summary and validation remain visible above the fold.
- All touch targets are at least 44×44px with 8px separation where possible.
- Avoid nested full-page scrolling: the document scrolls normally; only wide tables may scroll horizontally.
- Sticky regions must account for mobile safe-area insets.

## Components

- App sidebar: wordmark “OPTILAB”, Dashboard, three algorithm items, History, Guide. Active item uses a 3px accent rail.
- Run status bar: connection state to Python, execution ID, seed, elapsed time, and status badge.
- Algorithm header: title, concise description, optimization direction, dataset/problem name, primary run controls.
- Parameter group: labeled numeric/select fields with unit/help text and validation.
- Objective chart: line chart with visible point markers, grid, tooltip, legend, iteration axis, objective axis, and event markers for important improvements.
- Metric strip: best objective, current objective, improvement, iteration/generation, evaluations.
- Structured log: grouped by iteration/generation, expandable operations, severity/state color rail, monospace values, and plain-language explanation.
- Phase table viewer: tabs for Population, Roulette, Crossover, Mutation, New Population, and Summary. Tables show formulas, substituted values, random numbers, and results.
- Function explorer: plots `f(x)=1-x²` and places every individual from the selected generation directly on the curve.
- Binary chromosome row: bit cells with crossover boundaries and mutated-bit highlights.
- Source validation badge: distinguishes entered, source-provided, recalculated, and discrepant values.
- Responsive workspace switcher: desktop shows graph, table, and logs concurrently; mobile switches among them without losing the selected generation or phase.
- Mobile data card: transforms one table row into label/value pairs while retaining chromosome, formulas, probabilities, and intervals.
- Solution snapshot: compact representation appropriate to the problem (chromosome, route, selected nodes, etc.).
- Execution table: sortable rows and consistent algorithm/status badges.
- Buttons: rectangular, 4px radius, 36px height; primary blue, secondary transparent with border, dangerous red.
- Inputs: 36px height, white surface, 1px border, clear focus outline.

## Motion

- 150–220ms ease-out for panel and state changes.
- Chart points animate linearly between iterations; respect `prefers-reduced-motion`.
- New log entries use a subtle 120ms highlight, never auto-scroll if the user has scrolled upward.
- Pausing or stepping must not create decorative motion.

## Accessibility

- Minimum AA contrast.
- Full keyboard navigation and visible 2px focus rings.
- Never rely on color alone: pair state colors with icons/labels.
- Chart has a textual data table alternative.
- Live execution announcements use a polite live region; errors use assertive announcements.
- Log pane supports pause-follow mode and font resizing.

## Design fidelity constraint

Use only the fonts, colors, spacing, and component styles defined here. Do not introduce gradients, decorative serif fonts, neon colors, glassmorphism, or unrelated visual styles.
