const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface DraftField {
  value: any;
  confidence: 'high' | 'medium' | 'low';
  required: boolean;
  label: string;
}

export type DraftStatus = 'draft' | 'confirmed' | 'submitted' | 'completed' | 'APPROVED';

export interface Draft {
  id: string;
  customer_id?: string;
  customer_match_score: number;
  status: DraftStatus;
  needs_confirmation: boolean;
  fields: Record<string, DraftField>;
  parsed_data: any;
  material_matches: any[];
  file_url?: string;
  file_type?: string;
  created_at: string;
  updated_at: string;
}

export async function fetchDrafts(): Promise<Draft[]> {
  const res = await fetch(`${API_URL}/api/drafts`);
  if (!res.ok) throw new Error('Failed to fetch drafts');
  return res.json();
}

export async function fetchDraftById(id: string): Promise<Draft> {
  const res = await fetch(`${API_URL}/api/drafts/${id}`);
  if (!res.ok) throw new Error('Failed to fetch draft');
  return res.json();
}

export async function updateDraft(id: string, data: Partial<Draft>): Promise<Draft> {
  const res = await fetch(`${API_URL}/api/drafts/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to update draft');
  return res.json();
}
