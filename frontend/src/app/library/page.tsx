"use client";
import { useEffect, useState } from "react";
import { fetchDiscourses } from "@/lib/api";
import type { Discourse } from "@/lib/types";

export default function LibraryPage() {
  const [discourses, setDiscourses] = useState<Discourse[]>([]);
  const [volume, setVolume] = useState<number | undefined>();

  useEffect(() => {
    fetchDiscourses({ volume }).then(setDiscourses);
  }, [volume]);

  // Nhóm theo vagga
  const grouped = discourses.reduce((acc, d) => {
    const key = d.vagga || "Other";
    if (!acc[key]) acc[key] = [];
    acc[key].push(d);
    return acc;
  }, {} as Record<string, Discourse[]>);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Library</h1>

      {/* Volume filter */}
      <div className="flex gap-2 mb-6">
        {[undefined, 1, 2, 3].map((v) => (
          <button key={String(v)} onClick={() => setVolume(v)}
            className={`px-4 py-1.5 rounded-full text-sm border ${
              volume === v ? "bg-amber-700 text-white border-amber-700" : "border-stone-300 hover:bg-stone-100"
            }`}>
            {v ? `Volume ${v}` : "All"}
          </button>
        ))}
      </div>

      {/* Grouped by vagga */}
      {Object.entries(grouped).map(([vagga, items]) => (
        <div key={vagga} className="mb-8">
          <h2 className="text-sm font-semibold text-stone-400 uppercase tracking-wide mb-3">{vagga}</h2>
          <div className="space-y-1">
            {items.map((d) => (
              <a key={d.mn_number} href={`/discourse/${d.mn_number}`}
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-stone-100">
                <span className="text-xs text-stone-400 w-12">MN {d.mn_number}</span>
                <span className="font-medium">{d.title_en}</span>
                <span className="text-stone-400 text-sm italic">{d.title_pali}</span>
              </a>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
