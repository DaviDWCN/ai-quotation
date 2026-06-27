const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface FieldMetadata {
  name: string;
  label: string;
  type: 'text' | 'number' | 'date';
  required: boolean;
}

export interface QuotationDraft {
  id: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  created_at: string;
  confidence_score: number;
  missing_fields: string[];
  file_url?: string;
  // Metadata driven fields
  data: Record<string, any>;
  fields_config: FieldMetadata[];
  // Items are usually special in quotations
  items: Array<Record<string, any>>;
  item_fields_config?: FieldMetadata[];
}

export async function fetchDrafts(): Promise<QuotationDraft[]> {
  const res = await fetch(`${API_URL}/api/drafts`);
  if (!res.ok) throw new Error('Failed to fetch drafts');
  return res.json();
}

export async function fetchDraft(id: string): Promise<QuotationDraft> {
  const res = await fetch(`${API_URL}/api/drafts/${id}`);
  if (!res.ok) throw new Error('Failed to fetch draft');
  return res.json();
}

export async function updateDraft(id: string, data: Partial<QuotationDraft>): Promise<QuotationDraft> {
  const res = await fetch(`${API_URL}/api/drafts/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to update draft');
  return res.json();
}
