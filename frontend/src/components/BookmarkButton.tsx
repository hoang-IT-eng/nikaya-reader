"use client";
import { useState } from "react";
import { addBookmark, deleteBookmark } from "@/lib/api";
import type { Bookmark } from "@/lib/types";

interface BookmarkButtonProps {
  mnNumber: number;
  existing?: Bookmark | null;
}

export default function BookmarkButton({ mnNumber, existing }: BookmarkButtonProps) {
  const [bookmark, setBookmark] = useState<Bookmark | null>(existing ?? null);
  const [note, setNote] = useState("");
  const [showNote, setShowNote] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleAdd() {
    setLoading(true);
    const bm = await addBookmark(mnNumber, note);
    setBookmark(bm);
    setShowNote(false);
    setNote("");
    setLoading(false);
  }

  async function handleRemove() {
    if (!bookmark) return;
    setLoading(true);
    await deleteBookmark(bookmark.id);
    setBookmark(null);
    setLoading(false);
  }

  if (bookmark) {
    return (
      <div className="flex items-center gap-2">
        <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm bg-amber-100 text-amber-800 border border-amber-200">
          <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
          </svg>
          Bookmarked
        </span>
        <button
          onClick={handleRemove}
          disabled={loading}
          className="text-xs text-stone-400 hover:text-red-500 transition-colors"
        >
          Remove
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {showNote ? (
        <div className="flex gap-2 items-center">
          <input
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Add a note (optional)"
            className="border border-stone-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-amber-600"
          />
          <button
            onClick={handleAdd}
            disabled={loading}
            className="bg-amber-700 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-amber-800 transition-colors"
          >
            {loading ? "..." : "Save"}
          </button>
          <button
            onClick={() => setShowNote(false)}
            className="text-sm text-stone-400 hover:text-stone-600"
          >
            Cancel
          </button>
        </div>
      ) : (
        <button
          onClick={() => setShowNote(true)}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm border border-stone-300 hover:bg-stone-100 transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
          </svg>
          Bookmark
        </button>
      )}
    </div>
  );
}
