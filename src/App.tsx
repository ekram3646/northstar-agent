import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  Search,
  Filter,
  FileSpreadsheet,
  Download,
  Play,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Database,
  Cpu,
  BarChart3,
  FileCode,
  Layers,
  Clock,
  UserCheck,
  Sparkles,
  ArrowRight,
  ChevronRight,
  Info
} from 'lucide-react';

interface CaseItem {
  case_id: string;
  email: string;
  requested_at: string;
  reported_status: string;
  reported_at: string;
  audit_at: string;
  request_text: string;
  deletion_status: string;
  step_count: number;
  steps_json: any[];
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'cases' | 'rules' | 'eval' | 'usage' | 'export'>('cases');
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(null);
  const [caseDetails, setCaseDetails] = useState<any | null>(null);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [rules, setRules] = useState<any[]>([]);
  const [evalContent, setEvalContent] = useState('');
  const [usageContent, setUsageContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [auditRunning, setAuditRunning] = useState(false);

  // Fetch Cases
  const fetchCases = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/cases?search=${encodeURIComponent(search)}&status=${statusFilter}`);
      const data = await res.json();
      setCases(data.cases || []);
      if (data.cases.length > 0 && !selectedCaseId) {
        setSelectedCaseId(data.cases[0].case_id);
      }
    } catch (err) {
      console.error("Failed to fetch cases", err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch Case Details
  const fetchCaseDetails = async (id: string) => {
    try {
      const res = await fetch(`/api/cases/${id}`);
      const data = await res.json();
      setCaseDetails(data);
    } catch (err) {
      console.error("Failed to fetch case details", err);
    }
  };

  // Fetch Rules & Reports
  const fetchReports = async () => {
    try {
      const [rRes, eRes, uRes] = await Promise.all([
        fetch('/api/rules'),
        fetch('/api/evaluation'),
        fetch('/api/usage')
      ]);
      const rData = await rRes.json();
      const eData = await eRes.json();
      const uData = await uRes.json();
      setRules(rData.rules || []);
      setEvalContent(eData.content || '');
      setUsageContent(uData.content || '');
    } catch (err) {
      console.error("Failed to fetch reports", err);
    }
  };

  useEffect(() => {
    fetchCases();
  }, [search, statusFilter]);

  useEffect(() => {
    if (selectedCaseId) {
      fetchCaseDetails(selectedCaseId);
    }
  }, [selectedCaseId]);

  useEffect(() => {
    fetchReports();
  }, []);

  const runBackendAudit = async () => {
    setAuditRunning(true);
    try {
      await fetch('/api/audit/run', { method: 'POST' });
      await fetchCases();
      await fetchReports();
      alert("Backend audit pipeline completed successfully! output.csv updated.");
    } catch (err) {
      alert("Error running backend audit pipeline.");
    } finally {
      setAuditRunning(false);
    }
  };

  // Stats calculation
  const totalCases = 518;
  const completeCount = cases.filter(c => c.deletion_status === 'COMPLETE').length;
  const incompleteCount = cases.filter(c => c.deletion_status === 'INCOMPLETE').length;
  const naCount = cases.filter(c => c.deletion_status === 'NOT_APPLICABLE').length;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col">
      {/* Top Banner */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-sky-500/10 border border-sky-500/30 rounded-xl text-sky-400">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-slate-100 flex items-center gap-2">
                Northstar Deletion Audit Agent
                <span className="text-xs bg-sky-500/20 text-sky-300 border border-sky-500/30 px-2 py-0.5 rounded-full font-mono">
                  v1.0.0
                </span>
              </h1>
              <p className="text-xs text-slate-400">Evidence-Driven Personal Data Compliance & Ghost Data Prevention</p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={runBackendAudit}
              disabled={auditRunning}
              className="flex items-center space-x-2 px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold shadow transition disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5" />
              <span>{auditRunning ? 'Running Audit...' : 'Re-Run Full Audit'}</span>
            </button>
            <a
              href="/api/download/output"
              download
              className="flex items-center space-x-2 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow transition"
            >
              <FileSpreadsheet className="w-3.5 h-3.5" />
              <span>Download output.csv</span>
            </a>
            <a
              href="/api/download/zip"
              download
              className="flex items-center space-x-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-semibold transition"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download code.zip</span>
            </a>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto px-4 flex border-t border-slate-800/60 overflow-x-auto">
          <button
            onClick={() => setActiveTab('cases')}
            className={`flex items-center space-x-2 px-4 py-2.5 text-xs font-medium border-b-2 transition whitespace-nowrap ${
              activeTab === 'cases'
                ? 'border-sky-500 text-sky-400 bg-sky-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Search className="w-4 h-4" />
            <span>Case Investigator</span>
          </button>
          <button
            onClick={() => setActiveTab('rules')}
            className={`flex items-center space-x-2 px-4 py-2.5 text-xs font-medium border-b-2 transition whitespace-nowrap ${
              activeTab === 'rules'
                ? 'border-sky-500 text-sky-400 bg-sky-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Policy Rules</span>
          </button>
          <button
            onClick={() => setActiveTab('eval')}
            className={`flex items-center space-x-2 px-4 py-2.5 text-xs font-medium border-b-2 transition whitespace-nowrap ${
              activeTab === 'eval'
                ? 'border-sky-500 text-sky-400 bg-sky-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>Evaluation & Benchmarks</span>
          </button>
          <button
            onClick={() => setActiveTab('usage')}
            className={`flex items-center space-x-2 px-4 py-2.5 text-xs font-medium border-b-2 transition whitespace-nowrap ${
              activeTab === 'usage'
                ? 'border-sky-500 text-sky-400 bg-sky-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Cpu className="w-4 h-4" />
            <span>Token & Cost Usage</span>
          </button>
          <button
            onClick={() => setActiveTab('export')}
            className={`flex items-center space-x-2 px-4 py-2.5 text-xs font-medium border-b-2 transition whitespace-nowrap ${
              activeTab === 'export'
                ? 'border-sky-500 text-sky-400 bg-sky-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileCode className="w-4 h-4" />
            <span>Submission Hub</span>
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 flex flex-col gap-4">
        {/* Top Summary Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-400 font-medium">Total Dataset Cases</p>
              <p className="text-xl font-bold text-slate-100 font-mono mt-0.5">{totalCases}</p>
            </div>
            <div className="p-2.5 bg-slate-800 rounded-lg text-slate-400">
              <Database className="w-5 h-5" />
            </div>
          </div>

          <div className="bg-emerald-950/20 border border-emerald-500/30 rounded-xl p-3.5 flex items-center justify-between">
            <div>
              <p className="text-xs text-emerald-400 font-medium">Complete Verifications</p>
              <p className="text-xl font-bold text-emerald-300 font-mono mt-0.5">{completeCount}</p>
            </div>
            <div className="p-2.5 bg-emerald-500/10 rounded-lg text-emerald-400">
              <CheckCircle2 className="w-5 h-5" />
            </div>
          </div>

          <div className="bg-amber-950/20 border border-amber-500/30 rounded-xl p-3.5 flex items-center justify-between">
            <div>
              <p className="text-xs text-amber-400 font-medium">Incomplete Remediation</p>
              <p className="text-xl font-bold text-amber-300 font-mono mt-0.5">{incompleteCount}</p>
            </div>
            <div className="p-2.5 bg-amber-500/10 rounded-lg text-amber-400">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-400 font-medium">Not Applicable (Non-Deletion)</p>
              <p className="text-xl font-bold text-slate-300 font-mono mt-0.5">{naCount}</p>
            </div>
            <div className="p-2.5 bg-slate-800 rounded-lg text-slate-400">
              <XCircle className="w-5 h-5" />
            </div>
          </div>
        </div>

        {/* Tab 1: Case Investigator */}
        {activeTab === 'cases' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 flex-1">
            {/* Case List Sidebar */}
            <div className="lg:col-span-5 bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 flex flex-col gap-3">
              <div className="flex flex-col sm:flex-row gap-2">
                <div className="relative flex-1">
                  <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
                  <input
                    type="text"
                    placeholder="Search case_id, email..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-sky-500"
                >
                  <option value="ALL">All Statuses</option>
                  <option value="COMPLETE">COMPLETE</option>
                  <option value="INCOMPLETE">INCOMPLETE</option>
                  <option value="NOT_APPLICABLE">NOT_APPLICABLE</option>
                </select>
              </div>

              <div className="overflow-y-auto max-h-137.5 divide-y divide-slate-800/60 border border-slate-800/80 rounded-lg bg-slate-950/40">
                {loading ? (
                  <div className="p-8 text-center text-xs text-slate-500">Loading cases...</div>
                ) : cases.length === 0 ? (
                  <div className="p-8 text-center text-xs text-slate-500">No cases match filter.</div>
                ) : (
                  cases.map((c) => (
                    <div
                      key={c.case_id}
                      onClick={() => setSelectedCaseId(c.case_id)}
                      className={`p-3 cursor-pointer transition flex items-center justify-between ${
                        selectedCaseId === c.case_id
                          ? 'bg-sky-500/10 border-l-2 border-sky-500'
                          : 'hover:bg-slate-900/60'
                      }`}
                    >
                      <div className="space-y-1">
                        <div className="flex items-center space-x-2">
                          <span className="font-mono font-semibold text-xs text-slate-200">{c.case_id}</span>
                          <span
                            className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${
                              c.deletion_status === 'COMPLETE'
                                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                                : c.deletion_status === 'INCOMPLETE'
                                ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                                : 'bg-slate-800 text-slate-400 border-slate-700'
                            }`}
                          >
                            {c.deletion_status}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 font-mono truncate max-w-55">{c.email}</p>
                      </div>

                      <div className="text-right flex items-center space-x-2">
                        <span className="text-[10px] text-slate-500 font-mono">{c.step_count} steps</span>
                        <ChevronRight className="w-4 h-4 text-slate-600" />
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Case Details Viewer */}
            <div className="lg:col-span-7 bg-slate-900/60 border border-slate-800 rounded-xl p-4 flex flex-col gap-4">
              {caseDetails ? (
                <>
                  <div className="flex items-start justify-between border-b border-slate-800 pb-3">
                    <div>
                      <div className="flex items-center space-x-2">
                        <h2 className="text-base font-bold font-mono text-slate-100">{caseDetails.case_id}</h2>
                        <span
                          className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${
                            caseDetails.deletion_status === 'COMPLETE'
                              ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                              : caseDetails.deletion_status === 'INCOMPLETE'
                              ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                              : 'bg-slate-800 text-slate-400 border-slate-700'
                          }`}
                        >
                          {caseDetails.deletion_status}
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 mt-1">Target Email: <span className="font-mono text-slate-200">{caseDetails.email}</span></p>
                    </div>

                    <div className="text-right text-[11px] text-slate-400 space-y-0.5">
                      <p>Requested: <span className="font-mono text-slate-300">{caseDetails.requested_at}</span></p>
                      <p>Audit Time: <span className="font-mono text-slate-300">{caseDetails.audit_at}</span></p>
                    </div>
                  </div>

                  {/* Request Text */}
                  <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
                    <p className="text-[11px] text-slate-500 uppercase font-semibold tracking-wider mb-1">User Request Text</p>
                    <p className="text-xs text-slate-300 italic">"{caseDetails.request_text}"</p>
                  </div>

                  {/* Resolved Identity */}
                  <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
                    <p className="text-[11px] text-slate-500 uppercase font-semibold tracking-wider mb-2 flex items-center gap-1.5">
                      <UserCheck className="w-3.5 h-3.5 text-sky-400" /> Resolved Identity
                    </p>
                    <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                      <div>
                        <span className="text-slate-500">user_id: </span>
                        <span className="text-sky-300">{caseDetails.identity.user_id}</span>
                      </div>
                      <div>
                        <span className="text-slate-500">email_hash: </span>
                        <span className="text-slate-300 truncate block">{caseDetails.identity.email_hash.substring(0, 16)}...</span>
                      </div>
                    </div>
                  </div>

                  {/* Steps JSON Output Viewer */}
                  <div>
                    <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center justify-between">
                      <span>Ordered Steps JSON ({caseDetails.steps_json.length} steps)</span>
                      <span className="text-[10px] text-slate-500">FINDING &rarr; REMEDIATION &rarr; VERIFICATION</span>
                    </h3>

                    {caseDetails.steps_json.length === 0 ? (
                      <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 text-center text-xs text-slate-500 font-mono">
                        [] (No deletion or remediation authorized for NOT_APPLICABLE)
                      </div>
                    ) : (
                      <div className="space-y-2 max-h-65 overflow-y-auto pr-1">
                        {caseDetails.steps_json.map((step: any) => (
                          <div
                            key={step.step_no}
                            className={`p-3 rounded-lg border text-xs font-mono flex items-center justify-between ${
                              step.phase === 'FINDING'
                                ? 'bg-amber-950/10 border-amber-500/30 text-amber-200'
                                : step.phase === 'REMEDIATION'
                                ? 'bg-sky-950/10 border-sky-500/30 text-sky-200'
                                : 'bg-emerald-950/10 border-emerald-500/30 text-emerald-200'
                            }`}
                          >
                            <div className="space-y-1">
                              <div className="flex items-center space-x-2">
                                <span className="font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-200">
                                  #{step.step_no}
                                </span>
                                <span className="font-semibold text-slate-300">{step.phase}</span>
                                <span className="text-slate-500">&bull;</span>
                                <span className="text-slate-300">{step.operation}</span>
                              </div>
                              <p className="text-[11px] text-slate-400">
                                system: <span className="text-slate-200">{step.system_id}</span> | resource: <span className="text-slate-200">{step.resource_id}</span>
                              </p>
                            </div>

                            <div className="text-right space-y-1">
                              <span className="text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded bg-slate-900 border border-slate-800">
                                {step.state}
                              </span>
                              <p className="text-[10px] text-slate-500">ev_id: "{step.evidence_id}"</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </>
              ) : (
                <div className="p-12 text-center text-slate-500 text-xs">Select a case to inspect evidence.</div>
              )}
            </div>
          </div>
        )}

        {/* Tab 2: Policy Rules */}
        {activeTab === 'rules' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-3">
            <h2 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Layers className="w-4 h-4 text-sky-400" />
              Northstar Personal Data Category & Policy Treatment Matrix (`deletion_rules.csv`)
            </h2>
            <div className="overflow-x-auto border border-slate-800 rounded-lg">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 font-mono text-[11px] border-b border-slate-800">
                  <tr>
                    <th className="p-3">Category</th>
                    <th className="p-3">System ID</th>
                    <th className="p-3">Required Treatment</th>
                    <th className="p-3">Allowed Identifiers</th>
                    <th className="p-3">Retention Period (Days)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {rules.map((r: any, idx: number) => (
                    <tr key={idx} className="hover:bg-slate-900/50">
                      <td className="p-3 text-sky-300 font-semibold">{r.category}</td>
                      <td className="p-3 text-slate-200">{r.system_id}</td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-amber-300 font-semibold text-[10px]">
                          {r.required_treatment}
                        </span>
                      </td>
                      <td className="p-3 text-slate-400">{r.allowed_identifiers}</td>
                      <td className="p-3 text-slate-400">{r.retention_period_days}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab 3: Evaluation Report */}
        {activeTab === 'eval' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-3">
            <h2 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-emerald-400" />
              Evaluation & Benchmark Report (`evaluation/evaluation_report.md`)
            </h2>
            <pre className="bg-slate-950 border border-slate-800 rounded-lg p-4 font-mono text-xs text-slate-300 whitespace-pre-wrap max-h-150 overflow-y-auto">
              {evalContent}
            </pre>
          </div>
        )}

        {/* Tab 4: Usage Report */}
        {activeTab === 'usage' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-3">
            <h2 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-amber-400" />
              Token Usage & Cost Analysis Report (`evaluation/usage_report.md`)
            </h2>
            <pre className="bg-slate-950 border border-slate-800 rounded-lg p-4 font-mono text-xs text-slate-300 whitespace-pre-wrap max-h-150 overflow-y-auto">
              {usageContent}
            </pre>
          </div>
        )}

        {/* Tab 5: Export & Submission */}
        {activeTab === 'export' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6 max-w-3xl mx-auto w-full">
            <div className="space-y-2">
              <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <FileCode className="w-5 h-5 text-sky-400" />
                Submission & Export Package Center
              </h2>
              <p className="text-xs text-slate-400">
                All deliverables required for submission are packaged and verified.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-3 flex flex-col justify-between">
                <div>
                  <div className="flex items-center space-x-2 text-emerald-400 font-semibold text-xs">
                    <FileSpreadsheet className="w-4 h-4" />
                    <span>output.csv</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    Exactly 518 cases sorted by case_id ascending. Formatted as `case_id,deletion_status,steps_json`.
                  </p>
                </div>
                <a
                  href="/api/download/output"
                  download
                  className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold text-center transition flex items-center justify-center space-x-2"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download output.csv</span>
                </a>
              </div>

              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-3 flex flex-col justify-between">
                <div>
                  <div className="flex items-center space-x-2 text-sky-400 font-semibold text-xs">
                    <Download className="w-4 h-4" />
                    <span>code.zip</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    Complete runnable solution ZIP with source code, scripts, prompts, configuration, README, and evaluation folder.
                  </p>
                </div>
                <a
                  href="/api/download/zip"
                  download
                  className="w-full py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold text-center transition flex items-center justify-center space-x-2"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download code.zip</span>
                </a>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
