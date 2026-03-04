import UploadArea from "@/components/upload/UploadArea";
import ChatBox from "@/components/chat/ChatBox";
import DocumentList from "@/components/documents/DocumentList";

export default function Home() {
  return (
    <div className="flex flex-col h-screen overflow-hidden p-4 md:p-6 gap-6 relative">
      {/* Elementos visuales de fondo */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-emerald-600/20 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-green-600/20 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Header */}
      <header className="flex items-center justify-between z-10 px-2">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center shadow-lg shadow-emerald-500/30">
            <span className="text-white font-bold text-xl">IR</span>
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-wide">Intelli-RAG</h1>
            <p className="text-xs text-[var(--color-text-muted)]">Panel de Control Inteligente</p>
          </div>
        </div>
      </header>

      {/* Main Content Layout */}
      <main className="flex-1 flex flex-col lg:flex-row gap-6 z-10 min-h-0">

        {/* Panel Izquierdo (Gestión) */}
        <div className="w-full lg:w-1/3 flex flex-col gap-6 min-h-0 overflow-y-auto pr-2 pb-2">
          <UploadArea />
          <DocumentList />
        </div>

        {/* Panel Derecho (Chat) */}
        <div className="flex-1 min-h-0 flex flex-col">
          <ChatBox />
        </div>

      </main>
    </div>
  );
}
