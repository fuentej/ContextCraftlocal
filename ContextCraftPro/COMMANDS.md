# ContextCraftPro Command Reference

**Complete documentation for every command**

---

## Quick Command Map

| Command | Purpose | Time | When to Use |
|---------|---------|------|-----------|
| `init-project` | First-time setup | 2 min | Once per repo |
| `new-feature` | Define a feature | 5 min | For each feature |
| `generate-prp` | Create implementation prompt | 2 min | Before implementing |
| `validate` | Record implementation results | 5 min | After each feature |
| `health` | Check context status | 1 min | Weekly |
| `export` | Share artifacts | 3 min | Before committing |

---

## `init-project`

**Purpose:** One-time initialization of ContextCraftPro for your repository.

### Synopsis

```bash
python ccp.py init-project [OPTIONS]
```

### Description

Sets up ContextCraftPro by:
1. Scanning your repository for languages, frameworks, and test commands
2. Creating configuration file (`config/contextcraft.yaml`)
3. Generating default coding rules (`context/claude.md`)
4. Creating feature specification template (`context/INITIAL.md`)
5. Optionally updating `.gitignore` to exclude ContextCraftPro/

**Note:** This command is idempotent—safe to re-run multiple times.

### Options

#### `--dry-run`
Shows what would be created without actually writing files.

```bash
python ccp.py init-project --dry-run
```

Output:
```
🏗️  Init-Project (DRY RUN)
=========================

Would create:
  ✓ config/contextcraft.yaml
  ✓ context/claude.md
  ✓ context/INITIAL.md
  ✓ context/project-profile.yaml

Would scan:
  ✓ Repository structure
  ✓ Language detection
  ✓ Framework detection
  ✓ Test commands

Note: Run without --dry-run to actually create files.
```

#### `--verbose`
Enables extra logging output to stdout. Useful for debugging.

```bash
python ccp.py init-project --verbose
```

Shows:
- Detailed scanning progress
- Files created with timestamps
- Configuration values used

### Examples

**Basic usage:**
```bash
python ccp.py init-project
```

**Re-initialize (safe):**
```bash
# Preserves existing context files
python ccp.py init-project
# ✓ Config already exists, skipping
# ✓ Claude rules already exist, keeping
# ✓ Updating project profile only
```

**Check what would change:**
```bash
python ccp.py init-project --dry-run --verbose
```

### Output Files Created

| File | Purpose | Editable? |
|------|---------|-----------|
| `config/contextcraft.yaml` | Configuration (endpoint, model, paths) | Yes |
| `context/claude.md` | Coding rules for AI assistants | Yes |
| `context/INITIAL.md` | Feature specifications | Yes |
| `context/project-profile.yaml` | Auto-detected repo info | Usually no |
| `runtime/logs/ccp.log` | Operation logs | No (append-only) |

### Configuration Created

```yaml
# config/contextcraft.yaml
foundry_local:
  endpoint: "http://127.0.0.1:PORT/v1/chat/completions"
  model: "gpt-4o-mini"
  timeout: 30
  max_retries: 3

paths:
  project_root: ".."
  context_root: "context"
  claude_rules: "context/claude.md"
  initial_spec: "context/INITIAL.md"
  # ... more paths

behavior:
  auto_open_browser: false
  confirm_exports: true
  enable_refinement: true
  require_confirmation: true
```

### Environment Variable Overrides

Variables set before `init-project` affect defaults:

```bash
export CCP_FOUNDRY_LOCAL_ENDPOINT="http://127.0.0.1:PORT/v1"
export CCP_FOUNDRY_LOCAL_MODEL="llama2"
python ccp.py init-project
# Uses custom endpoint and model
```

### Troubleshooting

**Problem:** "Error: Cannot write to context/"
```bash
# Solution: Check directory permissions
chmod -R u+w ContextCraftPro/
python ccp.py init-project
```

**Problem:** "Error: .gitignore already has ContextCraftPro/"
```bash
# Solution: Just confirm, no issue
python ccp.py init-project
# It will skip the .gitignore entry
```

---

## `new-feature`

**Purpose:** Create a structured feature specification through interactive Q&A.

### Synopsis

```bash
python ccp.py new-feature [OPTIONS]
```

### Description

Guides you through defining a new feature:
1. Interactive questions about the feature
2. Optional LLM refinement of your answers
3. Appends structured spec to `context/INITIAL.md`

The feature spec includes:
- Name and description
- User value proposition
- Scope (in/out)
- Related code areas
- Technical constraints

### Options

#### `--feature-name TEXT`
Pre-fill the feature name (skips the first prompt).

```bash
python ccp.py new-feature --feature-name user-authentication
```

You'll still answer all other questions.

#### `--no-llm`
Skip LLM refinement, use template format directly.

```bash
python ccp.py new-feature --no-llm
```

Useful for offline work or to save LLM calls.

#### `--dry-run`
Show the generated spec without saving it.

```bash
python ccp.py new-feature --dry-run
```

Output:
```
Generated spec (would be saved to INITIAL.md):
---
## my-feature
### Description
...
---

Run without --dry-run to save.
```

#### `--verbose`
Extra logging about LLM calls and processing.

```bash
python ccp.py new-feature --verbose
```

### Interactive Questions

The tool asks in this order:

**1. Feature name**
```
What's the name of this feature?
```
Used as the heading in INITIAL.md. Can be:
- slug format: `user-authentication`
- spaces: `User Authentication`
- descriptive: `JWT-based Login System`

**2. What you're building**
```
What are you building? (1-2 sentences)
```
Describe the feature's functionality. Example:
```
A login system that authenticates users via email and password.
Supports password reset and rate limiting on failed attempts.
```

**3. User value**
```
Why does this matter to users?
```
What problem does it solve? Why should they care? Example:
```
Users need secure access to their accounts. This prevents unauthorized
access and provides smooth, reliable authentication.
```

**4. Scope**
```
What's in scope? (include/exclude)
```
Be explicit about boundaries. Example:
```
IN: Login form, password validation, session management, logout
OUT: OAuth, social login (future), 2FA
```

**5. Related code areas**
```
Which modules/code areas will be affected?
```
Where will changes be made? Example:
```
auth/, models/user.py, routes/auth.py, middleware/, tests/auth/
```

**6. Technical constraints**
```
Any known gotchas or technical constraints?
```
Document important details. Example:
```
Must use bcrypt for password hashing. Support concurrent logins.
Passwords require: 8+ chars, mix of numbers, special characters.
```

### Output Format

Features are appended to `context/INITIAL.md`:

```markdown
## user-authentication

### Description
A login system that authenticates users via email and password...

### User Value
Users need secure access to their accounts...

### Scope
**Included:**
- Login form
- Password validation
- Session management

**Excluded:**
- OAuth/social login (future)
- 2FA (future)

### Key Requirements
- Secure password hashing with bcrypt
- Support concurrent login sessions
- Rate limiting on failed attempts

### Technical Considerations
- PostgreSQL database required
- Password requirements: 8+ chars, numbers, symbols
- JWT token expiration: 24 hours
```

### Examples

**Simple feature, offline mode:**
```bash
python ccp.py new-feature --feature-name "dark-mode-toggle" --no-llm
# Interactive Q&A, no LLM refinement
```

**Complex feature with LLM refinement:**
```bash
python ccp.py new-feature
# Full interactive Q&A with LLM enhancement
```

**Preview before saving:**
```bash
python ccp.py new-feature --dry-run
# Review output, then run without --dry-run
```

### Tips

- **Be specific:** "Login system" is vague. "JWT-based email/password authentication" is clear.
- **Document constraints:** Mention database, security, concurrency issues upfront.
- **Update claude.md:** After validating, add successful patterns to `context/claude.md`

---

## `generate-prp`

**Purpose:** Generate a Product Requirements Prompt (PRP) for implementing a feature.

### Synopsis

```bash
python ccp.py generate-prp --feature FEATURE_SLUG [OPTIONS]
```

### Description

Generates a comprehensive implementation guide:
1. Reads feature spec from `context/INITIAL.md`
2. Gathers context (coding rules, examples, docs)
3. Calls Foundry Local LLM to generate PRP
4. Validates PRP structure
5. Shows for review
6. Saves to `context/prps/<feature-slug>.md`

The generated PRP includes:
- **Context & Assumptions** — current codebase state
- **Goals and Non-Goals** — what to build and what to avoid
- **Ordered Implementation Steps** — step-by-step instructions
- **Implementation Checklist** — verification points
- **Validation Plan** — how to test

### Options

#### `--feature FEATURE_SLUG` (Required)
The feature name from INITIAL.md (must match exactly, case-sensitive).

```bash
python ccp.py generate-prp --feature user-authentication
```

The feature name is the heading in INITIAL.md:
```markdown
## user-authentication  # <-- This is the FEATURE_SLUG
```

#### `--temperature FLOAT`
Controls LLM creativity (0.0–1.0, default 0.7).
- `0.0` = deterministic, repetitive
- `0.5` = balanced
- `1.0` = creative, unpredictable

```bash
# More structured, less creative
python ccp.py generate-prp --feature x --temperature 0.3

# More creative interpretations
python ccp.py generate-prp --feature x --temperature 0.9
```

#### `--max-tokens INT`
Maximum response length. Default: auto (usually 3000-4000).

```bash
# Shorter PRP (faster, less detailed)
python ccp.py generate-prp --feature x --max-tokens 2000

# Longer PRP (slower, more thorough)
python ccp.py generate-prp --feature x --max-tokens 6000
```

#### `--dry-run`
Generate PRP without saving it.

```bash
python ccp.py generate-prp --feature x --dry-run
# Displays PRP, doesn't save to context/prps/x.md
```

#### `--verbose`
Extra logging about context gathering and LLM calls.

```bash
python ccp.py generate-prp --feature x --verbose
```

### Output Format

Saves to `context/prps/feature-slug.md`:

```markdown
# Product Requirements Prompt: Feature Name

Generated by ContextCraftPro on 2025-11-21

## Context & Assumptions
- Current codebase uses FastAPI
- PostgreSQL database with existing User model
- Tests run with pytest
- Code follows style defined in claude.md

## Goals and Non-Goals

### Goals
- User can log in with email + password
- Password is securely hashed
- Session persists across requests
- Failed logins are rate-limited

### Non-Goals
- OAuth/social login
- 2FA
- LDAP integration

## Ordered Implementation Steps

1. Create UserAuth model if needed
   - email (unique constraint)
   - password_hash (bcrypt)
   - created_at timestamp

2. Add POST /auth/login endpoint
   - Accept: email, password
   - Return: JWT token on success
   - Return: 401 on failure

3. Add authentication middleware
   - Validates JWT in Authorization header
   - Adds user_id to request context

4. Implement password validation
   - Check email exists
   - Hash password, compare
   - Rate limit failed attempts

5. Add tests for all endpoints
   - Valid login
   - Wrong password
   - Non-existent user
   - Rate limiting

## Implementation Checklist
- [ ] UserAuth model created with proper constraints
- [ ] Password hashing uses bcrypt with salt
- [ ] Login endpoint validates both email and password
- [ ] JWT includes user_id and 24-hour expiration
- [ ] Failed logins return 401 (not "user not found")
- [ ] Rate limiting implemented (max 5 attempts/hour)
- [ ] All tests pass with pytest
- [ ] Code follows style guide from claude.md

## Validation Plan

1. Run tests: `pytest tests/auth/`
2. Manual test: POST /auth/login with valid credentials
3. Verify JWT is returned in response
4. Test with wrong password (should get 401)
5. Test rate limiting (5+ failed attempts)
6. Verify session works for subsequent requests
7. Logout clears session
```

### Requirements for Generate-PRP

Feature must exist in `context/INITIAL.md`:

```markdown
## feature-slug
### Description
...
```

If feature doesn't exist:
```bash
# Error message
Could not extract feature 'feature-slug' from INITIAL.md

# Create the feature first
python ccp.py new-feature --feature-name feature-slug

# Then generate PRP
python ccp.py generate-prp --feature feature-slug
```

### Examples

**Basic PRP generation:**
```bash
python ccp.py generate-prp --feature user-auth
```

**Generate multiple PRPs:**
```bash
python ccp.py generate-prp --feature user-auth
python ccp.py generate-prp --feature admin-dashboard
python ccp.py generate-prp --feature api-rate-limiting
```

**Preview before saving:**
```bash
python ccp.py generate-prp --feature x --dry-run
# Review output...
python ccp.py generate-prp --feature x  # Actually save
```

**Adjust LLM parameters:**
```bash
# More concise
python ccp.py generate-prp --feature x --max-tokens 2000 --temperature 0.5

# More thorough
python ccp.py generate-prp --feature x --max-tokens 6000 --temperature 0.7
```

### How to Use the Generated PRP

1. **Copy the PRP:**
   ```bash
   cat context/prps/feature-slug.md
   ```

2. **Use with Claude Code:**
   ```bash
   # Web interface: copy/paste the content
   # CLI: use as instruction file
   claude-code --instructions context/prps/feature-slug.md
   ```

3. **Or manually with your favorite AI:**
   - Open the .md file
   - Paste into ChatGPT, Claude, etc.
   - Ask it to implement the requirements

### Troubleshooting

**Problem:** "Request timed out"
```bash
# Solution: Use shorter PRP or increase timeout
python ccp.py generate-prp --feature x --max-tokens 2000

# Or adjust config
nano config/contextcraft.yaml
# Increase timeout: 60 (was 30)

python ccp.py generate-prp --feature x
```

**Problem:** "Invalid response from LLM"
```bash
# Solution: Try again, it might be transient
python ccp.py generate-prp --feature x

# If persists, check Foundry Local:
curl http://127.0.0.1:PORT/api/tags
```

---

## `validate`

**Purpose:** Record and analyze how well implementation matched the PRP.

### Synopsis

```bash
python ccp.py validate --feature FEATURE_SLUG [OPTIONS]
```

### Description

Captures validation results:
1. Loads original PRP
2. Optionally runs project tests
3. Asks about implementation quality
4. Calls LLM to analyze results
5. Saves validation report

Creates `context/validation/feature-slug.md` with:
- Implementation status
- What worked well
- What needs improvement
- Patterns worth promoting
- Quality score (1-10)

### Options

#### `--feature FEATURE_SLUG` (Required)
The feature to validate.

```bash
python ccp.py validate --feature user-auth
```

#### `--tests-command TEXT`
Override the test command from config.

```bash
# Use custom test command
python ccp.py validate --feature x --tests-command "pytest tests/auth/ -v"

# Different test framework
python ccp.py validate --feature x --tests-command "npm test -- auth"
```

#### `--skip-tests`
Skip test execution (manual validation only).

```bash
python ccp.py validate --feature x --skip-tests
# Asks for feedback without running tests
```

#### `--dry-run`
Generate report without saving it.

```bash
python ccp.py validate --feature x --dry-run
# Shows report, doesn't save to context/validation/x.md
```

#### `--verbose`
Extra logging about test execution and LLM analysis.

```bash
python ccp.py validate --feature x --verbose
```

### Interactive Questions

**1. Implementation quality**

```
Was the implementation successful?
  Options: full, partial, failed
```

- `full` — Meets all PRP requirements
- `partial` — Some requirements met, some issues
- `failed` — Implementation incomplete or broken

**2. What went well** (optional)

```
What went well? Any highlights?
```

Examples:
- "Clean code structure"
- "Tests are comprehensive"
- "Great error handling"

**3. What didn't work** (optional)

```
What didn't work or needs improvement?
```

Examples:
- "Forgot password reset flow"
- "Rate limiting not implemented"
- "Error messages too verbose"

**4. Patterns to promote** (optional)

```
What patterns from this implementation should we promote?
```

Examples:
- "JWT middleware pattern is reusable"
- "Error handling approach is solid"
- "Test structure could be standard"

### Output Format

Validation report at `context/validation/feature-slug.md`:

```markdown
# Validation Report: user-authentication

**Generated:** 2025-11-21 at 14:35
**Feature:** user-authentication
**Status:** FULLY IMPLEMENTED

## Test Results

```
PASSED 8 tests in 2.3 seconds
- test_login_success ✓
- test_login_invalid_email ✓
- test_login_wrong_password ✓
- test_login_rate_limiting ✓
- test_session_persistence ✓
- test_logout_clears_session ✓
- test_password_validation ✓
- test_jwt_expiration ✓
```

## Implementation Assessment

✓ **FULLY IMPLEMENTED**
All PRP requirements met. Code quality is production-ready.

## What Worked Well

- JWT middleware pattern is clean and reusable
- Password hashing properly uses bcrypt with salt
- Tests are comprehensive (100% coverage)
- Error handling is appropriate (no info leaks)
- Code style matches claude.md conventions

## Issues Found

None. Implementation is solid.

## Recommendations

1. Consider extracting middleware to shared module
2. Document JWT pattern in claude.md for reuse
3. Add integration test for full auth flow

## Quality Score: 9/10

Exceeds expectations. Production-ready code with excellent
test coverage and adherence to coding standards.

## Patterns to Promote

- JWT middleware validation pattern
- Bcrypt password hashing approach
- Error handling without information leaks
```

### Examples

**Standard validation:**
```bash
python ccp.py validate --feature user-auth
# Runs tests, asks questions, generates report
```

**Skip tests (manual only):**
```bash
python ccp.py validate --feature x --skip-tests
# Just asks about quality without running tests
```

**Custom test command:**
```bash
python ccp.py validate --feature x --tests-command "npm test"
```

**Preview report:**
```bash
python ccp.py validate --feature x --dry-run
# See report without saving
```

### How to Use Validation Results

1. **Read the report:**
   ```bash
   cat context/validation/feature-slug.md
   ```

2. **Update claude.md with successful patterns:**
   ```bash
   nano context/claude.md
   # Add patterns from "What Worked Well"
   ```

3. **Track improvements:**
   ```bash
   # Monitor quality scores over time
   grep "Quality Score" context/validation/*.md
   ```

4. **Include in sprint reviews:**
   ```bash
   # Export validation reports for stakeholders
   python ccp.py export --target all
   ```

---

## `health`

**Purpose:** Assess overall context health and completeness.

### Synopsis

```bash
python ccp.py health [OPTIONS]
```

### Description

Scans all context artifacts and reports:
- Total features defined
- Features with PRPs (completion %)
- Features with validation (completion %)
- Age of artifacts (flags stale items)
- Issues and recommendations

Perfect for:
- Sprint planning
- Identifying bottlenecks
- Monitoring progress

### Options

#### `--generate-report`
Save detailed report to `context/health-report.md`.

```bash
python ccp.py health --generate-report
```

Creates file with full analysis.

#### `--verbose`
Extra logging about scanning and analysis.

```bash
python ccp.py health --verbose
```

### Output Example

```
📊 Context Health Report
========================

✓ 5 features defined
  ✓ 3 with PRPs (60%)
  ✓ 2 validated (40%)
  ⚠ 1 stale (>30 days)

Feature Details:
  ✓ user-authentication: PRP ✓, Validated ✓, age 2 days
  ✓ admin-dashboard: PRP ✓, Validated ✗, age 5 days
  ⚠ api-rate-limiting: PRP ✗, Validated ✗, age 12 days
  ⚠ email-notifications: PRP ✓, Validated ✗, age 32 days
  ✓ audit-logging: PRP ✓, Validated ✓, age 1 day

Issues Found:
  • 2 features missing PRPs (api-rate-limiting, partially for email-notifications)
  • 3 features not validated (admin-dashboard, api-rate-limiting, email-notifications)
  • 1 artifact is stale (email-notifications, 32 days old)

Recommendations:
  1. Generate PRP for api-rate-limiting
  2. Validate admin-dashboard after implementation
  3. Review email-notifications (may need re-planning)
  4. Check if stale features are still relevant
```

### Health Report Format

When using `--generate-report`, creates `context/health-report.md`:

```markdown
# Context Health Report

**Generated:** 2025-11-21 at 14:35

## Summary

- **Total Features:** 5
- **With PRPs:** 3 (60%)
- **Validated:** 2 (40%)
- **Overall Health:** 66%

## Feature Status

| Feature | Spec | PRP | Validated | Age | Status |
|---------|------|-----|-----------|-----|--------|
| user-authentication | ✓ | ✓ | ✓ | 2d | Complete |
| admin-dashboard | ✓ | ✓ | ✗ | 5d | Implemented |
| api-rate-limiting | ✓ | ✗ | ✗ | 12d | Stalled |
| email-notifications | ✓ | ✓ | ✗ | 32d | Stale |
| audit-logging | ✓ | ✓ | ✓ | 1d | Complete |

## Issues & Risks

### Stale Artifacts
- `email-notifications` (32 days old)
  - Last updated 32 days ago
  - Implemented but not validated
  - Consider reviewing or deprioritizing

### Missing Work
- `api-rate-limiting` has no PRP yet
  - Blocked on PRP generation
  - Estimated: 2 min to generate

### Incomplete Validation
- 3 features implemented but not validated
  - `admin-dashboard` (5 days)
  - `email-notifications` (32 days)
  - `api-rate-limiting` (not yet implemented)

## Recommendations

1. **Immediate (Today)**
   - Generate PRP for `api-rate-limiting`
   - Validate `admin-dashboard`

2. **This Week**
   - Review `email-notifications` (stale, 32 days)
   - Decide: continue, replan, or archive?
   - Validate once decided

3. **Ongoing**
   - Validate within 1 week of implementation
   - Update claude.md with successful patterns
   - Keep features current (< 30 days old)

## Timeline

- Features defined: Last 2-5 days (good velocity)
- PRPs generated: Within 1-2 days of spec (good)
- Validation: Delays 5-32 days (concerning)

**Suggestion:** Prioritize validation to close the feedback loop.
```

### Examples

**Quick health check:**
```bash
python ccp.py health
# Shows status summary
```

**Detailed report:**
```bash
python ccp.py health --generate-report
# Creates context/health-report.md
# View detailed analysis
```

**Weekly check:**
```bash
# Monday morning ritual
python ccp.py health --generate-report --verbose
cat context/health-report.md
# Review and adjust sprint plan based on health
```

---

## `export`

**Purpose:** Export context artifacts to your main repository.

### Synopsis

```bash
python ccp.py export --target TARGET [OPTIONS]
```

### Description

Safely exports context artifacts:
1. Gathers selected artifacts (PRPs, validation, docs)
2. Renders into readable format
3. Copies to specified location
4. Confirms before overwriting

Export targets:
- `docs` — to `../docs/context/`
- `readme` — to `../README.context.md`
- `all` — to `../_context_exports/{timestamp}/`

### Options

#### `--target TARGET` (Required)
Where to export. One of:
- `docs` — Export to `../docs/context/` directory
- `readme` — Export to `../README.context.md` single file
- `all` — Export everything to timestamped bundle

```bash
python ccp.py export --target docs
python ccp.py export --target readme
python ccp.py export --target all
```

#### `--yes`
Skip confirmation prompts (auto-confirm).

```bash
python ccp.py export --target docs --yes
# Exports without asking for confirmation
```

Useful for CI/CD automation.

#### `--dry-run`
Show what would be exported without actually copying.

```bash
python ccp.py export --target docs --dry-run
# Lists files, shows destinations, doesn't copy
```

#### `--verbose`
Extra logging about files being exported.

```bash
python ccp.py export --target all --verbose
```

### Export Targets

#### Target: `docs`

Exports to `../docs/context/`:

```
../docs/context/
├── prps/
│   ├── user-auth.md
│   ├── admin-dashboard.md
│   └── README.md (index)
├── validation/
│   ├── user-auth.md
│   └── admin-dashboard.md
└── README.md (summary)
```

Use for: Sharing with team, keeping docs in repo.

#### Target: `readme`

Exports to `../README.context.md`:

Single-file overview with:
- Index of all features
- PRPs (full text)
- Validation results
- Status summary

Use for: Quick reference, including in main README.

#### Target: `all`

Exports to `../_context_exports/{timestamp}/`:

```
../_context_exports/2025-11-21_143500/
├── prps/
├── validation/
├── INITIAL.md
├── claude.md
├── health-report.md (if exists)
└── README.md (summary)
```

Use for: Full backup, sharing with stakeholders, archiving.

### Examples

**Export to docs:**
```bash
python ccp.py export --target docs

# Creates: ../docs/context/
#   prps/user-auth.md
#   prps/admin-dashboard.md
#   validation/user-auth.md
#   validation/admin-dashboard.md
#   README.md (index)
```

**Export single file:**
```bash
python ccp.py export --target readme

# Creates: ../README.context.md
# Includes all PRPs, validation, and status
```

**Full bundle with timestamp:**
```bash
python ccp.py export --target all

# Creates: ../_context_exports/2025-11-21_143500/
# Everything for backup/archival
```

**Automated CI/CD export:**
```bash
# In your CI/CD pipeline
python ccp.py export --target docs --yes --verbose
git add docs/context/
git commit -m "Update context artifacts"
git push
```

### Confirmation Flow

Default behavior (asks for confirmation):

```bash
$ python ccp.py export --target docs

📤 Export Context Artifacts
===========================

Target: docs/context/
Files to export:
  ✓ prps/user-auth.md
  ✓ prps/admin-dashboard.md
  ✓ validation/user-auth.md
  ✓ validation/admin-dashboard.md
  + 2 more files

Destination: ../docs/context/

⚠️  Warning: Will create/overwrite files in your main repo.
    Always review before committing!

Continue? [y/n]
> y

✓ Exported 6 files to ../docs/context/
✓ Created README.md with index
```

### Troubleshooting

**Problem:** "Target directory doesn't exist"
```bash
# Solution: Export creates directories
python ccp.py export --target docs
# Creates ../docs/context/ if needed
```

**Problem:** "Permission denied"
```bash
# Solution: Check file permissions
ls -la ../docs/
chmod u+w ../docs/

python ccp.py export --target docs
```

**Problem:** "Confirmation is slow in CI"
```bash
# Solution: Use --yes flag
python ccp.py export --target docs --yes
# No confirmation prompts
```

---

## Global Options

All commands support:

### `--help`
Shows command help.

```bash
python ccp.py --help
python ccp.py init-project --help
python ccp.py generate-prp --help
```

### `--config PATH`
Use custom configuration file.

```bash
python ccp.py health --config /path/to/config.yaml
```

Default: `config/contextcraft.yaml`

### `--verbose`
Extra logging to stdout.

```bash
python ccp.py new-feature --verbose
```

Shows:
- File operations
- LLM calls
- Detailed progress

---

## Environment Variables

Override configuration via environment:

### `CCP_FOUNDRY_LOCAL_ENDPOINT`
Foundry Local API endpoint.

```bash
export CCP_FOUNDRY_LOCAL_ENDPOINT="http://custom:8000/v1"
python ccp.py generate-prp --feature x
```

### `CCP_FOUNDRY_LOCAL_MODEL`
Model to use.

```bash
export CCP_FOUNDRY_LOCAL_MODEL="llama2"
python ccp.py generate-prp --feature x
```

### `CCP_FOUNDRY_LOCAL_TIMEOUT`
Request timeout in seconds.

```bash
export CCP_FOUNDRY_LOCAL_TIMEOUT=60
python ccp.py generate-prp --feature x
```

### `CCP_CONFIRM_EXPORTS`
Skip export confirmation.

```bash
export CCP_CONFIRM_EXPORTS=false
python ccp.py export --target docs --yes
```

---

## Exit Codes

Commands return:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (file not found, invalid config, etc.) |
| 130 | Cancelled by user (Ctrl+C) |

---

## Summary

- **`init-project`** — One-time setup
- **`new-feature`** — Define features (5 min each)
- **`generate-prp`** — Create implementation guides (2 min each)
- **`validate`** — Record results after implementation (5 min each)
- **`health`** — Check overall progress (1 min)
- **`export`** — Share artifacts (3 min)

For examples and workflows, see [USERGUIDE.md](USERGUIDE.md).
