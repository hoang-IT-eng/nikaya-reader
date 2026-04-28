export default function Home() {
  return (
    <div className="text-center py-16">
      <h1 className="text-3xl font-bold text-amber-800 mb-3">Middle Discourses</h1>
      <p className="text-stone-500 mb-8">Majjhima Nikāya · Bhikkhu Sujato · 152 suttas</p>
      <div className="flex gap-4 justify-center">
        <a href="/library"
          className="bg-amber-700 text-white px-6 py-3 rounded-lg hover:bg-amber-800">
          Browse Library
        </a>
        <a href="/search"
          className="border border-stone-300 px-6 py-3 rounded-lg hover:bg-stone-100">
          Search
        </a>
      </div>
    </div>
  );
}
