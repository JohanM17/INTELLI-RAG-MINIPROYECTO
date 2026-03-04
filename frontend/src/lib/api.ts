const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"

export async function uploadDocument(file: File) {
    const formData = new FormData()
    formData.append("file", file)

    const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData
    })

    if (!response.ok) throw new Error("Error al subir el documento")
    return response.json()
}

export async function askQuestion(question: string) {
    const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
    })

    if (!res.ok) throw new Error("Error en la respuesta de IA")
    const data = await res.json()
    return data.answer
}

export async function resetSystem() {
    const res = await fetch(`${API_URL}/reset`, {
        method: "DELETE"
    })
    if (!res.ok) throw new Error("Error al reiniciar la base de datos")
}

export async function getDocuments() {
    const res = await fetch(`${API_URL}/documents`, {
        method: "GET"
    })
    if (!res.ok) throw new Error("Error fetching documents")
    return res.json()
}

export async function deleteDocument(id: string) {
    const res = await fetch(`${API_URL}/document/${id}`, {
        method: "DELETE"
    })
    if (!res.ok) throw new Error("Error deleting document")
    return res.json()
}
