import { useState, useEffect } from 'react';
import { Draft, fetchDraftById, updateDraft } from '@/lib/api';

export function useDraft(id: string) {
  const [draft, setDraft] = useState<Draft | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchDraftById(id)
      .then(setDraft)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  const updateField = (key: string, value: any) => {
    if (!draft) return;
    setDraft({
      ...draft,
      fields: {
        ...draft.fields,
        [key]: { ...draft.fields[key], value }
      }
    });
  };

  const saveDraft = async (status?: string) => {
    if (!draft) return;
    setSaving(true);
    try {
      const updated = await updateDraft(id, {
        fields: draft.fields,
        status: status || (draft.status as any)
      });
      setDraft(updated);
      return updated;
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setSaving(false);
    }
  };

  return { draft, loading, error, saving, updateField, saveDraft };
}
