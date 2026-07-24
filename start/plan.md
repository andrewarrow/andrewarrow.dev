# Plan: Add a "Build Reddit Slowly" Section

## Current Page Fit

`index.html` is a single-page beginner roadmap for people learning to build with ChatGPT, Codex, Git, the terminal, web basics, hosting, and mobile. The tone is practical, direct, and beginner-friendly. The new section should extend the existing roadmap after section 13 as a capstone track, not replace the beginner material.

Suggested new section:

- Number: `14`
- Anchor: `build-reddit-slowly`
- Title: `Build a Reddit-like app slowly, from one simple homepage to a serious platform.`
- Short TOC bullets:
  - first homepage from seeded posts
  - React, Vite, Go, and PostgreSQL
  - prompt, run, paste errors, repeat
  - scale only when the app earns it

## Core Message

This should not be presented as "build all of Reddit in one sprint." The learner should understand that the first goal is tiny:

- A logged-out homepage.
- A few seeded posts in PostgreSQL.
- A Go API endpoint that returns those posts.
- A simple React/Vite frontend that displays the feed.
- No accounts, no comments, no voting, no moderation, no ranking, no recommendations, no Redis, no queues, no search, no mobile app.

The lesson is not just the code. The lesson is learning how to work with Codex:

- Ask for a small next step.
- Run what Codex gives you.
- Read the error without panic.
- Paste the exact error back into Codex.
- Ask Codex to explain the issue in plain English.
- Apply the fix.
- Repeat.

## Why We Do Not Build for Reddit Scale on Day One

The section should explicitly teach this product and engineering idea:

We are building a Reddit-like app as if it is a brand-new site, not an existing giant. Real Reddit-scale systems require expensive infrastructure, specialized databases, caching layers, queues, observability, abuse tooling, and engineering time. That complexity makes sense only after traffic and usage justify it.

Day one assumptions:

- Traffic is low.
- The team is tiny.
- Hosting budget matters.
- We do not know if users will care.
- Simple code is easier to understand, debug, and change.
- The first real bottleneck may not be the one we guessed.

Teaching phrase:

> We start with the simple version because it is cheap, understandable, and easy to change. Later, when parts of the system start to "run hot," we use that pressure to learn the next computer science concept and rewrite the part that actually needs help.

## Recommended Course Structure

Do not promise "complete Reddit in 90 days." That creates the wrong expectation. A better structure:

- Phase 1: 90 days to a low-traffic, usable Reddit-like MVP.
- Phases 2-11: ten more 90-day phases that gradually turn the MVP into a serious, scalable community platform.
- Total arc: about 33 months if the learner keeps going.

This lets the first page section stay approachable while still showing the long-term path to millions of users.

## Phase 1: First 90 Days, Tiny Reddit MVP

Goal: a simple site where logged-out users can see posts, then logged-in users can create posts and comments.

### Weeks 1-2: Project Setup and Static Shape

User outcome:

- Create a project folder.
- Install React with Vite using plain JavaScript.
- Create a Go backend.
- Start a local PostgreSQL database.
- Understand how frontend, backend, and database fit together.

Concepts:

- Project folders
- Terminal commands
- Localhost
- HTTP request and response
- JSON
- Environment variables
- Git checkpoints

Example Codex prompt:

```text
I want to start a beginner-friendly Reddit-like web app.
Use plain JavaScript, React, Vite, a Go backend, and PostgreSQL.
Do not use TypeScript.
Do not add auth, comments, voting, caching, queues, Docker, Redis, or search yet.

First, inspect this empty project folder and propose the smallest file structure.
Then create only the setup needed to show a React homepage and a Go health check endpoint locally.
Explain the commands I should run after you make the files.
```

### Weeks 3-4: Seeded PostgreSQL Posts

User outcome:

- Create database tables for communities and posts.
- Seed a handful of fake posts.
- Build one Go endpoint like `GET /api/posts`.
- Display those posts in the React homepage.

The first homepage should be much simpler than the screenshot:

- Basic header with site name.
- Main feed column.
- Each post shows community name, title, score, comment count, and age.
- Optional simple right rail on desktop only.
- Logged-out user can read but not post.
- No modals, no infinite scroll, no live ranking, no account menu.

Concepts:

- Tables, rows, columns
- Primary keys and foreign keys
- SQL select queries
- API handlers
- Fetching data from the browser
- Loading, empty, and error states

Example Codex prompt:

```text
Add the first real feature: a logged-out homepage feed.

Requirements:
- Use PostgreSQL as the source of truth.
- Add a small schema for communities and posts.
- Add seed data with 8 realistic posts.
- Add a Go endpoint that returns posts as JSON.
- Update the React homepage to fetch and display those posts.
- Keep the UI simple and readable, inspired by a Reddit feed but not a clone.
- Include loading, empty, and error states.
- Do not add login, comments, voting behavior, infinite scroll, Redis, or queues yet.

After making changes, tell me exactly which commands to run and in what order.
```

### Weeks 5-6: Create Posts

User outcome:

- Add a basic form to create a post.
- Store new posts in PostgreSQL.
- Refresh the feed after creation.

Concepts:

- HTML forms in React
- Controlled inputs
- POST requests
- Server validation
- SQL insert
- Error messages near fields

Example Codex prompt:

```text
Add the smallest possible create-post flow.

A user should be able to enter a title and body, choose one seeded community, submit the form, and see the post appear in the feed.
Do not add accounts yet. Use a temporary anonymous author field if needed.
Validate required fields on the server and show friendly errors in the UI.
Keep the design simple and mobile-friendly.
```

### Weeks 7-8: Comments

User outcome:

- Click a post.
- See a post detail page.
- Add simple comments.

Concepts:

- Routes
- URL parameters
- One-to-many relationships
- SQL joins
- Basic page states

Example Codex prompt:

```text
Add a post detail page with comments.

When I click a post in the feed, I should go to a detail route.
The detail page should show the post and a list of comments from PostgreSQL.
Add a simple comment form.
Keep comments flat for now. Do not add threaded replies yet.
```

### Weeks 9-10: Accounts and Sessions

User outcome:

- Sign up.
- Log in.
- Log out.
- Create posts as a real user.

Concepts:

- Password hashing
- Sessions or cookies
- Authentication vs authorization
- Protected endpoints
- Current user API

Example Codex prompt:

```text
Add beginner-friendly email/password accounts.

Use secure password hashing.
Use cookie-based sessions.
Add signup, login, logout, and a current-user endpoint.
Make post creation require login.
Do not add OAuth, 2FA, private messages, or roles yet.
Explain the security decisions in plain English after the code changes.
```

### Weeks 11-12: Voting, Sorting, and First Deployment

User outcome:

- Logged-in users can upvote posts.
- Feed can sort by newest or top.
- App deploys to a low-cost host.

Concepts:

- Unique constraints
- Idempotent actions
- Sorting
- Basic indexes
- Deployment environment variables
- Production database connection strings

Example Codex prompt:

```text
Add simple post voting and feed sorting.

Logged-in users can upvote or remove their upvote.
The feed can sort by newest or top.
Use PostgreSQL constraints so one user cannot upvote the same post twice.
Do not add downvotes, ranking algorithms, caching, or background jobs yet.
```

## Debugging Lessons to Build Into the Course

The course should repeatedly show learners how to recover from normal failures.

### Where Errors Appear: Browser, Terminal, or Both

Learners need to understand that "the app is broken" is not specific enough. The first debugging skill is learning where the error appeared.

Frontend errors often appear in the browser developer tools:

- In Chrome: right-click the page, choose `Inspect`, then open the `Console` tab.
- In Firefox: right-click the page, choose `Inspect`, then open the `Console` tab.
- JavaScript errors, React rendering errors, missing variables, failed imports, and browser security warnings often show up here.
- The `Network` tab is useful when the frontend tried to call the Go API but received a `404`, `500`, CORS error, or no response.

Backend errors often appear in the terminal where the Go server is running:

- Go compile errors appear when the backend fails to start.
- Database connection errors appear when the API cannot reach PostgreSQL.
- Handler panics or SQL errors may appear when the browser calls an API endpoint.
- These errors may not appear in the browser console except as a generic failed request.

Sometimes both places matter:

- The browser console may show `Failed to fetch`.
- The network tab may show that `/api/posts` returned `500`.
- The Go terminal may show the real reason, such as a missing table or bad SQL query.

Teach this habit early:

1. Copy the browser console error if the page is blank or a button does nothing.
2. Copy the network request details if an API call fails.
3. Copy the Go terminal output if the backend crashes or returns `500`.
4. Paste all relevant pieces into Codex and say where each one came from.

Example prompt:

```text
The homepage is not loading posts.

Browser console:
[paste console error]

Browser network tab:
[paste failed request, status code, and response if visible]

Go server terminal:
[paste backend log output]

Please tell me which layer is failing: React frontend, browser/network, Go API, or PostgreSQL.
Explain the evidence, then make the smallest fix.
```

### PostgreSQL Not Running

Likely error examples:

- `connection refused`
- `could not connect to server`
- `role does not exist`
- `database does not exist`
- `password authentication failed`

Example prompt:

```text
I ran this command:

[paste command here]

I expected the app to connect to PostgreSQL, but I got this error:

[paste the full error here]

Please explain what the error means in beginner language.
Then give me one likely fix at a time.
Do not rewrite unrelated code yet.
```

### Frontend Blank Page

Example prompt:

```text
The browser page is blank.
Here is the terminal output from Vite:

[paste output]

Here is the browser console error:

[paste console error]

Find the likely cause and make the smallest fix.
```

### API Error or CORS Issue

Example prompt:

```text
The React app cannot load posts from the Go API.
Here is the browser network error and the Go server log:

[paste both]

Please explain whether this is a CORS problem, a wrong URL, a server crash, or a database issue.
Make the smallest fix and tell me how to test it.
```

### Migration or Seed Data Problem

Example prompt:

```text
My database setup failed.
Here is the schema or seed command I ran:

[paste command]

Here is the full output:

[paste output]

Help me understand whether the table already exists, the database is missing, or the SQL has a syntax problem.
```

## The "Run Hot" Scaling Arc

The course should introduce scale only when the app has a reason for it. Each scaling phase starts with a symptom, then teaches the concept needed to fix it.

Examples:

- Symptom: homepage loads slowly.
  Concept: SQL indexes, query plans, `EXPLAIN`, pagination.
- Symptom: production errors are hard to understand from user reports alone.
  Concept: logs, metrics, traces, error tracking, Datadog, OpenTelemetry, Prometheus, Grafana, Loki, or another open-source telemetry stack.
- Symptom: repeated requests hit the database too often.
  Concept: caching with Redis or Valkey.
- Symptom: image uploads slow down post creation.
  Concept: object storage and background jobs.
- Symptom: sending notifications blocks user actions.
  Concept: queues and workers.
- Symptom: comment pages get huge.
  Concept: pagination, keyset pagination, data modeling.
- Symptom: feed ranking is naive.
  Concept: scoring algorithms and time decay.
- Symptom: one database becomes overloaded.
  Concept: connection pools, read replicas, partitioning, eventual sharding.
- Symptom: abuse and spam grow.
  Concept: rate limits, moderation queues, trust systems.
- Symptom: deployment failures become expensive.
  Concept: observability, metrics, logs, rollbacks, incident response.

## Long-Term 90-Day Phases

### Phase 2: Communities and Better Posting

Goal:

- Subreddit-like communities.
- Community pages.
- Moderators.
- Basic rules.
- Post types: text and links.

CS concepts:

- Authorization
- Relational modeling
- Slugs
- Uniqueness
- Server-side validation

### Phase 3: Comments Become Real

Goal:

- Threaded comments.
- Comment voting.
- Collapsing comment trees.
- Deleted comments.

CS concepts:

- Trees
- Recursion
- Recursive queries or materialized paths
- Tradeoffs in data modeling

### Phase 4: Moderation and Safety

Goal:

- Remove posts and comments.
- Ban users from communities.
- Report content.
- Mod queue.

CS concepts:

- State machines
- Audit logs
- Role-based access control
- Admin tooling

### Phase 5: Search and Discovery

Goal:

- Search posts and communities.
- Explore page.
- Better community recommendations.

CS concepts:

- Full-text search
- Indexes
- Ranking
- Precision and recall

### Phase 6: Media, Uploads, and Storage

Goal:

- Image posts.
- Link previews.
- User avatars.
- Safer upload handling.

CS concepts:

- Object storage
- File metadata
- MIME types
- CDN basics
- Background processing

### Phase 7: Notifications and Background Work

Goal:

- Notifications for replies.
- Email notifications.
- Background workers.
- Retry failed jobs.

CS concepts:

- Queues
- Idempotency
- Retries
- Dead-letter queues
- Event-driven systems

### Phase 8: Caching and Performance

Goal:

- Cache hot feeds.
- Cache community metadata.
- Add rate limits.
- Measure slow endpoints.

CS concepts:

- Redis or Valkey
- Cache invalidation
- TTLs
- Connection pooling
- Load testing

### Phase 9: Feed Ranking and Personalization

Goal:

- Hot ranking.
- Best sorting.
- Subscribed feed.
- Basic recommendation signals.

CS concepts:

- Ranking algorithms
- Time decay
- Batch jobs
- Materialized views
- Tradeoffs between freshness and cost

### Phase 10: Reliability and Operations

Goal:

- Production logs.
- Metrics.
- Traces.
- Error tracking.
- Alerts.
- Backups.
- Rollbacks.
- Incident drills.
- A hosted tool like Datadog or an open-source telemetry stack when the app outgrows local terminal logs.

CS concepts:

- Observability
- OpenTelemetry
- SLOs
- Error budgets
- Backups and restores
- Deployment safety

### Phase 11: Scaling Toward Millions

Goal:

- Read replicas.
- Partition large tables.
- Separate services where justified.
- Shard only after simpler options are exhausted.

CS concepts:

- Distributed systems
- Replication lag
- Consistency
- CAP tradeoffs
- Data partitioning
- Service boundaries

## Stack Recommendation

Use this stack for the course:

- Frontend: React with Vite, plain JavaScript.
- Backend: Go.
- Database: PostgreSQL.
- Later cache: Redis or Valkey.
- Later background jobs: Go workers with a queue.
- Later search: PostgreSQL full-text search first, dedicated search later only if needed.
- Later media: object storage and CDN.

Why this stack:

- JavaScript keeps the frontend approachable.
- React/Vite is common, fast to start, and easy for Codex to modify.
- Go gives a clean backend path without too much framework magic.
- PostgreSQL teaches real relational data modeling from the beginning.
- Redis, queues, search infrastructure, and distributed systems are introduced when there is a clear symptom.

## Site Direction: Homepage, Beginner Roadmap, and Reddit Track

The parent `../index.html` is currently a compact landing page for the AI Builder Roadmap. It explains the beginner path, repeats several roadmap benefits, and sends people to `/start/`. That worked when the site had one main artifact. Once the Reddit course exists, the root homepage should become a simpler decision page for two different visitors:

- Visitor A: "I am starting from zero."
- Visitor B: "I know the basics and want to build the Reddit-like project."

The homepage should not try to teach everything. Its job should be to orient the visitor and send them to the right starting point.

### Visual Thesis

Keep the current dark, technical, trustworthy mood, but make the composition less document-like and more like a focused product landing page. Use one strong idea: "from first localhost page to a Reddit-scale system, one working step at a time." Avoid adding more glass-card grids. Use fewer sections, stronger hierarchy, and one clear path selector.

### Content Plan for `../index.html`

Recommended homepage structure:

1. Hero: brand, promise, and two CTAs.
2. Path chooser: two clear routes based on the visitor's current skill level.
3. Course arc: a compact visual timeline from beginner basics to Reddit MVP to scaling phases.
4. Why the course is different: prompt, run, paste errors, repeat.
5. Coaching/contact: quiet secondary section.

Hero direction:

- Brand: `AI Builder Roadmap`
- Headline idea: `Learn the basics, then build a Reddit-like app one small prompt at a time.`
- Supporting copy: one short sentence explaining that the site starts with beginner setup and grows into a long-form project that teaches real CS concepts through a modern AI coding workflow.
- Primary CTA: `Start From Zero` linking to `/start/`.
- Secondary CTA: `Jump to Reddit Phase 1` linking to `/start/#build-reddit-slowly` at first, and later to a dedicated `/reddit/` or `/build-reddit/` page.

Path chooser copy:

- `I am new to coding`
  - Destination: `/start/`
  - Promise: learn ChatGPT, Codex, terminal, Git, HTML, CSS, JavaScript, and localhost first.
- `I know the basics`
  - Destination: `/start/#build-reddit-slowly` now, dedicated Reddit course later.
  - Promise: start the first 90-day phase with React, Vite, Go, PostgreSQL, seeded posts, and debugging habits.

The root page should remove or compress repeated explanatory sections like the current "Why This Page Exists" and "Inside The Roadmap." Those points can become one short proof/detail section instead of multiple card-heavy blocks.

### How `./index.html` Should Change Later

The current `./index.html` should remain the detailed beginner roadmap. It is the right place for the step-by-step basics. Do not turn it into a giant Reddit course page.

Recommended role for `/start/`:

- Keep it as the "start from zero" curriculum.
- Tighten the hero so it acknowledges the larger path: basics first, then the Reddit capstone.
- Add a clear top CTA or note for experienced users: `Already know the basics? Jump to the Reddit build.`
- Add section 14 as a compact gateway to the Reddit track, not the full 33-month curriculum.
- Use `plan.md` as the source for a later dedicated Reddit course page.

Suggested `/start/` changes when HTML work begins:

- Update the hero CTA pair:
  - Primary: `Start with the first hour`
  - Secondary: `Preview the Reddit build`
- Add one sentence near the top:
  - `This roadmap starts with the basics. The capstone is a long-form Reddit-like app built slowly from a seeded PostgreSQL feed to a system that can handle serious traffic.`
- Add a short "Where to go next" block after section 13:
  - `If you are still new, keep moving through the basics.`
  - `If you already know HTML, CSS, JavaScript, Git, and localhost, start the first Reddit phase.`
- Keep the section 14 content compact enough to scan in one minute.

### Future Dedicated Reddit Course Page

Eventually create a separate page, likely `/reddit/` or `/build-reddit/`, when the Reddit course becomes too large for `/start/`.

That page should contain:

- The full first 90-day plan.
- The ten later 90-day phases.
- Prompt examples.
- Debugging examples.
- Concept explanations.
- "Run hot" scaling lessons.
- Links back to prerequisite sections in `/start/`.

The dedicated Reddit page should not be framed as a clone tutorial. It should be framed as a long-form learning project:

> Build a Reddit-like app as if it is brand new, tiny, and unproven. Start cheap and simple. Let real pressure teach you what to rewrite.

### Navigation Plan

Initial nav:

- `Start`
- `Reddit Build`
- `Coaching`
- `About`

Initial URLs:

- `/` for the two-path landing page.
- `/start/` for beginner basics.
- `/start/#build-reddit-slowly` for the compact Reddit gateway.
- Later `/reddit/` or `/build-reddit/` for the full course.

### Interaction Thesis

When frontend work begins, keep motion restrained:

- Hero content fades and rises once on page load.
- The path chooser has subtle hover/focus states that make each route feel clickable.
- The course arc can use a simple horizontal timeline on desktop and a vertical sequence on mobile.

Respect reduced-motion preferences and avoid decorative animation that distracts from the two-route decision.

## What the Future HTML Section Should Contain

The future `index.html` section should be compact enough for the existing roadmap page, then link or point to a larger course later.

Suggested content blocks:

1. A short section intro explaining the capstone.
2. A `topic-list` with:
   - logged-out feed first
   - seeded PostgreSQL data
   - prompt/run/paste errors loop
   - scale after traffic
3. A `quote-card` explaining why we do not build for Reddit scale on day one.
4. A `roadmap-card` with the first 90-day phase.
5. A second `roadmap-card` or resource block summarizing the ten later 90-day phases.
6. A prompt examples block with two or three starter prompts, not actual code.

## Suggested First Section Copy Direction

Use language like:

> The first assignment is not "build Reddit." The first assignment is "show eight seeded posts from PostgreSQL on a simple logged-out homepage." That is enough to learn the browser, the backend, the database, the terminal, and the habit that matters most: run it, read the error, paste the error back into Codex, and keep going.

## Out of Scope for the First Assignment

Be explicit about what learners should not add yet:

- Authentication
- User profiles
- Voting
- Comments
- Moderation
- Search
- Infinite scroll
- Redis or Valkey
- Queues
- Microservices
- Kubernetes
- Recommendation systems
- Mobile apps
- Real-time updates
- Ads
- Payments

This keeps the first task small enough for a novice to actually finish.
