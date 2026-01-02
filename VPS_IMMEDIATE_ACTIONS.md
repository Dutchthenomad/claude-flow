# VPS Immediate Actions - Work From Hostinger Terminal

**For use while accessing VPS via Hostinger web terminal**
**No laptop access needed - do this NOW from work**

---

## 🎯 **What You Can Do Right Now**

You have VPS access via Hostinger web terminal. Here's what you can accomplish immediately:

---

## **Step 1: Pull the Latest Migration Plan** (2 minutes)

```bash
# Navigate to claude-flow repo
cd /root/projects/claude-flow

# Pull the latest changes (includes MIGRATION_PLAN.md)
git fetch origin
git checkout main
git pull origin main

# Merge the review branch that has the migration plan
git merge origin/claude/review-repo-state-rnXFK

# View the migration plan
cat MIGRATION_PLAN.md | less
# Press 'q' to exit
```

---

## **Step 2: Create Persistent tmux Session** (5 minutes)

This creates a persistent work session you can access from anywhere:

```bash
# Create main work session
tmux new-session -s claude-main -n workspace

# Inside tmux, set up your workspace
cd /root/projects/claude-flow

# You're now in a persistent session!
# To detach: Press Ctrl+b, then d
# To reattach later: tmux attach -t claude-main
```

**Why this matters:**
- Session persists even if you close the browser
- Can reconnect from laptop, phone, anywhere
- Multiple windows for different tasks

**Tmux Quick Reference:**
- `Ctrl+b d` - Detach (session keeps running)
- `Ctrl+b c` - Create new window
- `Ctrl+b n` - Next window
- `Ctrl+b p` - Previous window
- `Ctrl+b [` - Scroll mode (press 'q' to exit)

---

## **Step 3: Verify All Services Running** (3 minutes)

Check that all infrastructure is healthy:

```bash
# Check Docker containers
docker ps -a

# Should show 5 running containers:
# - n8n
# - n8n-postgres
# - qdrant
# - rabbitmq
# - timescaledb

# Check service health
echo "=== n8n Health ==="
curl -I http://localhost:5678

echo -e "\n=== Qdrant Collections ==="
curl -s http://localhost:6333/collections | head -50

echo -e "\n=== RabbitMQ Management ==="
curl -I http://localhost:15672

echo -e "\n=== Docker Resource Usage ==="
docker stats --no-stream
```

---

## **Step 4: Test RAG Stack** (5 minutes)

Verify your RAG collections are working:

```bash
# Activate Python venv
source /root/venv/bin/activate

# Check Qdrant collections
python3 << 'EOF'
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)
collections = client.get_collections()

print("=== RAG Collections ===")
for collection in collections.collections:
    info = client.get_collection(collection.name)
    print(f"\n{collection.name}:")
    print(f"  Vectors: {info.points_count}")
    print(f"  Status: {info.status}")
EOF

# Test a sample query
python3 << 'EOF'
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="localhost", port=6333)
encoder = SentenceTransformer('all-MiniLM-L6-v2')

# Test search on existing collection
query = "rugs.fun game mechanics"
query_vector = encoder.encode(query).tolist()

results = client.search(
    collection_name="rugs_protocol",
    query_vector=query_vector,
    limit=3
)

print(f"\n=== Search Results for '{query}' ===")
for i, result in enumerate(results, 1):
    print(f"\n{i}. Score: {result.score:.3f}")
    print(f"   {result.payload.get('text', 'No text')[:100]}...")
EOF
```

---

## **Step 5: Review Current Git State** (3 minutes)

```bash
# Check both repos
echo "=== claude-flow repo ==="
cd /root/projects/claude-flow
git status
git log --oneline -5
git branch -a

echo -e "\n=== VECTRA-PLAYER repo ==="
cd /root/projects/VECTRA-PLAYER
git status
git log --oneline -5

# Return to claude-flow
cd /root/projects/claude-flow
```

---

## **Step 6: Test n8n Workflow** (2 minutes)

Test your n8n health check workflow:

```bash
# Test the health check endpoint
curl http://localhost:5678/webhook/health

# Should return JSON with:
# {"status":"healthy","qdrant":{"status":"ok"},...}

# Access n8n UI (from external)
echo "n8n UI accessible at: http://72.62.160.2:5678"
```

---

## **Step 7: Create Backup Script** (10 minutes)

Set up automated git backups:

```bash
# Create scripts directory if it doesn't exist
mkdir -p /root/scripts

# Create backup script
cat > /root/scripts/backup-git-repos.sh << 'EOF'
#!/bin/bash
# Backup all git repos to VPS backup location
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/backups/$DATE"
mkdir -p "$BACKUP_DIR"

echo "Starting backup: $DATE"

# Backup each repo
cd /root/projects
for repo in */; do
  repo=${repo%/}  # Remove trailing slash
  if [ -d "$repo/.git" ]; then
    echo "Backing up $repo..."
    tar -czf "$BACKUP_DIR/$repo.tar.gz" "$repo/"
    echo "  ✓ $repo.tar.gz created"
  fi
done

# Show backup size
du -sh "$BACKUP_DIR"

# Keep only last 7 days of backups
find /root/backups -type d -mtime +7 -exec rm -rf {} + 2>/dev/null

echo "Backup complete: $BACKUP_DIR"
EOF

# Make executable
chmod +x /root/scripts/backup-git-repos.sh

# Test it
/root/scripts/backup-git-repos.sh

# Verify backup created
ls -lh /root/backups/
```

---

## **Step 8: Setup Automated Backups** (5 minutes)

Configure daily automated backups:

```bash
# Add to crontab (daily at 2am UTC)
(crontab -l 2>/dev/null; echo "0 2 * * * /root/scripts/backup-git-repos.sh >> /var/log/git-backup.log 2>&1") | crontab -

# Verify crontab
crontab -l

# Create log file
touch /var/log/git-backup.log
chmod 644 /var/log/git-backup.log
```

---

## **Step 9: Document VPS Credentials** (5 minutes)

Create a secure credentials file on VPS:

```bash
# Create credentials file (not in git)
cat > /root/CREDENTIALS.md << 'EOF'
# VPS Credentials and Access

**IMPORTANT: This file is gitignored. Keep secure.**

## VPS Access
- Public IP: 72.62.160.2
- Tailscale IP: 100.113.138.27
- SSH User: root
- SSH Key: /root/.ssh/hostinger_vps

## Docker Services

### n8n
- URL: http://72.62.160.2:5678
- User: [Add your n8n username]
- Password: [Add your n8n password]

### RabbitMQ
- Management UI: http://72.62.160.2:15672
- User: [Check /root/rag-stack/.env]
- Password: [Check /root/rag-stack/.env]

### Qdrant
- URL: http://72.62.160.2:6333
- No auth configured

### TimescaleDB
- Host: localhost:5433
- Database: [Check /root/rag-stack/.env]
- User: [Check /root/rag-stack/.env]
- Password: [Check /root/rag-stack/.env]

## API Keys
- Anthropic API: [Add if set in environment]
- Resend API (n8n SMTP): [Check /root/.env]

## GitHub
- SSH Key: /root/.ssh/id_rsa (or id_ed25519)
- Repos: claude-flow, VECTRA-PLAYER

## Notes
- Update this file whenever credentials change
- Backup externally to secure location
EOF

# Secure the file
chmod 600 /root/CREDENTIALS.md

echo "Created /root/CREDENTIALS.md - fill in your credentials"
```

---

## **Step 10: Optimize Docker Resources** (Optional - 5 minutes)

Only if you notice resource issues:

```bash
# Check current resource usage
docker stats --no-stream

# If containers using too much memory, add limits
cd /root/rag-stack

# Backup original compose file
cp docker-compose.yml docker-compose.yml.backup

# Edit to add memory limits (example)
cat >> docker-compose.yml << 'EOF'

# Resource limits (add to each service)
# services:
#   qdrant:
#     mem_limit: 1g
#     memswap_limit: 1g
EOF

echo "Compose file backed up. Edit docker-compose.yml to add mem_limit if needed"
```

---

## **Step 11: Create Quick Access Aliases** (3 minutes)

Add helpful aliases to your shell:

```bash
# Add to .bashrc
cat >> /root/.bashrc << 'EOF'

# Claude Flow Aliases
alias cdf='cd /root/projects/claude-flow'
alias cdv='cd /root/projects/VECTRA-PLAYER'
alias venv='source /root/venv/bin/activate'
alias docker-status='docker ps -a && echo && docker stats --no-stream'
alias rag-health='curl -s http://localhost:6333/collections | python3 -m json.tool'
alias n8n-health='curl -s http://localhost:5678/webhook/health | python3 -m json.tool'

# tmux shortcuts
alias tm='tmux attach -t claude-main || tmux new -s claude-main'
alias tls='tmux list-sessions'
EOF

# Reload bashrc
source /root/.bashrc

# Test aliases
echo "Testing aliases:"
cdf && pwd
venv && which python
```

---

## **Step 12: Sync Git State** (5 minutes)

Make sure VPS has latest code:

```bash
cd /root/projects/claude-flow

# Fetch all branches
git fetch --all

# See all available branches
git branch -r

# Merge the migration plan branch into main
git checkout main
git pull origin main
git merge origin/claude/review-repo-state-rnXFK

# Push updated main (includes migration plan)
git push origin main

# Verify MIGRATION_PLAN.md exists
ls -lh MIGRATION_PLAN.md
```

---

## **✅ Completion Checklist**

After running these steps, verify:

- [ ] tmux session `claude-main` created and working
- [ ] All 5 Docker containers running (docker ps)
- [ ] RAG collections accessible (3 collections found)
- [ ] n8n health endpoint responding
- [ ] Backup script created and tested
- [ ] Automated backups configured (crontab -l)
- [ ] Aliases working (cdf, venv, docker-status)
- [ ] Git state synced (MIGRATION_PLAN.md present)
- [ ] CREDENTIALS.md created and filled in

---

## **🚀 What's Next**

### **While Still at Work:**
- Browse to http://72.62.160.2:5678 (n8n UI)
- Test workflows
- Explore RAG collections via Qdrant dashboard: http://72.62.160.2:6333/dashboard

### **When You Get Home:**
- Follow MIGRATION_PLAN.md Phase 1 on New ThinkPad (10 min)
- SSH into VPS: `ssh hostinger-vps`
- Attach to tmux: `tmux attach -t claude-main`
- Continue work in persistent session

### **From Phone (Later):**
- Install Termux
- Copy SSH key from VPS
- Connect and work from anywhere

---

## **⚠️ Important Notes**

**Hostinger Web Terminal Limitations:**
- Session may timeout after inactivity
- Copy/paste can be tricky
- Use tmux to preserve work across disconnects

**Always use tmux** when working via web terminal:
```bash
# Start or attach to main session
tmux attach -t claude-main || tmux new -s claude-main
```

**To safely disconnect:**
1. Press `Ctrl+b` then `d` (detach from tmux)
2. Work is preserved
3. Reconnect anytime with `tmux attach -t claude-main`

---

**Created:** 2026-01-02
**For:** Immediate VPS setup via Hostinger web terminal
