#!/usr/bin/env node
/**
 * Email Sender via Resend API
 * Nutzt Resend für zuverlässigen Email-Versand
 */

const { Resend } = require('resend');

// API Key aus Umgebung oder Datei laden
const API_KEY = process.env.RESEND_API_KEY || require('fs').readFileSync('.env.resend', 'utf8')
  .split('\n').find(line => line.startsWith('RESEND_API_KEY='))?.split('=')[1]?.trim();

const resend = new Resend(API_KEY);

async function sendEmail(to, subject, htmlContent, from = 'onboarding@resend.dev') {
    try {
        const data = await resend.emails.send({
            from: from,
            to: to,
            subject: subject,
            html: htmlContent
        });
        
        console.log('✅ Email gesendet:', data);
        return data;
    } catch (error) {
        console.error('❌ Fehler beim Senden:', error);
        throw error;
    }
}

// Test
if (require.main === module) {
    // Beispiel-Email
    sendEmail(
        'keepitfsimple@gmail.com',
        'Test von Peter',
        '<p>Hallo! <strong>Resend funktioniert!</strong></p>'
    );
}

module.exports = { sendEmail };
