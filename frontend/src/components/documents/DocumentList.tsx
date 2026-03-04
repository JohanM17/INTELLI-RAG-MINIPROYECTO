"use client";

import { useState, useEffect } from "react";
import { resetSystem, getDocuments, deleteDocument } from "@/lib/api";

type Doc = {
    document_id: string;
    filename: string;
    upload_timestamp: string;
};

export default function DocumentList() {
    const [loading, setLoading] = useState(false);
    const [docs, setDocs] = useState<Doc[]>([]);

    useEffect(() => {
        fetchDocs();

        // Polling para actualización automática de la lista de documentos
        const interval = setInterval(fetchDocs, 5000);
        return () => clearInterval(interval);
    }, []);

    async function fetchDocs() {
        try {
            const data = await getDocuments();
            setDocs(data);
        } catch (e) {
            console.error("No se pudieron cargar los documentos.");
        }
    }

    async function handleDeleteDoc(id: string) {
        if (!window.confirm("¿Estás seguro de que deseas eliminar este documento de la IA?")) return;
        setLoading(true);
        try {
            await deleteDocument(id);
            setDocs(prev => prev.filter(d => d.document_id !== id));
        } catch (e) {
            alert("Error al borrar el documento.");
        } finally {
            setLoading(false);
        }
    }

    async function handleReset() {
        if (!window.confirm("¿Estás seguro de que deseas VACIAR completamente la base de datos? Esto eliminará todos los documentos indexados.")) {
            return;
        }

        setLoading(true);
        try {
            await resetSystem();
            alert("¡La base de datos vectorial ha sido reiniciada con éxito!");
            setDocs([]);
        } catch (err) {
            alert("Ocurrió un error al intentar vaciar la base de datos.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="glass-panel rounded-2xl p-6 shadow-xl flex-1 flex flex-col">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                Gestor de Base Vectorial
            </h2>

            <div className="flex-1 flex flex-col overflow-y-auto mb-4 border border-[var(--color-border)] rounded-xl bg-slate-900/40 p-2">
                {docs.length === 0 ? (
                    <div className="flex-1 flex flex-col items-center justify-center text-center p-6 opacity-70">
                        <svg className="w-10 h-10 text-emerald-400/50 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        <p className="text-sm text-[var(--color-text-muted)]">
                            Base de datos limpia.<br />No hay documentos indexados.
                        </p>
                    </div>
                ) : (
                    <ul className="space-y-2">
                        {docs.map(doc => (
                            <li key={doc.document_id} className="flex items-center justify-between p-3 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg hover:border-emerald-500/30 transition-colors">
                                <div className="flex items-center gap-3 overflow-hidden">
                                    <svg className="w-8 h-8 flex-shrink-0 text-emerald-500" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd"></path></svg>
                                    <div className="flex flex-col overflow-hidden">
                                        <span className="text-sm font-medium truncate" title={doc.filename}>{doc.filename}</span>
                                        <span className="text-[10px] text-[var(--color-text-muted)]">ID: {doc.document_id.split('-')[0]}...</span>
                                    </div>
                                </div>
                                <button
                                    onClick={() => handleDeleteDoc(doc.document_id)}
                                    disabled={loading}
                                    className="p-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors"
                                    title="Eliminar este PDF"
                                >
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            <button
                onClick={handleReset}
                disabled={loading || docs.length === 0}
                className="w-full py-3 px-4 bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/30 rounded-xl font-medium transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                {loading ? "Vaciando..." : "Vaciar Base de Datos"}
            </button>
        </div>
    );
}
