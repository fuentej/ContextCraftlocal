# ContextCraftPro User Guide

**Complete step-by-step workflows and examples**

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Workflow: Feature Spec to Implementation](#workflow-feature-spec-to-implementation)
3. [Workflow: Multiple Features & Planning](#workflow-multiple-features--planning)
4. [Advanced Workflows](#advanced-workflows)
5. [Examples with Real Output](#examples-with-real-output)
6. [Tips & Tricks](#tips--tricks)

---

## How It Works: The Two-Layer Architecture

CCP uses a **two-layer architecture** that separates context generation from implementation:

### Layer 1: Context Generation (Local-Only)
✓ **Happens on your machine via ContextCraftPro:**
- Define features with structured specs
- Generate PRPs (Product Requirements Prompts) using Foundry Local (your machine, not cloud)
- Validate implementations against requirements
- Track context health

**Result:** A markdown file (`context/prps/*.md`) with detailed implementation requirements.

### Layer 2: Implementation (Your Choice)
✓ **Happens in your coding tool:**
You choose how to implement. Options include:
- **Claude Code** (cloud-based Claude)
- **Cursor** (IDE with AI, local or cloud model switching)
- **VS Code + Claude Extension** (local IDE, cloud Claude)
- **ChatGPT/Gemini/etc.** (your preferred chat interface)
- **Any other coding assistant**

You feed the PRP (a Markdown file) to your chosen tool. That tool does the coding—using whatever LLM and setup you configured for it.

**Key insight:** CCP is local-only for *requirements generation*. Implementation is completely tool-agnostic—use whatever coding setup works best for you.

---

## Getting Started

### Initial Setup (5 minutes)

**Prerequisites:**
- Python 3.8+ installed
- Foundry Local installed and running (see [README](../README.md#requirements))
- Your project repo with at least one git commit

**Step-by-step:**

```bash
# 1. Navigate to your project root (where .git/ lives)
cd ~/my-project

# 2. Clone ContextCraftPro into your project
git clone https://github.com/fuentej/ContextCraftlocal.git temp-ccp
cp -r temp-ccp/ContextCraftPro .
rm -rf temp-ccp

# 3. Enter the folder and install
cd ContextCraftPro
pip install -r requirements.txt

# 4. Initialize the project
python ccp.py init-project

# You'll see:
#   ✓ Scanning repository...
#   ✓ Detected: Python, pytest
#   ✓ Created context/ directory
#   ✓ Created config/contextcraft.yaml
#   ✓ Add ContextCraftPro/ to .gitignore? [y/n]
#
# Answer 'y' to add to .gitignore

# 5. Verify setup
python ccp.py health

# Expected output:
#   ✓ Foundry Local is accessible
#   📊 Context Health Report
#   ========================
#   ✓ 0 features defined
```

You're ready! The `context/` directory now contains:
- `claude.md` — coding rules for AI assistants
- `INITIAL.md` — where your feature specs go
- `project-profile.yaml` — auto-detected repo info

---

## Workflow: Feature Spec to Implementation

**Time: 30 minutes for a typical feature**

This is the core workflow: define → generate → implement → validate.

### Phase 1: Define a Feature (5 min)

```bash
python ccp.py new-feature
```

The tool asks interactive questions:

```
📝 New Feature
==============

What's the name of this feature?
> user-authentication

What are you building? (1-2 sentences)
> A login system that authenticates users via email and password.
> Supports password reset flow and optional 2FA.

Why does this matter to users? (user value)
> Users need a secure way to access their accounts. This prevents
> unauthorized access and provides a smooth onboarding experience.

What's in scope? (include/exclude)
> IN: Login form, password validation, session management
> OUT: Third-party OAuth, social login (future)

Which modules/code areas will be affected?
> auth/, models/, routes/auth.py, middlewares/

Any known gotchas or technical constraints?
> Database: PostgreSQL with bcrypt hashing required.
> Must support concurrent logins.
> Password requirements: 8+ chars, mix of numbers and symbols.

LLM Refinement
==============
🤖 Refining your answers with LLM...
✓ Generated structured spec

Review the spec below:
---
## user-authentication

### Description
A login system that authenticates users via email and password...
[etc.]
---

Save to context/INITIAL.md? [y/n]
> y

✓ Feature saved to context/INITIAL.md
```

**What was created:**
- Feature section appended to `context/INITIAL.md`
- Includes all your answers + LLM refinement
- You can edit it anytime (it's just Markdown)

### Phase 2: Generate the PRP (5 min)

Now generate a Product Requirements Prompt that guides implementation:

```bash
python ccp.py generate-prp --feature user-authentication
```

The tool:
1. Reads your feature spec
2. Gathers context (coding rules, examples, docs)
3. Calls LLM to create a comprehensive PRP
4. Shows it for review
5. Saves to `context/prps/user-authentication.md`

**What you see:**

```
🚀 Generating PRP for 'user-authentication'
============================================

1️⃣  Loading context...
   ✓ Feature spec from INITIAL.md
   ✓ Coding rules from claude.md
   ✓ Project profile loaded

2️⃣  Calling Foundry Local...
   ⏳ Generating (may take 30 seconds)...

3️⃣  Validating PRP structure...
   ✓ Context & Assumptions ✓
   ✓ Goals and Non-Goals ✓
   ✓ Ordered Implementation Steps ✓
   ✓ Implementation Checklist ✓
   ✓ Validation Plan ✓

4️⃣  Review PRP:
---
# Product Requirements Prompt: User Authentication

## Context & Assumptions
- Current codebase uses FastAPI with PostgreSQL
- Passwords are stored with bcrypt hashing
- Sessions use JWT tokens stored in httponly cookies
[...]

## Goals and Non-Goals
**Goals:**
- User can log in with email and password
- Passwords are securely hashed and validated
- Sessions persist across requests
- Failed logins are rate-limited
- Logout clears session

**Non-Goals:**
- OAuth/social login (future feature)
- 2FA (future enhancement)
- LDAP integration
[...]

## Ordered Implementation Steps
1. Create User model (id, email, password_hash, created_at)
2. Add authentication middleware (validates JWT)
3. Create POST /auth/login endpoint
   - Accept email, password
   - Hash password, compare with stored hash
   - Generate JWT on success
   - Return JWT in httponly cookie
[...]

## Implementation Checklist
- [ ] User model has email_unique constraint
- [ ] Password hashing uses bcrypt with salt
- [ ] Login endpoint validates both email and password
- [ ] Failed login attempts return 401 (not "user not found")
- [ ] JWT includes user_id and expires in 24 hours
- [ ] Sessions are rate-limited (max 5 failed attempts)
- [ ] All endpoints tested with pytest
- [ ] Password reset flow documented
[...]

## Validation Plan
1. Run tests: pytest tests/auth/
2. Manual test: POST /auth/login with valid credentials
3. Verify JWT is set in httponly cookie
4. Test failed login (wrong password, non-existent user)
5. Verify rate limiting works
6. Test session expiration after 24 hours
---

Continue? [y/n]
> y

✓ PRP saved to context/prps/user-authentication.md
```

### Phase 3: Implement Using Your Coding Assistant (10 min)

CCP generates the requirements; now use your chosen coding tool to implement. The PRP is tool-agnostic.

#### Option A: Claude Code (Cloud-based)

```bash
# CLI approach
claude-code --instructions "$(cat context/prps/user-authentication.md)"

# Or copy the PRP manually
cat context/prps/user-authentication.md
# Then paste into claude.ai/code web interface
```

#### Option B: Cursor (IDE with AI)

1. Open your project in Cursor
2. Right-click `context/prps/user-authentication.md` → Open
3. Select all and use Cursor's AI chat to implement
4. Cursor executes changes directly in your editor

#### Option C: VS Code + Claude Extension

1. Open `context/prps/user-authentication.md` in VS Code
2. In the Claude panel, paste the PRP content
3. Ask: "Implement this PRP"
4. Claude suggests changes; you apply them

#### Option D: Any Other Tool (ChatGPT, Gemini, etc.)

```bash
# Copy the PRP
cat context/prps/user-authentication.md

# Paste into your tool's chat interface and ask:
# "Please implement this product requirements prompt. Follow each step
#  in order and verify against the checklist."
```

**All approaches will result in:**
- User model with email and password hash
- Authentication middleware validating JWT
- Login/logout endpoints
- Tests covering all scenarios
- Following your project's code style (from `context/claude.md`)

### Phase 4: Validate the Implementation (5 min)

After Claude (or you) implements the feature:

```bash
python ccp.py validate --feature user-authentication
```

The tool:
1. Runs your tests (pytest by default)
2. Asks: Did it work? What's missing? What's good?
3. Calls LLM to analyze validation results
4. Saves report to `context/validation/user-authentication.md`

**Interactive flow:**

```
✓ Running tests: pytest tests/auth/
  PASSED 8 tests in 2.3 seconds

🔍 Validation Feedback
======================

Did the implementation match the PRP requirements?
  Options: full, partial, failed
> full

What went well? (optional)
> Great! All tests pass. The implementation is clean and follows
> the code style from claude.md. JWT handling is solid.

What didn't work or needs improvement? (optional)
> Nothing major. Minor: could add more detailed error messages
> for failed login attempts (still secure, just more helpful).

What patterns from this feature should we promote? (optional)
> The middleware pattern for JWT validation is reusable. Consider
> documenting this as a pattern in claude.md.

LLM Analysis
============
🤖 Analyzing validation results...

Generated report:
---
# Validation Report: user-authentication

## Implementation Status
✓ FULLY IMPLEMENTED
All PRP requirements met. Tests pass. Code quality is high.

## What Worked Well
- JWT middleware pattern is clean and reusable
- Password hashing properly uses bcrypt
- Tests are comprehensive (100% coverage of auth endpoints)
- Error handling is appropriate (no info leaks on failed login)

## What Could Improve
- Add more descriptive error messages in response (still secure)
- Document the middleware pattern in claude.md for reuse

## Recommendations
1. Update claude.md to include JWT middleware pattern
2. Extract middleware to shared module for other features
3. Consider extracting authentication to a separate service (future)

## Quality Score: 9/10
Implementation exceeds requirements. Production-ready.
---

Save report? [y/n]
> y

✓ Validation saved to context/validation/user-authentication.md
```

---

## Workflow: Multiple Features & Planning

**Time: 60 minutes for planning 5 features**

When you have multiple features to track:

### Step 1: Define All Features

```bash
# Define each feature one by one
python ccp.py new-feature  # feature 1: user-authentication
python ccp.py new-feature  # feature 2: admin-dashboard
python ccp.py new-feature  # feature 3: api-rate-limiting
python ccp.py new-feature  # feature 4: email-notifications
python ccp.py new-feature  # feature 5: audit-logging
```

Each appends to `context/INITIAL.md`.

### Step 2: Check Context Health

See where you stand:

```bash
python ccp.py health
```

**Output:**

```
📊 Context Health Report
========================

✓ 5 features defined
  ✗ 0 with PRPs (0%)
  ✗ 0 validated (0%)
  ⚠ All new (defined today)

Stale Artifacts: None

Issues Found:
  ⚠ No PRPs generated yet
  ⚠ No validations recorded yet

Recommendations:
  1. Generate PRPs for all 5 features
  2. Prioritize by complexity/dependencies
  3. Validate after each implementation
```

### Step 3: Generate PRPs Strategically

Prioritize features by dependencies:

```bash
# Foundation first (others depend on this)
python ccp.py generate-prp --feature user-authentication

# Then core features
python ccp.py generate-prp --feature admin-dashboard
python ccp.py generate-prp --feature api-rate-limiting

# Then enhancements
python ccp.py generate-prp --feature email-notifications
python ccp.py generate-prp --feature audit-logging
```

### Step 4: Monitor Progress

```bash
# After each implementation & validation
python ccp.py health --generate-report
```

This generates `context/health-report.md` showing:
- Completion percentage
- Which features are missing PRPs
- Which features aren't validated
- Recommendations

Perfect for sprint planning!

---

## Advanced Workflows

### Workflow A: Iterative Refinement

If the first PRP isn't quite right:

```bash
# Option 1: Edit INITIAL.md and regenerate
nano context/INITIAL.md  # Make edits to spec
python ccp.py generate-prp --feature my-feature

# Option 2: Edit the PRP directly
nano context/prps/my-feature.md  # Adjust requirements
# Then implement with edited PRP

# Option 3: Start over
rm context/INITIAL.md  # Delete feature spec
rm context/prps/my-feature.md  # Delete PRP
python ccp.py new-feature  # Start fresh
```

### Workflow B: Switching Between Models

Foundry Local runs one model at a time. To use different models:

```bash
# Terminal 1: Start a model
foundry model run qwen2.5-0.5b

# Terminal 2: Set CCP to use this model
export CCP_FOUNDRY_LOCAL_MODEL="qwen2.5-0.5b"

# Verify the config is correct
python ccp.py config

# Now use CCP
python ccp.py new-feature

# When you want a different model:
# Terminal 1: Stop current model (Ctrl+C)
# Terminal 1: Start a different model
foundry model run gpt-4-turbo

# Terminal 2: Update CCP to match
export CCP_FOUNDRY_LOCAL_MODEL="gpt-4-turbo"
python ccp.py generate-prp --feature complex-feature

# Then switch back if needed
# Terminal 1: (Ctrl+C) and restart
foundry model run qwen2.5-0.5b

# Terminal 2:
export CCP_FOUNDRY_LOCAL_MODEL="qwen2.5-0.5b"
python ccp.py validate --feature complex-feature
```

**Note:**
- Only one Foundry Local model runs at a time
- When you switch the model in Terminal 1, update the `CCP_FOUNDRY_LOCAL_MODEL` in Terminal 2 to match
- Alternatively, edit `config/contextcraft.yaml` and update the `model:` field

---

## Examples with Real Output

### Example 1: Simple Feature (5 minutes)

**Scenario:** Add a dark mode toggle to the UI

```bash
$ python ccp.py new-feature
? What's the name of this feature?
> dark-mode-toggle

? What are you building?
> A toggle in settings that switches between light and dark themes.
> Preference is saved to local storage.

? Why does this matter?
> Users want dark mode for reduced eye strain in low light.
> Improves user satisfaction and accessibility.

? What's in scope?
> IN: UI toggle, CSS themes, local storage persistence
> OUT: System preference detection (future)

? Which modules affected?
> ui/, styles/, settings/

? Any gotchas?
> CSS variables for theme switching. Need to update all color
> definitions. May need JavaScript to prevent flash on reload.

[LLM refinement...]

✓ Saved to context/INITIAL.md
```

**Generated INITIAL.md section:**

```markdown
## dark-mode-toggle

### Description
A theme toggle allowing users to switch between light and dark modes.
User preference persists across sessions via local storage.

### User Value
Reduces eye strain in low-light environments. Improves accessibility
and user satisfaction.

### Scope
**Included:**
- UI toggle in settings menu
- CSS theme switching via variables
- Local storage persistence
- Smooth transition between themes

**Excluded:**
- Automatic system preference detection
- Server-side theme preference
- Custom theme builder (future)

### Key Requirements
- Toggle button accessible from settings
- Persistent across page reloads
- No flash of wrong theme on page load
- All UI elements themed (buttons, inputs, etc.)
- Smooth CSS transitions

### Technical Considerations
- Use CSS custom properties (variables) for colors
- Store preference in localStorage
- Load preference before rendering (prevent flash)
- Ensure sufficient contrast in both themes (WCAG AA)
```

**Generate PRP:**

```bash
$ python ccp.py generate-prp --feature dark-mode-toggle
[...generates PRP...]

Key sections from generated PRP:
- Store theme preference in localStorage on change
- Load theme preference on app initialization
- Apply 'dark' class to root element
- CSS variables automatically switch colors
- Test in dark/light mode, verify no flash
```

**Validation:**

```bash
$ python ccp.py validate --feature dark-mode-toggle
✓ All tests pass
? Did implementation match? > full
? What went well? > Perfect! Clean CSS variable usage.
? Anything to improve? > Consider adding system preference detection later.

✓ Saved validation report
```

---

### Example 2: Complex Feature (15 minutes)

**Scenario:** Payment processing with Stripe

```bash
$ python ccp.py new-feature
? Feature name?
> stripe-payment-integration

? What are you building?
> Integration with Stripe for processing payments. Users select
> subscription tier, enter card details, and receive confirmation.
> Support one-time and recurring payments.

? Why matters?
> Users need way to purchase premium features. Business requires
> recurring revenue model.

? In scope?
> IN: Subscription tiers, card processing, webhook validation
> OUT: Fraud detection, dunning emails, invoice management

? Modules affected?
> payments/, models/subscription.py, routes/billing.py,
> webhooks/stripe.py, tests/payments/

? Gotchas?
> Stripe API key management. Webhook signature verification.
> Idempotent processing of webhook events. PCI compliance.
> Test mode vs live mode. Currency handling.

[LLM refinement...]

✓ Feature spec created with all details
```

**Generated PRP will include:**

```markdown
## Ordered Implementation Steps

1. Set up Stripe account and get API keys
   - Store in environment variables
   - Never commit keys to repo

2. Create Subscription model
   - Fields: user, tier, stripe_id, status, created_at, expires_at
   - Relationships: User has many subscriptions

3. Add Payment endpoint POST /api/payments/subscribe
   - Input: tier_id, stripeToken
   - Create Stripe customer if needed
   - Create subscription in Stripe
   - Store subscription in database
   - Return success/error

4. Implement webhook handler POST /api/webhooks/stripe
   - Verify webhook signature
   - Handle events: customer.subscription.created, .updated, .deleted
   - Update subscription status in database
   - Log all events

5. Add user dashboard showing current subscription
   - Display tier, next billing date, cancel button

6. Write comprehensive tests
   - Mock Stripe API responses
   - Test success path
   - Test error handling
   - Test webhook signature verification
   - Test idempotency

7. Document:
   - API key setup
   - Testing with Stripe test mode
   - Production deployment checklist
```

**With validation:**

```bash
$ python ccp.py validate --feature stripe-payment-integration
✓ All tests pass (18 tests, 100% coverage)

? Implementation quality?
> ~85% (works but webhook retry logic needs improvement)

? Issues?
> Webhook processing doesn't handle retries well. If database save fails
> after Stripe confirms payment, webhook is lost.

✓ Generated validation report with:
  - Clear statement of what works
  - Specific issues to fix
  - Recommendations for improvement
  - Patterns to promote (webhook handling)
```

---

## Tips & Tricks

### 💡 Tip 1: Use Dry-Run to Preview

Always preview before writing:

```bash
# Preview new feature without saving
python ccp.py new-feature --dry-run

# Preview export without copying
python ccp.py export --target docs --dry-run

# Preview PRP without confirming
python ccp.py generate-prp --feature x --dry-run
```

### 💡 Tip 2: Iterate on claude.md

Your `context/claude.md` improves over time:

```bash
# Initial version (auto-generated)
cat context/claude.md

# After first few features, add:
# - Patterns that worked well
# - Common gotchas
# - Project-specific conventions

# Then regenerate PRPs with improved context
python ccp.py generate-prp --feature next-feature
```

This makes each PRP better!

### 💡 Tip 3: Share Validation Insights

After validation, update claude.md with learnings:

```bash
# From validation report, see patterns worth promoting
# Edit claude.md to add:

## Tested Patterns
- JWT middleware (user-authentication feature)
- CSS variables for theming (dark-mode-toggle)

## Common Mistakes
- Don't store API keys in config, use env vars
- Always verify webhook signatures
```

### 💡 Tip 4: Generate Reports for Planning

Weekly health checks help plan sprints:

```bash
# Every Monday
python ccp.py health --generate-report
# Review context/health-report.md
# Update backlog based on health metrics
```

### 💡 Tip 5: Export for Stakeholders

Share PRPs without giving access to ContextCraftPro:

```bash
# Export everything
python ccp.py export --target all

# Stakeholders can see:
# - What's planned (specs)
# - Implementation requirements (PRPs)
# - What's validated (validation reports)
```

### 💡 Tip 6: Version Your Context

Track changes over time:

```bash
# Before major work
git add ContextCraftPro/context/
git commit -m "Phase 1: Initial feature specs

- user-authentication
- admin-dashboard
- payment-processing"

# After PRPs generated
git commit -m "Phase 2: PRPs generated

- User auth PRP complete
- Admin dashboard PRP complete
- etc"

# After validation
git commit -m "Phase 3: Validation complete

- User auth validated (production ready)
- Admin dashboard validated (minor issues)
- etc"
```

### 💡 Tip 7: Use Environment Variables for Automation

Automate CI/CD integration:

```bash
# In CI/CD pipeline
export CCP_FOUNDRY_LOCAL_ENDPOINT="http://llm-service:8000/v1"
export CCP_CONFIRM_EXPORTS=false
export CCP_VERBOSE=true

python ccp.py health --generate-report
# Upload report to CI artifacts
```

### 💡 Tip 8: Learn from Generated PRPs

Don't just execute them—study them:

```bash
# After generating PRP
cat context/prps/my-feature.md

# Notice:
# - How LLM structured the requirements
# - Implementation patterns suggested
# - What assumptions were made
# - How to write better future specs

# Next spec, incorporate those learnings
```

---

## Troubleshooting Common Issues

### Issue: "I defined a feature but can't generate PRP"

```bash
# Check if feature is in INITIAL.md
grep -A 5 "## my-feature" context/INITIAL.md

# If not there, create it
python ccp.py new-feature --feature-name my-feature

# Feature name must match exactly (case-sensitive)
python ccp.py generate-prp --feature my-feature
```

### Issue: "LLM response didn't match my intent"

```bash
# Edit INITIAL.md to clarify
nano context/INITIAL.md
# Make spec clearer, more specific

# Also improve claude.md to guide LLM better
nano context/claude.md

# Regenerate PRP
python ccp.py generate-prp --feature my-feature
```

### Issue: "Export didn't work as expected"

```bash
# Preview first
python ccp.py export --target docs --dry-run

# Check that source files exist
ls -la context/prps/
ls -la context/validation/

# Try exporting to different target
python ccp.py export --target all
# Full bundle might work better
```

---

## Next Steps

- Read the main [README.md](README.md) for command reference
- Check [docs/llm-architecture.md](docs/llm-architecture.md) for technical details
- Review `context/claude.md` to understand your project's coding conventions
- Start with small features to get comfortable with the workflow

**Happy context engineering!** 🚀
