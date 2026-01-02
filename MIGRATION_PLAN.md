# Migration Plan: VPS-Primary Development Environment

**Created:** 2026-01-02
**Status:** In Progress
**Strategy:** VPS-Primary with Laptop Thin Clients

---

## 🎯 **Architecture Overview**

### **Primary Work Environment: Hostinger VPS**
- **All development work happens on VPS via SSH/tmux**
- **RAG stack runs on VPS** (Qdrant, RabbitMQ, TimescaleDB)
- **n8n automation workflows on VPS**
- **Accessible from anywhere** (laptop, phone, work PC via Tailscale)

### **Laptop Roles: Thin Clients**
- **New ThinkPad (Ubuntu 24)**: Git operations, file editing, VPS access point
- **Legacy Laptop**: Archive and decommission after final transfer
- **Both laptops**: Minimal local setup, SSH into VPS for heavy work

---

## 📊 **Current State Summary**

### VPS (srv1216617 - 72.62.160.2) ✅ **PRODUCTION READY**
| Component | Status | Details |
|-----------|--------|---------|
| Docker Services | ✅ Running | n8n, Qdrant, RabbitMQ, TimescaleDB, PostgreSQL |
| RAG Collections | ✅ Active | 3 collections: external_docs, rugs_protocol, rl_design |
| Git Repos | ✅ Clean | claude-flow (main), VECTRA-PLAYER (main) |
| Python Env | ✅ Ready | 7.3GB venv with qdrant-client, sentence-transformers |
| Claude Code | ✅ Configured | 5 plugins enabled |
| Resources | ✅ Healthy | 69GB disk free, 5.1GB RAM available |
| SSH Keys | ✅ Present | All keys transferred to /root/.ssh/ |

### New ThinkPad (Ubuntu 24) ⚠️ **NEEDS CONFIGURATION**
| Component | Status | Required Action |
|-----------|--------|-----------------|
| claude-flow repo | ⚠️ Wrong branch | On `claude/review-repo-state-rnXFK`, need to pull/merge |
| Claude Code Plugin | ❌ Not installed | Run ./install.sh |
| SSH Config | ❌ Missing | Configure ~/.ssh/config for VPS access |
| Python Deps | ❌ Not installed | Optional (only if testing locally) |
| Path References | ❌ Broken | .mcp.json, sync scripts reference /home/nomad |

### Legacy Laptop ⚠️ **READY FOR ARCHIVAL**
| Task | Action |
|------|--------|
| Verify final transfer | Ensure all important files copied to VPS |
| Archive credentials | Backup SSH keys, API keys to secure location |
| Clean workspace | Remove old projects after verification |

---

## 🚀 **Implementation Plan**

### **PHASE 1: Enable VPS Access from New ThinkPad** (Priority 1)

#### Step 1.1: Verify SSH Key on VPS
```bash
# Run on VPS (already done, keys are there)
ls -la /root/.ssh/
# Should show: hostinger_vps, id_rsa, id_ed25519, etc.
```

#### Step 1.2: Download SSH Key to New ThinkPad
```bash
# On New ThinkPad
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Option A: If you have temporary VPS access via password
scp root@72.62.160.2:/root/.ssh/hostinger_vps ~/.ssh/
# (Will need to enter root password)

# Option B: Use Tailscale IP (if connected)
scp root@100.113.138.27:/root/.ssh/hostinger_vps ~/.ssh/

# Set correct permissions
chmod 600 ~/.ssh/hostinger_vps
```

#### Step 1.3: Configure SSH on New ThinkPad
```bash
# On New ThinkPad
cat >> ~/.ssh/config << 'EOF'
Host hostinger-vps
    HostName 72.62.160.2
    User root
    IdentityFile ~/.ssh/hostinger_vps
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host hostinger-vps-tailscale
    HostName 100.113.138.27
    User root
    IdentityFile ~/.ssh/hostinger_vps
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF

chmod 600 ~/.ssh/config
```

#### Step 1.4: Test VPS Connection
```bash
# On New ThinkPad
ssh hostinger-vps "hostname && uptime"
# Should show: srv1216617 and uptime

# Test Tailscale fallback
ssh hostinger-vps-tailscale "hostname"
```

---

### **PHASE 2: Configure New ThinkPad Local Environment** (Priority 2)

#### Step 2.1: Fix Local Path References
```bash
# On New ThinkPad
cd /home/user/claude-flow

# Fix MCP server path
sed -i 's|/home/nomad/Desktop/claude-flow|/home/user/claude-flow|g' .mcp.json

# Fix sync scripts in hostinger-vps-infrastructure
cd integrations/hostinger-vps-infrastructure
sed -i 's|LOCAL_BASE="/home/nomad/Desktop"|LOCAL_BASE="/home/user"|g' scripts/sync-to-vps.sh
sed -i 's|LOCAL_BASE="/home/nomad/Desktop"|LOCAL_BASE="/home/user"|g' scripts/sync-from-vps.sh

# Commit fixes
cd /home/user/claude-flow
git add .mcp.json
git add integrations/hostinger-vps-infrastructure/scripts/*.sh
git commit -m "fix: Update paths from /home/nomad to /home/user for new ThinkPad"
```

#### Step 2.2: Install claude-flow Plugin
```bash
# On New ThinkPad
cd /home/user/claude-flow
./install.sh --symlink

# Verify installation
ls -la ~/.claude/commands
ls -la ~/.claude/agents
```

#### Step 2.3: Sync Git State with VPS
```bash
# On New ThinkPad
cd /home/user/claude-flow

# Merge your review branch into main
git checkout main
git pull origin main
git merge claude/review-repo-state-rnXFK
git push origin main

# Push the review branch for backup
git push -u origin claude/review-repo-state-rnXFK
```

#### Step 2.4: Optional - Local Python Setup (Only if Testing Locally)
```bash
# Only needed if you want to run RAG/Jupyter locally
# Otherwise skip - all work happens on VPS

cd /home/user/claude-flow/rag-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd /home/user/claude-flow/jupyter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd /home/user/claude-flow/mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### **PHASE 3: Configure Legacy Laptop** (Priority 3)

#### Step 3.1: Setup SSH Access to VPS (Same as ThinkPad)
```bash
# On Legacy Laptop
# Follow Step 1.2-1.4 from Phase 1 above
# (SSH key download, config setup, test connection)
```

#### Step 3.2: Verify No Missing Files
```bash
# On Legacy Laptop - Compare with VPS
ssh hostinger-vps "ls -la /root/projects/"
ls -la ~/Desktop/

# Check for any projects not on VPS
# If found, transfer them:
rsync -avz --progress ~/Desktop/missing-project/ hostinger-vps:~/projects/missing-project/
```

#### Step 3.3: Archive and Clean
```bash
# On Legacy Laptop - After verification

# Backup credentials to secure location
tar -czf ~/credentials-backup-$(date +%Y%m%d).tar.gz \
  ~/.ssh/ \
  ~/.aws/ \
  ~/.config/
# Copy this to external drive or secure cloud storage

# Archive old projects (optional)
tar -czf ~/Desktop/archive-$(date +%Y%m%d).tar.gz ~/Desktop/projects/

# Clean workspace (after verification!)
# rm -rf ~/Desktop/old-project-name
```

---

### **PHASE 4: VPS Optimization** (Priority 4)

#### Step 4.1: Create Persistent tmux Session
```bash
# On VPS
# Create default claude-code work session
tmux new-session -d -s claude-main -n workspace
tmux send-keys -t claude-main:workspace "cd /root/projects/claude-flow" C-m

# Attach to it
tmux attach -t claude-main
```

#### Step 4.2: Setup Automated Backups (Recommended)
```bash
# On VPS
cat > /root/scripts/backup-git-repos.sh << 'EOF'
#!/bin/bash
# Backup all git repos to VPS backup location
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/backups/$DATE"
mkdir -p "$BACKUP_DIR"

cd /root/projects
for repo in claude-flow VECTRA-PLAYER; do
  if [ -d "$repo/.git" ]; then
    echo "Backing up $repo..."
    tar -czf "$BACKUP_DIR/$repo.tar.gz" "$repo/"
  fi
done

# Keep only last 7 days of backups
find /root/backups -type d -mtime +7 -exec rm -rf {} +
echo "Backup complete: $BACKUP_DIR"
EOF

chmod +x /root/scripts/backup-git-repos.sh

# Add to crontab (daily at 2am)
(crontab -l 2>/dev/null; echo "0 2 * * * /root/scripts/backup-git-repos.sh >> /var/log/git-backup.log 2>&1") | crontab -
```

#### Step 4.3: Configure RAG Stack Health Monitoring
```bash
# On VPS
# n8n workflow already exists: "Simple RAG Health Check"
# Test it:
curl http://localhost:5678/webhook/health

# Should return: {"status":"healthy","qdrant":{"status":"ok"},...}
```

#### Step 4.4: Optimize Docker Resource Limits (Optional)
```bash
# On VPS - Only if you see resource issues
cd /root/rag-stack

# Edit docker-compose.yml to add memory limits
# This prevents any single container from consuming all RAM
```

---

## 🔄 **Daily Workflow**

### **From New ThinkPad (or any device)**

#### Morning: Connect to VPS
```bash
# Connect via SSH
ssh hostinger-vps

# Or via Tailscale (more reliable)
ssh hostinger-vps-tailscale

# Attach to existing session or create new
tmux attach -t claude-main || tmux new -s claude-main

# Navigate to project
cd /root/projects/claude-flow

# Start Claude Code
claude
```

#### During Work: Use Claude Code on VPS
- All commands (/tdd, /debug, /verify, etc.) work on VPS
- All agents available
- RAG stack accessible (Qdrant collections)
- n8n workflows accessible
- Git operations from VPS

#### End of Day: Detach (Keep Session Running)
```bash
# Press Ctrl+b, then d (detach from tmux)
# Session keeps running on VPS
# Can reconnect from phone, laptop, anywhere
```

---

## 📱 **Mobile/Remote Access**

### **From Phone (Termux)**
```bash
# Install Termux from F-Droid
pkg install openssh

# Copy SSH key (one-time)
# Use laptop to transfer: scp ~/.ssh/hostinger_vps phone:/data/data/com.termux/files/home/.ssh/

# Connect to VPS
ssh -i ~/.ssh/hostinger_vps root@72.62.160.2

# Attach to session
tmux attach -t claude-main
```

### **From Work PC (if allowed)**
```bash
# Via Tailscale (most reliable through corporate firewalls)
ssh root@100.113.138.27
tmux attach -t claude-main
```

---

## 🔧 **Troubleshooting**

### **Can't SSH to VPS**
```bash
# Check 1: VPS is up
ping 72.62.160.2

# Check 2: Tailscale connected
tailscale status

# Check 3: SSH key permissions
ls -la ~/.ssh/hostinger_vps
chmod 600 ~/.ssh/hostinger_vps

# Check 4: Try Tailscale IP instead
ssh root@100.113.138.27
```

### **VPS tmux Session Lost**
```bash
# List sessions
tmux list-sessions

# If none exist, create new
tmux new-session -s claude-main -n workspace
cd /root/projects/claude-flow
```

### **Docker Services Down on VPS**
```bash
# On VPS
docker ps -a

# Restart specific service
docker restart n8n
docker restart qdrant

# Or restart entire stack
cd /root/rag-stack
docker-compose restart
```

### **RAG Collections Empty**
```bash
# On VPS - Check collections
curl http://localhost:6333/collections

# If empty, re-ingest (from claude-flow repo)
cd /root/projects/claude-flow/rag-pipeline
source /root/venv/bin/activate
python -m ingestion.ingest
```

---

## ✅ **Verification Checklist**

### **New ThinkPad Setup Complete When:**
- [ ] Can SSH to VPS: `ssh hostinger-vps`
- [ ] Claude Code plugin installed locally: `ls ~/.claude/commands`
- [ ] Paths fixed: `.mcp.json` uses `/home/user`
- [ ] Git synced: `main` branch up to date
- [ ] Can attach to VPS tmux: `ssh hostinger-vps -t "tmux attach"`

### **Legacy Laptop Archived When:**
- [ ] All projects verified on VPS: `ssh hostinger-vps "ls /root/projects"`
- [ ] Credentials backed up to secure location
- [ ] Can SSH to VPS from legacy laptop
- [ ] Old workspace cleaned (optional)

### **VPS Optimized When:**
- [ ] Persistent tmux session exists: `claude-main`
- [ ] All 5 Docker containers running: `docker ps`
- [ ] All 3 Qdrant collections active
- [ ] n8n health webhook responding: `curl localhost:5678/webhook/health`
- [ ] Automated backups configured (optional)

---

## 🎯 **Priority Execution Order**

**While at work (away from laptops):**
1. ✅ VPS is already working - no action needed
2. ✅ Migration plan created (this document)
3. ✅ Plan committed to git

**When you get home to New ThinkPad:**
1. **Phase 1**: Enable VPS access (Steps 1.2-1.4) - 10 minutes
2. **Phase 2**: Fix local paths and install plugin (Steps 2.1-2.3) - 15 minutes
3. **Test**: SSH into VPS, attach to tmux, start Claude Code - 2 minutes

**When you access Legacy Laptop:**
1. **Phase 3**: Enable VPS access (same as ThinkPad) - 10 minutes
2. **Phase 3**: Verify no missing files - 10 minutes
3. **Optional**: Archive and clean - 30 minutes

**Future optimization (low priority):**
1. **Phase 4**: VPS tmux sessions, backups, monitoring - 30 minutes

---

## 📝 **Notes**

- **VPS Public IP**: 72.62.160.2
- **VPS Tailscale IP**: 100.113.138.27
- **VPS Hostname**: srv1216617
- **SSH Key Name**: hostinger_vps (on VPS at /root/.ssh/)
- **Primary Git Branch**: main (both repos)
- **VPS Projects**: /root/projects/claude-flow, /root/projects/VECTRA-PLAYER
- **RAG Collections**: external_docs, rugs_protocol, rl_design

---

**Last Updated:** 2026-01-02
**Next Review:** After New ThinkPad setup complete
