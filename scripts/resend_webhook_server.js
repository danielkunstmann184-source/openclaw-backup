#!/usr/bin/env node
/**
 * Resend Webhook Handler
 * Empfängt Emails von Resend und verarbeitet sie
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3001;
const INBOX_DIR = path.join(__dirname, '..', 'data', 'inbox');

// Inbox-Verzeichnis erstellen
if (!fs.existsSync(INBOX_DIR)) {
    fs.mkdirSync(INBOX_DIR, { recursive: true });
}

// Email speichern
function saveEmail(emailData) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `email_${timestamp}.json`;
    const filepath = path.join(INBOX_DIR, filename);
    
    fs.writeFileSync(filepath, JSON.stringify(emailData, null, 2));
    console.log(`✅ Email gespeichert: ${filename}`);
    return filename;
}

// Email zusammenfassen (einfache Version)
function summarizeEmail(emailData) {
    const subject = emailData.data?.subject || 'Kein Betreff';
    const from = emailData.data?.from || 'Unbekannt';
    const to = emailData.data?.to?.join(', ') || 'Unbekannt';
    
    return {
        from: from,
        to: to,
        subject: subject,
        received_at: new Date().toISOString(),
        summary: `Neue Email von ${from}: "${subject}"`
    };
}

// Webhook Server
const server = http.createServer((req, res) => {
    // Nur POST auf /webhook/resend erlauben
    if (req.method !== 'POST' || req.url !== '/webhook/resend') {
        res.writeHead(404);
        res.end('Not found');
        return;
    }
    
    let body = '';
    req.on('data', chunk => {
        body += chunk.toString();
    });
    
    req.on('end', () => {
        try {
            const event = JSON.parse(body);
            
            // Prüfe ob es ein email.received Event ist
            if (event.type === 'email.received') {
                console.log('📧 Neue Email empfangen!');
                
                // Speichern
                const filename = saveEmail(event);
                
                // Zusammenfassen
                const summary = summarizeEmail(event);
                
                // Summary auch speichern
                const summaryFile = path.join(INBOX_DIR, `summary_${filename}`);
                fs.writeFileSync(summaryFile, JSON.stringify(summary, null, 2));
                
                console.log('📝 Zusammenfassung:', summary.summary);
                
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'ok', message: 'Email received' }));
            } else {
                res.writeHead(200);
                res.end('Event ignored');
            }
        } catch (error) {
            console.error('❌ Fehler:', error);
            res.writeHead(500);
            res.end('Error');
        }
    });
});

server.listen(PORT, () => {
    console.log(`🚀 Resend Webhook Server läuft auf Port ${PORT}`);
    console.log(`📧 Webhook URL: http://dein-server:${PORT}/webhook/resend`);
    console.log(`💡 Tipp: In Resend Dashboard als Webhook eintragen!`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('👋 Server wird beendet...');
    server.close(() => {
        process.exit(0);
    });
});
