"use client";
import { useEffect, useState } from "react";
import { fetchDiscourses } from "@/lib/api";
import type { Discourse } from "@/lib/types";
import DiscourseList from "@/components/DiscourseList";

export default function LibraryPage() {
  const [discourses, setDiscourses] = useState<Discourse[]>([]);
  const [volume, setVolume] = useState<number | undefined>();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchDiscourses({ volume }).then((data) => {
      setDiscourses(data);
      setLoading(false);
    });
  }, [volume]);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Library</h1>
      <p className="text-stone-500 mb-6">152 suttas · Majjhima Nikāya · Bhikkhu Sujato</p>

      {/* Volume filter */}
      <div className="flex gap-2 mb-8">
        {([undefined, 1, 2, 3] as const).map((v) => (
          <button
            key={String(v)}
            onClick={() => setVolume(v)}
            className={`px-4 py-1.5 rounded-full text-sm border transition-colors ${
              volume === v
                ? "bg-amber-700 text-white border-amber-700"
                : "border-stone-300 hover:bg-stone-100"
            }`}
          >
            {v ? `Volume ${v}` : "All"}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-2">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-10 bg-stone-100 rounded-lg animate-pulse" />
          ))}
        </div>
      ) : discourses.length === 0 ? (
        <p className="text-stone-400">No discourses found.</p>
      ) : (
        <DiscourseList discourses={discourses} grouped />
      )}
    </div>
  );
}
