import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nikaya Reader",
  description: "Tra cứu và học bộ Middle Discourses (Majjhima Nikāya)",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-stone-50 text-stone-900 min-h-screen">
        <nav className="border-b border-stone-200 px-6 py-4 flex items-center gap-6 bg-white sticky top-0 z-10">
          <a href="/" className="font-semibold text-amber-800 mr-2">
            Nikaya Reader
          </a>
          <a href="/library" className="text-stone-600 hover:text-stone-900 text-sm transition-colors">
            Library
          </a>
          <a href="/search" className="text-stone-600 hover:text-stone-900 text-sm transition-colors">
            Search
          </a>
          <a href="/bookmarks" className="text-stone-600 hover:text-stone-900 text-sm transition-colors">
            Bookmarks
          </a>
        </nav>
        <main className="max-w-4xl mx-auto px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
