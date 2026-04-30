export interface Discourse {
  id: number;
  mn_number: number;
  title_en: string;
  title_pali: string;
  volume: number;
  vagga: string;
  page_start: number;
  full_text?: string;
  title_vi?: string | null;
  full_text_vi?: string | null;
}

export interface Bookmark {
  id: number;
  mn_number: number;
  note: string;
  created_at: string;
}

export interface SearchResult {
  mn_number: number;
  title_en: string;
  title_pali: string;
  volume: number;
  vagga: string;
  score: number;
}
