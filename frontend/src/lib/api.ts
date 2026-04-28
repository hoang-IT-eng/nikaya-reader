const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchDiscourses(params?: { volume?: number; vagga?: string }) {
  const query = new URLSearchParams();
  if (params?.volume) query.set("volume", String(params.volume));
  if (params?.vagga)  query.set("vagga", params.vagga);
  const res = await fetch(`${BASE_URL}/discourses?${query}`);
  return res.json();
}

export async function fetchDiscourse(mnNumber: number) {
  const res = await fetch(`${BASE_URL}/discourses/${mnNumber}`);
  if (!res.ok) throw new Error("Not found");
  return res.json();
}

export async function searchDiscourses(q: string) {
  const res = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(q)}`);
  return res.json();
}

export async function fetchBookmarks() {
  const res = await fetch(`${BASE_URL}/bookmarks`);
  return res.json();
}

export async function addBookmark(mn_number: number, note = "") {
  const res = await fetch(`${BASE_URL}/bookmarks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mn_number, note }),
  });
  return res.json();
}

export async function deleteBookmark(id: number) {
  await fetch(`${BASE_URL}/bookmarks/${id}`, { method: "DELETE" });
}
