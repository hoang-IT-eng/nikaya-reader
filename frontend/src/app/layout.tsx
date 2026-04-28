import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Majjhima Study Hub",
  description: "Tra cứu và học bộ Middle Discourses (Majjhima Nikāya)",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-stone-50 text-stone-900 min-h-screen">
        <nav className="border-b border-stone-200 px-6 py-4 flex gap-6 bg-white">
          <a href="/" className="font-semibold text-amber-800">Majjhima Study Hub</a>
          <a href="/library" className="text-stone-600 hover:text-stone-900">Library</a>
          <a href="/search" className="text-stone-600 hover:text-stone-900">Search</a>
        </nav>
        <main className="max-w-4xl mx-auto px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
