import type { Discourse } from "@/lib/types";
import Link from "next/link";

interface DiscourseListProps {
  discourses: Discourse[];
  /** If true, groups items by vagga */
  grouped?: boolean;
}

function DiscourseRow({ d }: { d: Discourse }) {
  return (
    <Link
      href={`/discourse/${d.mn_number}`}
      className="flex items-center gap-3 p-3 rounded-lg hover:bg-stone-100 transition-colors"
    >
      <span className="text-xs text-stone-400 w-12 shrink-0">MN {d.mn_number}</span>
      <span className="font-medium text-stone-900">{d.title_en}</span>
      {d.title_pali && (
        <span className="text-stone-400 text-sm italic hidden sm:block">{d.title_pali}</span>
      )}
    </Link>
  );
}

export default function DiscourseList({ discourses, grouped = true }: DiscourseListProps) {
  if (!grouped) {
    return (
      <div className="space-y-1">
        {discourses.map((d) => (
          <DiscourseRow key={d.mn_number} d={d} />
        ))}
      </div>
    );
  }

  // Group by vagga
  const groups = discourses.reduce((acc, d) => {
    const key = d.vagga || "Uncategorized";
    if (!acc[key]) acc[key] = [];
    acc[key].push(d);
    return acc;
  }, {} as Record<string, Discourse[]>);

  return (
    <div>
      {Object.entries(groups).map(([vagga, items]) => (
        <div key={vagga} className="mb-8">
          <h2 className="text-xs font-semibold text-stone-400 uppercase tracking-widest mb-3 px-3">
            {vagga}
          </h2>
          <div className="space-y-0.5">
            {items.map((d) => (
              <DiscourseRow key={d.mn_number} d={d} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
