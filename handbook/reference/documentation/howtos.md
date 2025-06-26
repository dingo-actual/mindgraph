# How-Tos Guide

## Purpose

This guide provides actionable steps for creating effective how-to guides following the Diátaxis framework. A how-to guide is goal-oriented documentation that helps competent users accomplish specific tasks in real-world scenarios. This document helps documentation writers craft how-to guides that solve problems efficiently while maintaining clear boundaries with other documentation types.

## Prerequisites

- Understanding of the Diátaxis framework's four documentation types
- Experience with the domain you're documenting
- Access to test your instructions in realistic scenarios
- Ability to identify common user tasks and problems
- Basic technical writing skills

## Understanding How-To Guide Fundamentals

### Step 1: Recognize the User's Work Context

How-to guides serve users who are at work, not at study. Your reader has a specific goal and needs practical directions to achieve it. Unlike tutorials that build confidence through learning, how-to guides assume competence and focus on task completion.

**Example: Work vs Learning Context**
```markdown
# How-To Guide: Configure Load Balancing (✓)
Prerequisites: Basic understanding of networking

# Tutorial: Learn About Load Balancing (✗)
Let's explore what load balancing means...
```

The how-to addresses an immediate need; the tutorial provides education.

### Step 2: Define the Problem, Not the Tool

Structure how-to guides around meaningful user goals, not product features. How-to guides are about goals, projects and problems, not about tools. The machinery appears incidentally as the means to achieve the user's end.

**Example: Problem-Focused Titles**
```markdown
# Poor: Using the Config Command
The config command accepts these parameters...

# Better: How to Migrate Settings Between Environments
When deploying to production, you need to...
```

## Creating Goal-Oriented Structure

### Step 3: Write Action-Focused Titles

Every how-to guide title should clearly state what the user will accomplish. Use active verbs and specific outcomes that users search for when facing problems.

**Example: Effective How-To Titles**
```markdown
# How to Restore a Corrupted Database
# How to Debug Memory Leaks in Production
# How to Implement Zero-Downtime Deployments
# How to Configure Multi-Factor Authentication
# How to Optimize Query Performance
```

Each title promises a solution to a specific problem.

### Step 4: List Clear Prerequisites

State upfront what knowledge, access, or tools users need. This respects their time and prevents frustration from discovering missing requirements mid-task.

**Example: Prerequisites Section**
```markdown
## Prerequisites

- Admin access to the production server
- PostgreSQL 14+ installed
- At least 10GB free disk space
- Backup of current database
- Understanding of SQL basics
```

## Writing Practical Instructions

### Step 5: Focus on the Essential Path

A how-to guide serves the work of the already-competent user, whom you can assume to know what they want to do, and to be able to follow your instructions correctly. Eliminate explanations and focus on actions.

**Example: Action-Focused Writing**
```markdown
# Too Explanatory (✗)
First, let's understand why SSH keys are important.
They use asymmetric cryptography...

# Action-Focused (✓)
1. Generate your SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your@email.com"
   ```
2. Add the key to your SSH agent:
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```
```

### Step 6: Provide Escape Hatches

Real-world scenarios rarely follow the happy path. The how-to guide must prepare for the unexpected, alerting the user to its possibility and providing guidance on how to deal with it.

**Example: Handling Variations**
```markdown
## Step 3: Start the Migration

Run the migration command:
```bash
migrate --source old_db --target new_db
```

**If you see "Connection refused":**
- Check if the database is running: `pg_isready`
- Verify firewall rules allow port 5432
- Ensure connection string uses correct hostname

**For large databases (>100GB):**
Use the batch mode to prevent timeouts:
```bash
migrate --source old_db --target new_db --batch-size 1000
```
```

### Step 7: Make Decisions for the User

A how-to guide needs to be adaptable to real-world use-cases. However, avoid paralyzing users with too many options. Make sensible defaults clear.

**Example: Opinionated Guidance**
```markdown
## Configure Backup Retention

Set retention to 30 days (recommended for most cases):
```yaml
backup:
  retention_days: 30
  compression: gzip  # Best balance of speed/size
```

For compliance requirements, extend to 90 days:
```yaml
backup:
  retention_days: 90
```
```

## Ensuring Practical Value

### Step 8: Design for Adaptability

Write guides that users can modify for their specific contexts without losing their way. Provide the reasoning behind critical steps.

**Example: Adaptable Instructions**
```markdown
## Step 2: Configure the Service

1. Open the configuration file:
   ```bash
   nano /etc/myapp/config.yml
   ```

2. Set the memory limit based on your available RAM:
   ```yaml
   memory_limit: 2048  # MB - set to ~50% of system RAM
   ```

3. Configure worker processes:
   ```yaml
   workers: 4  # Typically CPU cores - 1
   ```
```

### Step 9: Include Verification Steps

Help users confirm they're on track without over-explaining. Quick checks prevent cascading failures.

**Example: Verification Points**
```markdown
## Step 4: Verify Installation

Check the service status:
```bash
systemctl status myapp
```

You should see:
```
Active: active (running)
Main PID: 12345
```

If the status shows "failed", check the logs:
```bash
journalctl -u myapp -n 50
```
```

### Step 10: Maintain Goal Focus Throughout

Every section should contribute directly to achieving the stated goal. Resist tangents, no matter how interesting.

**Example: Staying Focused**
```markdown
# How to Set Up Database Replication

## Configure the Primary Server

1. Edit postgresql.conf:
   ```bash
   wal_level = replica
   max_wal_senders = 3
   ```
   
   [Not here: "WAL stands for Write-Ahead Logging..."]

2. Restart PostgreSQL:
   ```bash
   systemctl restart postgresql
   ```
```

## Testing and Validation

### Step 11: Test in Realistic Scenarios

Unlike tutorials in controlled environments, how-to guides must work in messy real-world situations. Test with actual production-like setups.

**Example: Testing Matrix**
```markdown
Test your how-to guide against:
- [ ] Fresh installation
- [ ] Existing system with customizations  
- [ ] Different OS versions
- [ ] Various permission levels
- [ ] Network restrictions
- [ ] Resource constraints
- [ ] Previous failed attempts
```

### Step 12: Validate with Real Tasks

The ultimate test: can someone use your guide to solve an actual problem? Testing with synthetic scenarios misses real-world complexity.

**Example: Validation Protocol**
```markdown
1. Identify 3 users with the actual problem
2. Provide only the how-to guide URL
3. Monitor their progress without helping
4. Note where they hesitate or fail
5. Ask: "Did you achieve your goal?"
6. Revise based on failure patterns
```

## Common Anti-Patterns to Avoid

### The Tutorial Trap

Don't teach concepts in how-to guides. Users are working, not learning.

**Anti-pattern Example:**
```markdown
# Don't do this in how-to guides:
"Before we begin, let's understand what DNS is.
DNS stands for Domain Name System..."
```

### The Reference Overflow

Avoid listing every possible option. Focus on solving the specific problem.

**Anti-pattern Example:**
```markdown
# Avoid exhaustive lists:
"The command accepts 47 flags. Let's examine each:
--verbose: Increases output verbosity..."
```

### The Explanation Detour

Explanations belong elsewhere. Link to them if needed.

**Anti-pattern Example:**
```markdown
# Skip the theory:
"To understand why we use TLS 1.3, we need to
explore the history of SSL/TLS protocols..."
```

## Design Considerations

### Sequential Flow

The fundamental structure of a how-to guide is a sequence. It implies logical ordering in time, that there is a sense and meaning to this particular order.

**Example: Logical Sequence**
```markdown
## How to Deploy with Zero Downtime

1. **Prepare** the new version
2. **Verify** health checks pass
3. **Route** traffic gradually
4. **Monitor** error rates
5. **Complete** or rollback

[Each step depends on the previous one completing successfully]
```

### Meaningful Checkpoints

Structure guides with natural pause points where users can verify progress or safely stop.

**Example: Safe Stopping Points**
```markdown
## Checkpoint: Database Backed Up

Before proceeding to migration:
- ✓ Backup completed successfully
- ✓ Backup integrity verified  
- ✓ Restoration tested

You can safely stop here and resume later.
```

### Performance Implications

When procedures affect system performance, make this explicit with concrete metrics.

**Example: Performance Warnings**
```markdown
## Step 3: Rebuild Search Index

**Performance Impact:**
- Duration: ~20 minutes per million records
- CPU usage: 80-90% on indexing threads
- Disk I/O: Sustained 200MB/s reads
- User impact: Search may be slower

For minimal impact, run during off-peak hours.
```

## Maintenance Strategy

How-to guides require updates when:
- The problem-solving approach changes
- New edge cases emerge from user feedback
- Better solutions become available
- Performance characteristics change
- Tool versions introduce breaking changes

**Maintenance Checklist:**
- Monthly: Review user feedback for failures
- Quarterly: Re-test all procedures
- On release: Update for version changes
- Annually: Assess if problem still exists

## Quick Reference Card

| Element | How-To Guide Approach |
|---------|----------------------|
| **Purpose** | Enable task completion |
| **Audience** | Competent users at work |
| **Voice** | Direct, imperative ("Configure...", "Set...") |
| **Explanation** | Minimal - link to explanations |
| **Alternatives** | Practical variations only |
| **Testing** | In realistic scenarios |
| **Success Metric** | Task completed successfully |
| **Maintenance** | Update when approach changes |

## Conclusion

Writing effective how-to guides requires maintaining laser focus on the user's goal while resisting the urge to educate or explain. A how-to guide is concerned with work - a task or problem, with a practical goal. Maintain focus on that goal. Success comes from understanding that your reader is competent but facing a specific challenge, and your job is to guide them efficiently to a solution.

Unlike tutorials that own the entire learning experience, how-to guides insert themselves into the user's existing workflow. They must be adaptable enough to handle real-world complexity while remaining focused enough to be immediately useful. When done well, how-to guides become trusted tools that users return to whenever they face familiar problems, knowing they'll find a reliable path to success.