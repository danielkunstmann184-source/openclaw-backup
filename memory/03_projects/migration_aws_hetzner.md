# Migrationsplan: AWS → Hetzner

**Ziel:** Zero-Downtime Umzug ohne Datenverlust

---

## Phase 1: Vollständiges Backup (VOR dem Umzug)

### 1.1 Git-Backup (Wichtigste Daten)
```bash
cd /home/ubuntu/.openclaw/workspace
git add -A
git commit -m "Pre-Migration Backup: Stand vor Hetzner-Umzug"
git push origin master
```

### 1.2 API-Keys sichern
```bash
# Keys aus ~/.config/openclaw/ kopieren
mkdir -p ~/migration_backup
cp -r ~/.config/openclaw ~/migration_backup/
```

### 1.3 Cron-Jobs exportieren
```bash
# Liste aller Jobs speichern
openclaw cron list > ~/migration_backup/cron_jobs.json
```

### 1.4 System-Config
```bash
# Wichtige Configs sichern
cp ~/.openclaw/openclaw.json ~/migration_backup/ 2>/dev/null || true
cp -r ~/.openclaw/workspace ~/migration_backup/ 2>/dev/null || true
```

### 1.5 Komplettes Archiv erstellen
```bash
cd ~
tar -czvf openclaw_migration_$(date +%Y%m%d).tar.gz \
  .openclaw/ \
  .config/openclaw/ \
  migration_backup/
```

**Dieses Archiv auf sicheres Medium kopieren (Download/S3)**

---

## Phase 2: Hetzner Server einrichten

### 2.1 Server bestellen
- **Typ:** CX21 (2 vCPU, 4 GB RAM, 40 GB SSD)
- **Kosten:** 5,35 €/Monat (~6$)
- **OS:** Ubuntu 24.04 LTS

### 2.2 Grundkonfiguration
```bash
# Als root auf neuem Server
apt update && apt upgrade -y
apt install -y git curl wget vim htop

# Firewall aktivieren
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Node.js installieren (für OpenClaw)
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# OpenClaw installieren
npm install -g openclaw
```

### 2.3 SSH-Key einrichten
```bash
# Vom alten Server: ~/.ssh/authorized_keys kopieren
# ODER neuen Key generieren
ssh-keygen -t ed25519 -C "openclaw@hetzner"
```

---

## Phase 3: Daten wiederherstellen

### 3.1 Migration-Archiv übertragen
```bash
# Vom alten Server auf neuen kopieren
scp openclaw_migration_*.tar.gz root@<neue-hetzner-ip>:/root/

# Auf neuem Server entpacken
tar -xzvf openclaw_migration_*.tar.gz -C /
```

### 3.2 API-Keys wiederherstellen
```bash
mkdir -p ~/.config/openclaw
cp ~/migration_backup/openclaw/* ~/.config/openclaw/
```

### 3.3 Git-Repo klonen
```bash
mkdir -p ~/.openclaw
cd ~/.openclaw
git clone https://github.com/danielkunstmann184-source/openclaw-backup.git workspace
cd workspace
```

### 3.4 OpenClaw konfigurieren
```bash
openclaw doctor --fix
```

---

## Phase 4: Cron-Jobs wiederherstellen

### 4.1 Jobs neu erstellen
```bash
# cron_jobs.json wurde in Phase 1.3 exportiert
# Manuell oder via Script neu anlegen
```

**Alternative:** Ich kann die Jobs aus `memory/cron-jobs-config.md` neu erstellen.

### 4.2 Testläufe
```bash
# Einzelne Jobs testen
openclaw cron run <job-id>
```

---

## Phase 5: Testphase (PARALLEL)

### 5.1 Beide Server laufen parallel
- **AWS:** Läuft weiter (Sicherheit)
- **Hetzner:** Neu eingerichtet, im Test

### 5.2 Funktionstests
- [ ] Telegram-Bot reagiert
- [ ] Cron-Jobs laufen
- [ ] Notion-Integration funktioniert
- [ ] Git-Push funktioniert
- [ ] API-Keys sind korrekt

### 5.3 24-Stunden Test
- Einen Tag laufen lassen
- Alle Cron-Jobs mindestens einmal triggern lassen

---

## Phase 6: Umstellung

### 6.1 Telegram-Wechsel
- In Telegram: Bot-Father → Webhook auf neue IP umstellen
- ODER: Webhook-URL in OpenClaw-Config ändern

### 6.2 DNS (falls verwendet)
- Domain auf neue IP zeigen lassen
- TTL kurz vorher reduzieren

### 6.3 AWS-Instanz stoppen
- Erst nach 48h erfolgreichem Hetzner-Betrieb
- Nicht löschen, nur stoppen (für 1 Woche)

---

## Phase 7: Aufräumen

### 7.1 Nach 1 Woche erfolgreichem Betrieb
```bash
# AWS-Instanz beenden (kostet dann nichts mehr)
# Backup auf S3 für 3 Monate behalten
```

---

## 🛡️ Rollback-Plan

Falls etwas schiefgeht:

1. **AWS-Instanz starten** (läuft parallel)
2. **DNS/Webhook zurück auf AWS**
3. **Problem auf Hetzner beheben**
4. **Erneuter Versuch**

---

## 📋 Checkliste vor Start

- [ ] Git-Repo gepusht
- [ ] API-Keys gesichert
- [ ] Cron-Jobs exportiert
- [ ] Migration-Archiv erstellt
- [ ] Hetzner-Server bestellt
- [ ] Zeitfenster für Umzug (Wochenende?)

---

**Geschätzte Dauer:** 2-3 Stunden aktive Arbeit + 48h Testphase

**Wichtig:** Nie beide Server gleichzeitig auf dasselbe Telegram-Bot-Token zeigen lassen (sonst doppelte Antworten)!
