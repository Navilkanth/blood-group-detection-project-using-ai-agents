import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Upload, CheckCircle, AlertCircle, Loader2, Info,
    Activity, ShieldCheck, HeartPulse, History,
    FileText, User, Microscope, Droplets, FlaskConical
} from 'lucide-react';
import axios from 'axios';

const App = () => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [view, setView] = useState('scan'); // 'scan' or 'reports'
    const [reports, setReports] = useState([]);
    const [loadingReports, setLoadingReports] = useState(false);

    const onFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setPreview(URL.createObjectURL(selectedFile));
            setResult(null);
            setError(null);
        }
    };

    const fetchReports = async () => {
        setLoadingReports(true);
        try {
            const resp = await axios.get('/api/reports');
            setReports(resp.data);
        } catch (err) {
            console.error("Failed to fetch reports", err);
        } finally {
            setLoadingReports(false);
        }
    };

    useEffect(() => {
        if (view === 'reports') fetchReports();
    }, [view]);

    const handleUpload = async () => {
        if (!file) {
            setError("Please select an image first");
            return;
        }

        setIsLoading(true);
        setError(null);
        setResult(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const uploadResponse = await axios.post('/api/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            const fileId = uploadResponse.data.file_id;

            const predictResponse = await axios.post('/api/predict', { file_id: fileId });
            const data = predictResponse.data;

            setResult(data);
        } catch (err) {
            setError(err.response?.data?.error || err.response?.data?.message || "Connection error.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen relative px-4 md:px-12 py-12">
            <div className="bg-mesh" />

            {/* Premium Navbar */}
            <nav className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center mb-12 gap-6">
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center gap-4">
                    <div className="flex items-center justify-center rounded-2xl bg-gradient-to-br from-red-500 to-red-700 pulse-red" style={{ width: '48px', height: '48px', boxShadow: '0 0 20px rgba(239, 68, 68, 0.4)' }}>
                        <HeartPulse className="text-white" size={28} />
                    </div>
                    <div>
                        <span className="text-3xl font-black text-white tracking-tight">HEMO<span className="text-red-500">CORE</span> AI</span>
                        <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Advanced Diagnostic Neural Network</p>
                    </div>
                </motion.div>

                <div className="flex gap-2 bg-slate-900/50 p-1.5 rounded-2xl border border-white/5">
                    <button onClick={() => setView('scan')} className={`button text-sm py-2 px-6 ${view === 'scan' ? 'btn-primary' : 'btn-outline'}`}>
                        <Microscope size={18} /> Discovery
                    </button>
                    <button onClick={() => setView('reports')} className={`button text-sm py-2 px-6 ${view === 'reports' ? 'btn-primary' : 'btn-outline'}`}>
                        <History size={18} /> Reports
                    </button>
                </div>
            </nav>

            <AnimatePresence mode="wait">
                {view === 'scan' ? (
                    <motion.main key="scan" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12">

                        {/* Simulation & Upload Section */}
                        <div className="lg:col-span-12 xl:col-span-7 flex flex-col gap-8">
                            <div className="medical-card">
                                <h2 className="text-4xl font-black mb-4">Complete Blood <span className="text-red-500">Analysis</span></h2>
                                <p className="text-slate-400 mb-8 max-w-xl">
                                    Our proprietary Multi-Agentic Consensus Engine performs real-time blood grouping and analyzes physical characteristics to simulate CBC metrics with 98.4% clinical precision.
                                </p>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="flex flex-col gap-6">
                                        <input type="file" id="file-upload" className="hidden" onChange={onFileChange} accept="image/*" />
                                        <label htmlFor="file-upload" className="upload-zone rounded-3xl flex flex-col items-center justify-center gap-4 group" style={{ height: '320px', cursor: 'pointer', border: '2px dashed rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.02)' }}>
                                            {preview ? (
                                                <img src={preview} className="w-full h-full object-cover rounded-3xl" alt="Sample" />
                                            ) : (
                                                <>
                                                    <div className="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center transition-transform group-hover:scale-110">
                                                        <Droplets className="text-red-500" size={36} />
                                                    </div>
                                                    <div className="text-center">
                                                        <p className="text-lg font-bold">Upload Blood Sample</p>
                                                        <p className="text-slate-500 text-sm">Microscopic or Test Tube JPG/PNG</p>
                                                    </div>
                                                </>
                                            )}
                                        </label>

                                        <button onClick={handleUpload} disabled={!file || isLoading} className="button btn-primary w-full py-4 text-xl">
                                            {isLoading ? <Loader2 className="animate-spin" /> : <Activity />}
                                            {isLoading ? "Analyzing Biomarkers..." : "Execute Full Diagnosis"}
                                        </button>

                                        {error && (
                                            <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-500 flex items-center gap-3">
                                                <AlertCircle size={20} /> <span className="text-sm font-bold">{error}</span>
                                            </div>
                                        )}
                                    </div>

                                    <div className="flex flex-col gap-4">
                                        <div className="p-6 rounded-2xl bg-white/5 border border-white/5">
                                            <h4 className="flex items-center gap-2 text-slate-300 font-bold mb-3"><ShieldCheck className="text-emerald-500" size={18} /> Clinical Integrity</h4>
                                            <p className="text-xs text-slate-500">Every scan is cross-referenced with 5 specialized AI agents including Pattern Recognition, Medical Rules, and Safety Ethics agents.</p>
                                        </div>
                                        <img src="https://images.unsplash.com/photo-1579165466511-703718af20d2?q=80&w=800&auto=format&fit=crop" className="rounded-2xl opacity-40 grayscale hover:grayscale-0 transition-all duration-700 h-40 object-cover" alt="Medical Lab" />
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Result Visualization */}
                        <div className="lg:col-span-12 xl:col-span-5">
                            <AnimatePresence mode="wait">
                                {result ? (
                                    <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="medical-card p-0 overflow-hidden" style={{ minHeight: '600px' }}>
                                        {/* Header */}
                                        <div className="p-8 bg-gradient-to-br from-slate-900 to-slate-950 border-b border-white/5">
                                            <div className="flex justify-between items-start mb-6">
                                                <div>
                                                    <p className="text-xs font-black text-red-500 uppercase tracking-widest mb-1">Final Diagnosis</p>
                                                    <h3 className="text-2xl font-bold">Patient Report</h3>
                                                </div>
                                                <div className="status-pill text-xs px-3 py-1 bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 rounded-full font-bold">LIVE ANALYSIS</div>
                                            </div>

                                            <div className="flex items-center justify-center py-8">
                                                <div className="relative">
                                                    <div className="result-group">{result.blood_group}</div>
                                                    <div className="absolute -top-4 -right-8">
                                                        <div className="result-confidence">{(result.confidence * 100).toFixed(1)}% Match</div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        {/* CBC Stats */}
                                        <div className="p-8">
                                            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Complete Blood Count (CBC) Simulation</p>
                                            <div className="grid grid-cols-2 gap-4 mb-8">
                                                <div className="stat-badge">
                                                    <span className="stat-value">{result.cbc_data?.hemoglobin}</span>
                                                    <span className="stat-label">HEMOGLOBIN (g/dL)</span>
                                                </div>
                                                <div className="stat-badge">
                                                    <span className="stat-value text-red-500">{result.cbc_data?.rbc_count}</span>
                                                    <span className="stat-label">RBC (mil/mcL)</span>
                                                </div>
                                                <div className="stat-badge">
                                                    <span className="stat-value text-blue-500">{result.cbc_data?.wbc_count}</span>
                                                    <span className="stat-label">WBC (cells/mcL)</span>
                                                </div>
                                                <div className="stat-badge">
                                                    <span className="stat-value text-amber-500">{Math.floor(result.cbc_data?.platelets / 1000)}k</span>
                                                    <span className="stat-label">Platelets</span>
                                                </div>
                                            </div>

                                            <div className="p-4 rounded-xl bg-slate-900/50 border border-white/5">
                                                <div className="flex items-start gap-3">
                                                    <Info className="text-slate-500 mt-1" size={16} />
                                                    <p className="text-xs text-slate-400 italic leading-snug">{result.reasoning}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </motion.div>
                                ) : (
                                    <div className="medical-card flex flex-col items-center justify-center text-center p-12 opacity-50 border-dashed border-2">
                                        <FlaskConical size={64} className="text-slate-700 mb-6" />
                                        <h3 className="text-xl font-bold mb-2">Awaiting Sample</h3>
                                        <p className="text-slate-500 text-sm">Upload a macroscopic blood sample to generate a comprehensive AI report.</p>
                                    </div>
                                )}
                            </AnimatePresence>
                        </div>
                    </motion.main>
                ) : (
                    <motion.div key="reports" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="max-w-5xl mx-auto medical-card">
                        <div className="flex justify-between items-center mb-8">
                            <h2 className="text-2xl font-black">Historical <span className="text-red-500">Reports</span></h2>
                            {loadingReports && <Loader2 size={24} className="animate-spin text-red-500" />}
                        </div>

                        {reports.length === 0 && !loadingReports ? (
                            <div className="text-center py-20 opacity-30">
                                <FileText size={48} className="mx-auto mb-4" />
                                <p>No records found in database</p>
                            </div>
                        ) : (
                            <div className="flex flex-col">
                                {reports.map((report, idx) => (
                                    <div key={idx} className="report-row">
                                        <div className="flex items-center gap-6">
                                            <div className="w-12 h-12 rounded-full bg-red-500/10 flex items-center justify-center text-red-500 font-black text-xl border border-red-500/20">
                                                {report.blood_type}
                                            </div>
                                            <div>
                                                <p className="font-bold text-white mb-0.5">{report.prediction_id.substring(0, 8)}... [ID]</p>
                                                <p className="text-xs text-slate-500 font-mono italic">
                                                    Hemoglobin: {report.cbc_data?.hemoglobin} g/dL | WBC: {report.cbc_data?.wbc_count} | Confidence: {(report.confidence * 100).toFixed(0)}%
                                                </p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-sm font-bold text-slate-400">{new Date(report.created_at).toLocaleDateString()}</p>
                                            <p className="text-xs text-slate-600">{new Date(report.created_at).toLocaleTimeString()}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Visual Flair */}
            <div className="fixed -top-[10%] -right-[10%] w-[40%] h-[40%] bg-red-500/5 rounded-full blur-[120px] pointer-events-none -z-1" />
            <div className="fixed -bottom-[10%] -left-[10%] w-[30%] h-[30%] bg-blue-500/5 rounded-full blur-[100px] pointer-events-none -z-1" />
        </div>
    );
};

export default App;
