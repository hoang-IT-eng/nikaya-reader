"use client";
import { useEffect, useState } from "react";
import { fetchBookmarks, deleteBookmark } from "@/lib/api";
import type { Bookmark } from "@/lib/types";
import Link from "next/link";

export default function BookmarksPage() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBookmarks().then((data) => {
      setBookmarks(data);
      setLoading(false);
    });
  }, []);

  async function handleDelete(id: number) {
    await deleteBookmark(id);
    setBookmarks((prev) => prev.filter((b) => b.id !== id));
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Bookmarks</h1>

      {loading && (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-16 bg-stone-100 rounded-lg animate-pulse" />
          ))}
        </div>
      )}

      {!loading && bookmarks.length === 0 && (
        <div className="text-center py-12 text-stone-400">
          <p className="mb-4">No bookmarks yet.</p>
          <Link href="/library" className="text-amber-700 hover:underline">
            Browse the library →
          </Link>
        </div>
      )}

      {!loading && bookmarks.length > 0 && (
        <div className="space-y-2">
          {bookmarks.map((b) => (
            <div
              key={b.id}
              className="flex items-start gap-4 p-4 border border-stone-200 rounded-lg hover:bg-stone-50 transition-colors"
            >
              <Link href={`/discourse/${b.mn_number}`} className="flex-1 min-w-0">
                <p className="font-medium text-stone-900">MN {b.mn_number}</p>
                {b.note && (
                  <p className="text-sm text-stone-500 mt-0.5 truncate">{b.note}</p>
                )}
                <p className="text-xs text-stone-400 mt-1">
                  {new Date(b.created_at).toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                  })}
                </p>
              </Link>
              <button
                onClick={() => handleDelete(b.id)}
                className="text-stone-300 hover:text-red-400 transition-colors shrink-0"
                aria-label="Remove bookmark"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
