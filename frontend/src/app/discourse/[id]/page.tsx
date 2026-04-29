"use client";
import { useEffect, useState } from "react";
import { fetchDiscourse } from "@/lib/api";
import type { Discourse } from "@/lib/types";
import DiscourseReader from "@/components/DiscourseReader";

export default function DiscoursePage({ params }: { params: { id: string } }) {
  const [discourse, setDiscourse] = useState<Discourse | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetchDiscourse(Number(params.id))
      .then(setDiscourse)
      .catch(() => setError(true));
  }, [params.id]);

  if (error) {
    return (
      <div className="text-center py-16">
        <p className="text-stone-400 mb-4">MN {params.id} not found.</p>
        <a href="/library" className="text-amber-700 hover:underline">← Back to Library</a>
      </div>
    );
  }

  if (!discourse) {
    return (
      <div className="max-w-2xl space-y-4 animate-pulse">
        <div className="h-4 bg-stone-100 rounded w-32" />
        <div className="h-8 bg-stone-100 rounded w-2/3" />
        <div className="h-4 bg-stone-100 rounded w-1/3" />
        <div className="mt-8 space-y-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-4 bg-stone-100 rounded" />
          ))}
        </div>
      </div>
    );
  }

  return <DiscourseReader discourse={discourse} />;
}
