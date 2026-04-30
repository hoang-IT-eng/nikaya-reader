"use client";
import { useState, useEffect } from "react";
import type { Discourse } from "@/lib/types";
import LanguageToggle, { type Language } from "./LanguageToggle";

const STORAGE_KEY = "nikaya-language";

function getStoredLanguage(): Language {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === "en" || stored === "vi") return stored;
  } catch {
    // localStorage không khả dụng (private mode, v.v.)
  }
  return "en";
}

function setStoredLanguage(lang: Language) {
  try {
    localStorage.setItem(STORAGE_KEY, lang);
  } catch {
    // Bỏ qua nếu localStorage không khả dụng
  }
}

interface DiscourseReaderProps {
  discourse: Discourse;
}

export default function DiscourseReader({ discourse }: DiscourseReaderProps) {
  const [language, setLanguage] = useState<Language>("en");

  // Đọc preference từ localStorage sau khi mount (tránh hydration mismatch)
  useEffect(() => {
    const stored = getStoredLanguage();
    // Nếu đang ở tiếng Việt nhưng bài này không có bản dịch → fallback về English
    if (stored === "vi" && !discourse.full_text_vi) {
      setLanguage("en");
    } else {
      setLanguage(stored);
    }
  }, [discourse.mn_number, discourse.full_text_vi]);

  function handleLanguageChange(lang: Language) {
    setLanguage(lang);
    setStoredLanguage(lang);
  }

  const hasVietnamese = !!(discourse.full_text_vi && discourse.full_text_vi.trim());

  const title =
    language === "vi" && discourse.title_vi
      ? discourse.title_vi
      : discourse.title_en;

  const content =
    language === "vi" && discourse.full_text_vi
      ? discourse.full_text_vi
      : discourse.full_text;

  const paragraphs = content?.split("\n\n").filter(Boolean) ?? [];

  return (
    <article className="max-w-2xl">
      {/* Header */}
      <header className="mb-6">
        <p className="text-sm text-stone-400 mb-1">
          MN {discourse.mn_number} · Volume {discourse.volume}
          {discourse.vagga && ` · ${discourse.vagga}`}
        </p>
        <h1 className="text-2xl font-bold text-stone-900 mb-1">{title}</h1>
        {discourse.title_pali && (
          <p className="text-stone-500 italic text-sm">{discourse.title_pali}</p>
        )}
        {/* Hiển thị tên dịch giả */}
        <p className="text-xs text-stone-400 mt-1">
          {language === "vi"
            ? "Dịch: Hòa thượng Thích Minh Châu"
            : "Trans: Bhikkhu Sujato"}
        </p>
      </header>

      {/* Language Toggle */}
      <div className="mb-6">
        <LanguageToggle
          language={language}
          hasVietnamese={hasVietnamese}
          onChange={handleLanguageChange}
        />
      </div>

      {/* Navigation prev/next */}
      <div className="flex gap-4 mb-8 text-sm">
        {discourse.mn_number > 1 && (
          <a href={`/discourse/${discourse.mn_number - 1}`} className="text-amber-700 hover:underline">
            ← MN {discourse.mn_number - 1}
          </a>
        )}
        {discourse.mn_number < 152 && (
          <a href={`/discourse/${discourse.mn_number + 1}`} className="text-amber-700 hover:underline ml-auto">
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
          <p className="text-stone-400 italic">Không có nội dung.</p>
        )}
      </div>

      {/* Citation */}
      <footer className="mt-12 pt-6 border-t border-stone-200 text-xs text-stone-400">
        {language === "vi" ? (
          <>Nguồn: Kinh Trung Bộ (Majjhima Nikāya), Thích Minh Châu dịch · MN {discourse.mn_number}</>
        ) : (
          <>Source: Middle Discourses (Majjhima Nikāya), Bhikkhu Sujato · MN {discourse.mn_number} · Volume {discourse.volume}</>
        )}
      </footer>
    </article>
  );
}
