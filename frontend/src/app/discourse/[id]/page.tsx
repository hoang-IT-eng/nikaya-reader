"use client";
import { useEffect, useState } from "react";
import { fetchDiscourse, addBookmark } from "@/lib/api";
import type { Discourse } from "@/lib/types";

export default function DiscoursePage({ params }: { params: { id: string } }) {
  const [discourse, setDiscourse] = useState<Discourse | null>(null);
  const [bookmarked, setBookmarked] = useState(false);

  useEffect(() => {
    fetchDiscourse(Number(params.id)).then(setDiscourse);
  }, [params.id]);

  if (!discourse) return <div className="text-stone-400">Loading...</div>;

  const paragraphs = discourse.full_text?.split("\n\n").filter(Boolean) || [];

  return (
    <div className="max-w-2xl">
      {/* Header */}
      <div className="mb-8">
        <p className="text-sm text-stone-400 mb-1">MN {discourse.mn_number} · Volume {discourse.volume}</p>
        <h1 className="text-2xl font-bold mb-1">{discourse.title_en}</h1>
        <p className="text-stone-500 italic">{discourse.title_pali}</p>
        <p className="text-xs text-stone-400 mt-1">{discourse.vagga}</p>
      </div>

      {/* Bookmark */}
      <button onClick={async () => {
          await addBookmark(discourse.mn_number);
          setBookmarked(true);
        }}
        className={`mb-8 px-4 py-1.5 rounded-full text-sm border ${
          bookmarked ? "bg-amber-700 text-white border-amber-700" : "border-stone-300 hover:bg-stone-100"
        }`}>
        {bookmarked ? "Bookmarked" : "Bookmark"}
      </button>

      {/* Content */}
      <div className="prose prose-stone max-w-none">
        {paragraphs.map((p, i) => (
          <p key={i} className="mb-4 leading-relaxed">{p}</p>
        ))}
      </div>

      {/* Citation */}
      <div className="mt-12 pt-6 border-t border-stone-200 text-xs text-stone-400">
        Source: Middle Discourses (Majjhima Nikāya), Bhikkhu Sujato · MN {discourse.mn_number} · Volume {discourse.volume}
      </div>
    </div>
  );
}
