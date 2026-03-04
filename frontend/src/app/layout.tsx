import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Intelli-RAG Miniproyecto",
  description: "Sistema RAG avanzado con documentos PDF",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="antialiased min-h-screen bg-[var(--color-background)]">
        {children}
      </body>
    </html>
  );
}
