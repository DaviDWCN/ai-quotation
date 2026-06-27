const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface DraftField {
  key: string;
  label: string;
  value: string;
  confidence: 'high' | 'medium' | 'low';
  required: boolean;
}

export interface Draft {
  id: string;
  customer_id: string;
  status: 'DRAFT' | 'PENDING' | 'COMPLETED';
  fields: DraftField[];
  file_url?: string;
  created_at: string;
  updated_at: string;
}

export async function fetchDrafts(): Promise<Draft[]> {
  const response = await fetch(`${API_URL}/api/drafts`);
  if (!response.ok) {
    throw new Error('Failed to fetch drafts');
  }
  return response.json();
}

export async function fetchDraft(id: string): Promise<Draft> {
  const response = await fetch(`${API_URL}/api/drafts/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch draft');
  }
  return response.json();
}

export async function updateDraft(id: string, data: Partial<Draft>): Promise<Draft> {
  const response = await fetch(`${API_URL}/api/drafts/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('Failed to update draft');
  }
  return response.json();
}
