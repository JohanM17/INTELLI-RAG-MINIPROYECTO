"use client";

import { useState } from "react";
import { uploadDocument } from "@/lib/api";

export default function UploadArea() {
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
        if (!e.target.files || e.target.files.length === 0) return;
        const file = e.target.files[0];

        // Reestablece estados de la interfaz
        setLoading(true);
        setSuccess(null);
        setError(null);

        try {
            const res = await uploadDocument(file);
            setSuccess(`¡Procesado! (${res.chunks_created} fragmentos generados)`);
            // Limpia el input de archivos
            e.target.value = '';

            // Remueve mensaje de éxito tras temporizador de 5s
            setTimeout(() => {
                setSuccess(null);
            }, 5000);

        } catch (err: any) {
            setError(err.message || "Error al subir el archivo.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="glass-panel rounded-2xl p-6 flex flex-col shadow-xl">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                Ingesta de Datos
            </h2>

            <div className="relative border-2 border-dashed border-[var(--color-border)] hover:border-emerald-500 transition-colors rounded-xl p-8 flex flex-col items-center justify-center text-center group bg-[#0f172a]/40">
                <input
                    type="file"
                    accept=".pdf"
                    onChange={handleUpload}
                    disabled={loading}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
                />

                <div className="bg-[var(--color-surface)] p-3 rounded-full mb-3 group-hover:bg-emerald-500/20 transition-colors">
                    <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                </div>
                <p className="font-medium text-[var(--color-text-main)]">
                    {loading ? "Procesando PDF..." : "Haz clic o arrastra un PDF aquí"}
                </p>
                <p className="text-xs text-[var(--color-text-muted)] mt-1">
                    Solo archivos .pdf soportados
                </p>
            </div>

            {/* Alertas de Feedback */}
            {success && (
                <div className="mt-4 p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                    {success}
                </div>
            )}

            {error && (
                <div className="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    {error}
                </div>
            )}
        </div>
    );
}
