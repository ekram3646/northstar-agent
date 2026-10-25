import express from 'express';
import path from 'path';
import fs from 'fs';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { GoogleGenAI } from '@google/genai';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Serve static dataset & artifacts if needed
const DATASET_DIR = path.join(__dirname, 'dataset');
const EVAL_DIR = path.join(__dirname, 'evaluation');

// Utility to parse CSV cleanly
function parseCsv(filepath: string): any[] {
  if (!fs.existsSync(filepath)) return [];
  const content = fs.readFileSync(filepath, 'utf-8');
  const lines = content.split('\n').filter(l => l.trim().length > 0);
  if (lines.length === 0) return [];

  const parseLine = (line: string): string[] => {
    const result: string[] = [];
    let current = '';
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      if (char === '"' && (i === 0 || line[i - 1] !== '\\')) {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        result.push(current.replace(/^"|"$/g, '').trim());
        current = '';
      } else {
        current += char;
      }
    }
    result.push(current.replace(/^"|"$/g, '').trim());
    return result;
  };

  const headers = parseLine(lines[0]);
  return lines.slice(1).map(line => {
    const values = parseLine(line);
    const obj: any = {};
    headers.forEach((h, idx) => {
      obj[h] = values[idx] || '';
    });
    return obj;
  });
}

// API Endpoints

// 1. Get Cases List
app.get('/api/cases', (req, res) => {
  const requests = parseCsv(path.join(DATASET_DIR, 'deletion_requests.csv'));
  const outputs = parseCsv(path.join(__dirname, 'output.csv'));
  const outputMap = new Map(outputs.map(o => [o.case_id, o]));

  const search = (req.query.search as string || '').toLowerCase();
  const statusFilter = req.query.status as string || 'ALL';

  let filtered = requests.map(r => {
    const out = outputMap.get(r.case_id);
    let steps = [];
    try {
      steps = out ? JSON.parse(out.steps_json) : [];
    } catch (e) {
      steps = [];
    }
    return {
      case_id: r.case_id,
      email: r.email,
      requested_at: r.requested_at,
      reported_status: r.reported_status,
      reported_at: r.reported_at,
      audit_at: r.audit_at,
      request_text: r.request_text,
      deletion_status: out ? out.deletion_status : 'PENDING',
      step_count: steps.length,
      steps_json: steps
    };
  });

  if (statusFilter !== 'ALL') {
    filtered = filtered.filter(c => c.deletion_status === statusFilter);
  }

  if (search) {
    filtered = filtered.filter(c =>
      c.case_id.toLowerCase().includes(search) ||
      c.email.toLowerCase().includes(search) ||
      c.request_text.toLowerCase().includes(search)
    );
  }

  res.json({
    total: filtered.length,
    cases: filtered
  });
});

// 2. Get Case Details by ID
app.get('/api/cases/:id', (req, res) => {
  const caseId = req.params.id;
  const requests = parseCsv(path.join(DATASET_DIR, 'deletion_requests.csv'));
  const reqCase = requests.find(r => r.case_id === caseId);

  if (!reqCase) {
    return res.status(404).json({ error: 'Case not found' });
  }

  const identities = parseCsv(path.join(DATASET_DIR, 'user_identities.csv'));
  const userIdent = identities.find(i => i.email.toLowerCase() === reqCase.email.toLowerCase()) || {
    user_id: `user_resolved_${caseId}`,
    email: reqCase.email,
    phone: '+1-555-0199',
    email_hash: 'hash_sha256_mock',
    name: 'Resolved Customer'
  };

  const activities = parseCsv(path.join(DATASET_DIR, 'system_activity.csv'));
  const userActivities = activities.filter(a => a.user_id === userIdent.user_id || a.details.includes(reqCase.email));

  const rules = parseCsv(path.join(DATASET_DIR, 'deletion_rules.csv'));
  const outputs = parseCsv(path.join(__dirname, 'output.csv'));
  const out = outputs.find(o => o.case_id === caseId);

  let steps = [];
  try {
    steps = out ? JSON.parse(out.steps_json) : [];
  } catch (e) {
    steps = [];
  }

  res.json({
    case_id: reqCase.case_id,
    email: reqCase.email,
    requested_at: reqCase.requested_at,
    reported_status: reqCase.reported_status,
    reported_at: reqCase.reported_at,
    audit_at: reqCase.audit_at,
    request_text: reqCase.request_text,
    deletion_status: out ? out.deletion_status : 'PENDING',
    identity: userIdent,
    activities: userActivities,
    rules: rules,
    steps_json: steps
  });
});

// 3. Run Audit Pipeline
app.post('/api/audit/run', (req, res) => {
  try {
    execSync('python3 scripts/run_audit.py', { cwd: __dirname });
    execSync('python3 scripts/evaluate.py', { cwd: __dirname });
    execSync('python3 scripts/package_submission.py', { cwd: __dirname });
    res.json({ status: 'SUCCESS', message: 'Audit pipeline executed and output.csv updated.' });
  } catch (err: any) {
    res.status(500).json({ error: err.message || 'Audit execution failed' });
  }
});

// 4. Get Rules
app.get('/api/rules', (req, res) => {
  const rules = parseCsv(path.join(DATASET_DIR, 'deletion_rules.csv'));
  res.json({ rules });
});

// 5. Get Evaluation Report
app.get('/api/evaluation', (req, res) => {
  const evalPath = path.join(EVAL_DIR, 'evaluation_report.md');
  const content = fs.existsSync(evalPath) ? fs.readFileSync(evalPath, 'utf-8') : 'Evaluation report pending.';
  res.json({ content });
});

// 6. Get Token Usage
app.get('/api/usage', (req, res) => {
  const usagePath = path.join(EVAL_DIR, 'usage_report.md');
  const content = fs.existsSync(usagePath) ? fs.readFileSync(usagePath, 'utf-8') : 'Usage report pending.';
  res.json({ content });
});

// 7. Download Files
app.get('/api/download/output', (req, res) => {
  const file = path.join(__dirname, 'output.csv');
  if (fs.existsSync(file)) {
    res.download(file, 'output.csv');
  } else {
    res.status(404).send('output.csv not found');
  }
});

app.get('/api/download/zip', (req, res) => {
  const file = path.join(__dirname, 'code.zip');
  if (fs.existsSync(file)) {
    res.download(file, 'code.zip');
  } else {
    res.status(404).send('code.zip not found');
  }
});

// Vite Integration in Development Mode
if (process.env.NODE_ENV !== 'production') {
  const { createServer: createViteServer } = await import('vite');
  const vite = await createViteServer({
    server: { middlewareMode: true },
    appType: 'spa',
  });
  app.use(vite.middlewares);
} else {
  app.use(express.static(path.join(__dirname, 'dist')));
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`Northstar Deletion Audit Server listening on http://localhost:${PORT}`);
});
