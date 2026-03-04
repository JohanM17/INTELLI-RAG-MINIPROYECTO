"use client";

import { useState, useRef, useEffect } from "react";
import { askQuestion } from "@/lib/api";

type Message = {
    role: "user" | "ai";
    content: string;
};

export default function ChatBox() {
    const [query, setQuery] = useState("");
    const [messages, setMessages] = useState<Message[]>([
        {
            role: "ai",
            content: "¡Hola! Soy el asistente RAG del sistema (Tema Matrix activado). Hazme una pregunta sobre los documentos que has procesado y te responderé usando únicamente esa información."
        }
    ]);
    const [loading, setLoading] = useState(false);
    const endOfMessagesRef = useRef<HTMLDivElement>(null);

    // Scroll automático al recibir nuevos mensajes
    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, loading]);

    async function handleSend() {
        if (!query.trim()) return;

        // Registro de la entrada del usuario en la vista
        const userMsg = query;
        setMessages(prev => [...prev, { role: "user", content: userMsg }]);
        setQuery("");
        setLoading(true);

        try {
            // Consulta al orquestador RAG
            const answer = await askQuestion(userMsg);
            setMessages(prev => [...prev, { role: "ai", content: answer }]);
        } catch (e: any) {
            setMessages(prev => [...prev, { role: "ai", content: "❌ Ocurrió un error al contactar con el orquestador RAG." }]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="glass-panel rounded-2xl shadow-xl flex flex-col h-full border border-[var(--color-border)] overflow-hidden">

            {/* Cabecera del Chat */}
            <div className="bg-[var(--color-surface)]/50 border-b border-[var(--color-border)] p-4 flex items-center gap-3">
                <div className="relative">
                    <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center border border-emerald-500/30">
                        <svg className="w-5 h-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                    </div>
                    <span className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-[var(--color-background)] rounded-full"></span>
                </div>
                <div>
                    <h2 className="font-semibold text-sm">Asistente Inteligente (Cohere)</h2>
                    <p className="text-xs text-[var(--color-text-muted)]">Basado en tu base vectorial local</p>
                </div>
            </div>

            {/* Visualización de la conversación */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                        <div className={`max-w-[85%] rounded-2xl px-5 py-3 ${msg.role === "user"
                            ? "bg-emerald-600 text-white rounded-br-sm shadow-md"
                            : "bg-[var(--color-surface)] border border-[var(--color-border)] text-[var(--color-text-main)] rounded-bl-sm shadow-sm"
                            }`}>
                            <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl rounded-bl-sm px-5 py-4 flex gap-2 shadow-sm">
                            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-bounce"></div>
                            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                        </div>
                    </div>
                )}
                <div ref={endOfMessagesRef} />
            </div>

            {/* Control de entrada de texto */}
            <div className="p-4 bg-[var(--color-surface)]/30 border-t border-[var(--color-border)]">
                <div className="relative flex items-center">
                    <input
                        className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] text-white placeholder-[var(--color-text-muted)] rounded-xl py-4 pl-4 pr-14 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all shadow-inner"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        placeholder="Pregunta algo sobre tus documentos..."
                        onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
                    />
                    <button
                        onClick={handleSend}
                        disabled={loading || !query.trim()}
                        className="absolute right-2 p-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition-colors disabled:opacity-50 disabled:hover:bg-emerald-600 flex items-center justify-center"
                    >
                        <svg className="w-5 h-5 translate-x-px translate-y-px" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                    </button>
                </div>
                <p className="text-center text-[10px] text-[var(--color-text-muted)] mt-2">
                    La IA responde basada en contexto semántico. No inventa datos.
                </p>
            </div>

        </div>
    );
}
