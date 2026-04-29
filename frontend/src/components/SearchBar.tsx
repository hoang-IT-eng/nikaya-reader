"use client";
import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";

interface SearchBarProps {
  defaultValue?: string;
  onSearch?: (q: string) => void;
  /** If true, navigates to /search?q=... instead of calling onSearch */
  navigate?: boolean;
}

export default function SearchBar({ defaultValue = "", onSearch, navigate = false }: SearchBarProps) {
  const [query, setQuery] = useState(defaultValue);
  const router = useRouter();

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    if (navigate) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    } else {
      onSearch?.(query.trim());
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search suttas — mindfulness, right view, craving..."
        className="flex-1 border border-stone-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-amber-600 bg-white"
      />
      <button
        type="submit"
        className="bg-amber-700 text-white px-6 py-2 rounded-lg hover:bg-amber-800 transition-colors"
      >
        Search
      </button>
    </form>
  );
}
