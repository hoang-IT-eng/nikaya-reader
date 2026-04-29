import type { Discourse } from "@/lib/types";
import BookmarkButton from "./BookmarkButton";

interface DiscourseReaderProps {
  discourse: Discourse;
}

export default function DiscourseReader({ discourse }: DiscourseReaderProps) {
  const paragraphs = discourse.full_text?.split("\n\n").filter(Boolean) ?? [];

  return (
    <article className="max-w-2xl">
      {/* Header */}
      <header className="mb-8">
        <p className="text-sm text-stone-400 mb-1">
          MN {discourse.mn_number} · Volume {discourse.volume}
          {discourse.vagga && ` · ${discourse.vagga}`}
        </p>
        <h1 className="text-2xl font-bold text-stone-900 mb-1">{discourse.title_en}</h1>
        {discourse.title_pali && (
          <p className="text-stone-500 italic">{discourse.title_pali}</p>
        )}
      </header>

      {/* Bookmark */}
      <div className="mb-8">
        <BookmarkButton mnNumber={discourse.mn_number} />
      </div>

      {/* Navigation */}
      <div className="flex gap-4 mb-8 text-sm">
        {discourse.mn_number > 1 && (
          <a
            href={`/discourse/${discourse.mn_number - 1}`}
            className="text-amber-700 hover:underline"
          >
            ← MN {discourse.mn_number - 1}
          </a>
        )}
        {discourse.mn_number < 152 && (
          <a
            href={`/discourse/${discourse.mn_number + 1}`}
            className="text-amber-700 hover:underline ml-auto"
          >
            MN {discourse.mn_number + 1} →
          </a>
        )}
      </div>

      {/* Content */}
      <div className="prose prose-stone max-w-none">
        {paragraphs.length > 0 ? (
          paragraphs.map((p, i) => (
            <p key={i} className="mb-4 leading-relaxed text-stone-800">
              {p}
            </p>
          ))
        ) : (
          <p className="text-stone-400 italic">No content available.</p>
        )}
      </div>

      {/* Citation */}
      <footer className="mt-12 pt-6 border-t border-stone-200 text-xs text-stone-400">
        Source: Middle Discourses (Majjhima Nikāya), Bhikkhu Sujato · MN {discourse.mn_number} · Volume {discourse.volume}
      </footer>
    </article>
  );
}
