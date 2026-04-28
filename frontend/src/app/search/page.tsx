"use client";
import { useState } from "react";
import { searchDiscourses } from "@/lib/api";
import type { SearchResult } from "@/lib/types";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    const data = await searchDiscourses(query);
    setResults(data);
    setLoading(false);
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Search</h1>

      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <input value={query} onChange={(e) => setQuery(e.target.value)}
          placeholder="mindfulness, right view, craving..."
          className="flex-1 border border-stone-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-amber-600"
        />
        <button type="submit"
          className="bg-amber-700 text-white px-6 py-2 rounded-lg hover:bg-amber-800">
          {loading ? "..." : "Search"}
        </button>
      </form>

      <div className="space-y-3">
        {results.map((r) => (
          <a key={r.mn_number} href={`/discourse/${r.mn_number}`}
            className="block p-4 border border-stone-200 rounded-lg hover:bg-stone-50">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs text-stone-400">MN {r.mn_number}</span>
              <span className="text-xs text-stone-300">·</span>
              <span className="text-xs text-stone-400">Vol {r.volume}</span>
            </div>
            <p className="font-medium">{r.title_en}</p>
            <p className="text-sm text-stone-400 italic">{r.title_pali}</p>
          </a>
        ))}
        {results.length === 0 && query && !loading && (
          <p className="text-stone-400">No results for "{query}"</p>
        )}
      </div>
    </div>
  );
}
