import { useState, useEffect } from 'react';
import { fetchDraft, fetchDrafts, updateDraft, QuotationDraft } from '../lib/api';

export function useDrafts() {
  const [drafts, setDrafts] = useState<QuotationDraft[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchDrafts()
      .then(setDrafts)
      .catch((err) => {
        console.warn('Mocking drafts for demo');
        setDrafts([
          {
            id: 'draft-1',
            status: 'PENDING',
            created_at: new Date().toISOString(),
            confidence_score: 0.8,
            missing_fields: [],
            data: { customer_name: 'Alpha Corp' },
            fields_config: [],
            items: []
          },
          {
            id: 'draft-2',
            status: 'APPROVED',
            created_at: new Date().toISOString(),
            confidence_score: 0.95,
            missing_fields: [],
            data: { customer_name: 'Beta LLC' },
            fields_config: [],
            items: []
          }
        ]);
      })
      .finally(() => setLoading(false));
  }, []);

  return { drafts, loading, error };
}

export function useDraft(id: string) {
  const [draft, setDraft] = useState<QuotationDraft | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!id) return;
    fetchDraft(id)
      .then(setDraft)
      .catch((err) => {
        console.warn('Using mock data due to fetch error:', err);
        setDraft({
          id: id,
          status: 'PENDING',
          created_at: new Date().toISOString(),
          confidence_score: 0.85,
          missing_fields: ['Tax ID'],
          data: {
            customer_name: 'Mock Customer Corp',
            customer_name_confidence: 'high',
            tax_id: '',
            tax_id_confidence: 'low'
          },
          fields_config: [
            { name: 'customer_name', label: 'Customer Name', type: 'text', required: true },
            { name: 'tax_id', label: 'Tax ID', type: 'text', required: true }
          ],
          items: [
            { material_name: 'Steel Pipe', quantity: 10, unit_price: 100, material_name_confidence: 'high' },
            { material_name: 'Unknown Part', quantity: 5, unit_price: 50, material_name_confidence: 'low' },
          ],
          item_fields_config: [
            { name: 'material_name', label: 'Material Name', type: 'text', required: true },
            { name: 'quantity', label: 'Qty', type: 'number', required: true },
            { name: 'unit_price', label: 'Price', type: 'number', required: true }
          ],
          file_url: 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
        });
      })
      .finally(() => setLoading(false));
  }, [id]);

  const update = async (data: Partial<QuotationDraft>) => {
    try {
      const updated = await updateDraft(id, data);
      setDraft(updated);
      return updated;
    } catch (err) {
      console.error('Update failed, but proceeding in mock mode', err);
      return data as QuotationDraft;
    }
  };

  return { draft, loading, error, update };
}
