# ContextCraftPro Documentation Index

Complete guide to all documentation for ContextCraftPro.

---

## 📚 Documentation Files

### [README.md](README.md) — **Start Here**
The main documentation file. Covers:
- Overview and key principles
- Installation & setup
- Quick start workflow
- Complete command reference
- Configuration guide
- Directory structure
- Use cases and workflows
- Best practices
- Troubleshooting
- Advanced configuration

**Best for:** Getting oriented, understanding features, solving common problems

**Read time:** 20-30 minutes

---

### [USERGUIDE.md](USERGUIDE.md) — **Step-by-Step Workflows**
Practical, hands-on guide with real examples. Covers:
- Getting started (5 min)
- Feature spec to implementation workflow (30 min)
- Multiple features & planning (60 min)
- Advanced workflows (iterative refinement, offline mode, etc.)
- Real output examples
- Tips & tricks
- Troubleshooting common issues

**Best for:** Learning by doing, seeing what output looks like, understanding workflows

**Read time:** 30-40 minutes

---

### [COMMANDS.md](COMMANDS.md) — **Command Reference**
Detailed documentation for each command. Covers:
- Quick command map
- `init-project` — setup
- `new-feature` — define features
- `generate-prp` — create implementation guides
- `validate` — record results
- `health` — check progress
- `export` — share artifacts
- Global options and environment variables

**Best for:** Understanding what each command does, all available options, specific examples

**Read time:** 40-50 minutes

---

### [docs/llm-architecture.md](docs/llm-architecture.md) — **Architecture & Technical Design**
Deep dive into LLM integration. Covers:
- Component architecture (LLM client, prompts, response processing)
- Error handling strategy
- Security considerations
- Context management
- Command-specific flows
- Testing strategy
- Configuration details
- Monitoring and logging

**Best for:** Understanding how it works internally, extending functionality, debugging

**Read time:** 30-40 minutes

---

## 🚀 Quick Navigation

### I want to...

**Get started quickly**
1. Read [README.md](README.md) — Overview section (2 min)
2. Follow Installation & Setup (5 min)
3. Read Quick Start: Feature to PRP Workflow (10 min)

**Learn by example**
→ Go to [USERGUIDE.md](USERGUIDE.md)

**Understand a specific command**
→ Go to [COMMANDS.md](COMMANDS.md)

**Plan my workflow**
1. Read [USERGUIDE.md](USERGUIDE.md) — relevant use case
2. Follow along with your own repo

**Implement a feature using PRP**
1. Read [USERGUIDE.md](USERGUIDE.md) — Workflow: Feature Spec to Implementation
2. Follow each phase step-by-step

**Share my work with others**
→ See README.md section "Best Practices" and COMMANDS.md `export` command

**Troubleshoot an issue**
1. Check [README.md](README.md) — Troubleshooting section
2. Check [USERGUIDE.md](USERGUIDE.md) — Troubleshooting section
3. Check [docs/llm-architecture.md](docs/llm-architecture.md) — Error handling details

**Understand the architecture**
→ Go to [docs/llm-architecture.md](docs/llm-architecture.md)

**Extend or modify the tool**
1. Start with [docs/llm-architecture.md](docs/llm-architecture.md)
2. Review core module documentation
3. Check test suite

---

## 📖 Reading Paths

### Path 1: New User (60 minutes)
1. README.md — Overview (5 min)
2. README.md — Installation & Setup (5 min)
3. README.md — Quick Start (10 min)
4. USERGUIDE.md — Getting Started (5 min)
5. USERGUIDE.md — Workflow: Feature Spec to Implementation (20 min)
6. Try it yourself! (10 min)

### Path 2: Complete Understanding (2 hours)
1. README.md — Full read (30 min)
2. USERGUIDE.md — Full read (40 min)
3. COMMANDS.md — Full read (30 min)
4. docs/llm-architecture.md — Skim (10 min)
5. Try workflows yourself (10 min)

### Path 3: Hands-On Learner (90 minutes)
1. README.md — Overview + Installation (10 min)
2. Run `python ccp.py init-project` (2 min)
3. USERGUIDE.md — Example 1: Simple Feature (follow along) (15 min)
4. Try `python ccp.py new-feature` (5 min)
5. Try `python ccp.py generate-prp --feature x` (5 min)
6. USERGUIDE.md — Remaining examples (read) (20 min)
7. Try more workflows (30 min)

### Path 4: Architecture Focus (60 minutes)
1. README.md — Overview only (5 min)
2. docs/llm-architecture.md — Full read (40 min)
3. Review source code: core/ccp_llm.py, core/ccp_prompts.py (15 min)

---

## 🎯 Use Case References

### "I want to define a feature"
- [README.md](README.md) — `new-feature` command section
- [USERGUIDE.md](USERGUIDE.md) — Workflow: Feature Spec to Implementation, Phase 1
- [COMMANDS.md](COMMANDS.md) — `new-feature` command reference

### "I want to generate a PRP"
- [README.md](README.md) — Quick Start section
- [USERGUIDE.md](USERGUIDE.md) — Workflow: Feature Spec to Implementation, Phase 2
- [COMMANDS.md](COMMANDS.md) — `generate-prp` command reference

### "I want to validate my implementation"
- [USERGUIDE.md](USERGUIDE.md) — Workflow: Feature Spec to Implementation, Phase 4
- [COMMANDS.md](COMMANDS.md) — `validate` command reference

### "I want to plan multiple features"
- [USERGUIDE.md](USERGUIDE.md) — Workflow: Multiple Features & Planning
- [README.md](README.md) — Best Practices section

### "I want to export artifacts"
- [README.md](README.md) — `export` command section
- [USERGUIDE.md](USERGUIDE.md) — Use Case 3: Export for Stakeholders
- [COMMANDS.md](COMMANDS.md) — `export` command reference

### "Something isn't working"
- [README.md](README.md) — Troubleshooting section
- [USERGUIDE.md](USERGUIDE.md) — Troubleshooting Common Issues section
- [COMMANDS.md](COMMANDS.md) — Troubleshooting under relevant command

---

## 📋 Checklists

### Initial Setup Checklist
- [ ] Read README.md — Overview & Installation (10 min)
- [ ] Install Python dependencies
- [ ] Verify Foundry Local is running
- [ ] Run `python ccp.py init-project`
- [ ] Run `python ccp.py health` to verify setup
- [ ] Review generated `context/claude.md`
- [ ] Read USERGUIDE.md to understand workflows

### First Feature Checklist
- [ ] Run `python ccp.py new-feature`
- [ ] Answer all 6 questions about the feature
- [ ] Review generated spec in `context/INITIAL.md`
- [ ] Run `python ccp.py generate-prp --feature my-feature`
- [ ] Review generated PRP in `context/prps/my-feature.md`
- [ ] Use PRP with Claude Code to implement
- [ ] Run `python ccp.py validate --feature my-feature`
- [ ] Review validation report in `context/validation/my-feature.md`
- [ ] Update `context/claude.md` with successful patterns

### Weekly Health Check
- [ ] Run `python ccp.py health --generate-report`
- [ ] Review `context/health-report.md`
- [ ] Identify stale or incomplete features
- [ ] Prioritize next work based on health metrics
- [ ] Update sprint/project plan

---

## 💾 File Organization

```
ContextCraftPro/
├── README.md                    ← Main documentation
├── USERGUIDE.md                 ← Step-by-step workflows
├── COMMANDS.md                  ← Command reference
├── DOCUMENTATION_INDEX.md       ← This file
├── docs/
│   └── llm-architecture.md      ← Technical architecture
├── context/
│   ├── INITIAL.md              ← Your feature specs
│   ├── claude.md               ← Coding rules
│   ├── prps/                   ← Generated PRPs
│   └── validation/             ← Validation reports
└── ...
```

---

## 🔗 Key Links

**Core Documentation**
- [README.md](README.md) — Main guide
- [USERGUIDE.md](USERGUIDE.md) — Practical examples
- [COMMANDS.md](COMMANDS.md) — Command reference
- [docs/llm-architecture.md](docs/llm-architecture.md) — Architecture

**Your Work**
- `context/INITIAL.md` — Your feature specifications
- `context/claude.md` — Your coding rules
- `context/prps/` — Generated PRPs for implementation
- `context/validation/` — Implementation validation reports

**Configuration**
- `config/contextcraft.yaml` — Settings and paths
- `context/project-profile.yaml` — Auto-detected repo info

---

## ❓ FAQ

**Q: Which document should I read first?**
A: [README.md](README.md) — Overview and Installation sections (15 minutes)

**Q: How do I see what each command does?**
A: [COMMANDS.md](COMMANDS.md) has a complete reference with examples

**Q: I want to learn by doing, not reading.**
A: Follow [USERGUIDE.md](USERGUIDE.md) Step 1-3 while running commands

**Q: I need help with a specific feature.**
A: Check [USERGUIDE.md](USERGUIDE.md) for that use case, or [COMMANDS.md](COMMANDS.md) for command details

**Q: How is ContextCraftPro different from X tool?**
A: Read [README.md](README.md) — Key Principles section

**Q: Can I modify how it works?**
A: Yes! See [docs/llm-architecture.md](docs/llm-architecture.md) for architecture, then review source code in `core/`

**Q: What if Foundry Local isn't working?**
A: See [README.md](README.md) — Troubleshooting section

---

## 🎓 Learning Resources

### For Different Learning Styles

**Visual Learners**
- Check directory structure in [README.md](README.md)
- Look at example outputs in [USERGUIDE.md](USERGUIDE.md)

**Hands-On Learners**
- Follow Path 3 from "Reading Paths" above
- Use `--dry-run` flag to preview without committing

**Reference Lovers**
- Use [COMMANDS.md](COMMANDS.md) as your main guide
- Keep it open while working

**Architecture Nerds**
- Deep dive into [docs/llm-architecture.md](docs/llm-architecture.md)
- Review source code in `core/`

---

## 📞 Still Need Help?

1. **Search documentation** — Use Ctrl+F in each document
2. **Check README.md Troubleshooting** — Common issues covered
3. **Check USERGUIDE.md Troubleshooting** — More examples
4. **Review logs** — `cat runtime/logs/ccp.log | jq .`
5. **Try --help** — `python ccp.py <command> --help`
6. **Try --verbose** — `python ccp.py <command> --verbose` for debugging

---

*Last updated: 2025-11-21*
*ContextCraftPro v1.0*
