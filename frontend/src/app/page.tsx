import Link from "next/link";

export default function Home() {
  return (
    <div className="text-center py-20">
      <p className="text-sm text-stone-400 uppercase tracking-widest mb-3">Majjhima Nikāya</p>
      <h1 className="text-4xl font-bold text-amber-800 mb-3">Middle Discourses</h1>
      <p className="text-stone-500 mb-2">Bhikkhu Sujato · 152 suttas</p>
      <p className="text-stone-400 text-sm mb-10 max-w-md mx-auto">
        Read, search, and study the Middle Length Discourses of the Buddha.
      </p>

      <div className="flex gap-4 justify-center flex-wrap">
        <Link
          href="/library"
          className="bg-amber-700 text-white px-6 py-3 rounded-lg hover:bg-amber-800 transition-colors"
        >
          Browse Library
        </Link>
        <Link
          href="/search"
          className="border border-stone-300 px-6 py-3 rounded-lg hover:bg-stone-100 transition-colors"
        >
          Search Suttas
        </Link>
      </div>

      {/* Quick links to popular suttas */}
      <div className="mt-16">
        <p className="text-xs text-stone-400 uppercase tracking-widest mb-4">Popular Suttas</p>
        <div className="flex flex-wrap gap-2 justify-center">
          {[
            { mn: 10, name: "Satipaṭṭhāna" },
            { mn: 22, name: "Alagaddūpama" },
            { mn: 36, name: "Mahāsaccaka" },
            { mn: 63, name: "Cūḷamāluṅkya" },
            { mn: 118, name: "Ānāpānasati" },
            { mn: 131, name: "Bhaddekaratta" },
          ].map(({ mn, name }) => (
            <Link
              key={mn}
              href={`/discourse/${mn}`}
              className="px-3 py-1.5 rounded-full border border-stone-200 text-sm text-stone-600 hover:bg-stone-100 transition-colors"
            >
              MN {mn} · {name}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
