export type Language = "en" | "vi";

interface LanguageToggleProps {
  language: Language;
  /** false nếu full_text_vi là null/rỗng — ẩn option tiếng Việt */
  hasVietnamese: boolean;
  onChange: (lang: Language) => void;
}

export default function LanguageToggle({
  language,
  hasVietnamese,
  onChange,
}: LanguageToggleProps) {
  if (!hasVietnamese) {
    return (
      <div className="flex items-center gap-3">
        <span className="px-3 py-1.5 rounded-full text-sm bg-amber-100 text-amber-800 border border-amber-200">
          English
        </span>
        <span className="text-xs text-stone-400 italic">
          Bản dịch tiếng Việt chưa có
        </span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-1 p-1 bg-stone-100 rounded-full w-fit">
      <button
        onClick={() => onChange("en")}
        className={`px-3 py-1 rounded-full text-sm transition-colors ${
          language === "en"
            ? "bg-white text-stone-900 shadow-sm font-medium"
            : "text-stone-500 hover:text-stone-700"
        }`}
      >
        English
      </button>
      <button
        onClick={() => onChange("vi")}
        className={`px-3 py-1 rounded-full text-sm transition-colors ${
          language === "vi"
            ? "bg-white text-stone-900 shadow-sm font-medium"
            : "text-stone-500 hover:text-stone-700"
        }`}
      >
        Tiếng Việt
      </button>
    </div>
  );
}
