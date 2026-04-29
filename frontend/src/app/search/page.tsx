"use client";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { searchDiscourses } from "@/lib/api";
import type { SearchResult } from "@/lib/types";
import SearchBar from "@/components/SearchBar";
import Link from "next/link";

export default function SearchPage() {
  const searchParams = useSearchParams();
  const initialQ = searchParams.get("q") ?? "";

  const [query, setQuery] = useState(initialQ);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function handleSearch(q: string) {
    setQuery(q);
    setLoading(true);
    setSearched(true);
    const data = await searchDiscourses(q);
    setResults(data);
    setLoading(false);
  }

  // Run search if URL has ?q=
  useEffect(() => {
    if (initialQ) handleSearch(initialQ);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Search</h1>

      <div className="mb-8">
        <SearchBar defaultValue={initialQ} onSearch={handleSearch} />
      </div>

      {loading && (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-16 bg-stone-100 rounded-lg animate-pulse" />
          ))}
        </div>
      )}

      {!loading && searched && results.length === 0 && (
        <p className="text-stone-400">No results for &ldquo;{query}&rdquo;</p>
      )}

      {!loading && results.length > 0 && (
        <>
          <p className="text-sm text-stone-400 mb-4">{results.length} results</p>
          <div className="space-y-2">
            {results.map((r) => (
              <Link
                key={r.mn_number}
                href={`/discourse/${r.mn_number}`}
                className="block p-4 border border-stone-200 rounded-lg hover:bg-stone-50 transition-colors"
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs text-stone-400">MN {r.mn_number}</span>
                  <span className="text-xs text-stone-300">·</span>
                  <span className="text-xs text-stone-400">Vol {r.volume}</span>
                  {r.vagga && (
                    <>
                      <span className="text-xs text-stone-300">·</span>
                      <span className="text-xs text-stone-400">{r.vagga}</span>
                    </>
                  )}
                </div>
                <p className="font-medium text-stone-900">{r.title_en}</p>
                {r.title_pali && (
                  <p className="text-sm text-stone-400 italic">{r.title_pali}</p>
                )}
              </Link>
            ))}
          </div>
        </>
      )}

      {!searched && (
        <div className="text-center py-12 text-stone-400">
          <p className="mb-2">Try searching for:</p>
          <div className="flex flex-wrap gap-2 justify-center">
            {["mindfulness", "right view", "craving", "nibbana", "four noble truths", "breath"].map((term) => (
              <button
                key={term}
                onClick={() => handleSearch(term)}
                className="px-3 py-1 rounded-full border border-stone-200 text-sm hover:bg-stone-100 transition-colors"
              >
                {term}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
