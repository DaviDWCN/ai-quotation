import { useState, useEffect, useCallback } from 'react';
import { Draft, fetchDraft, updateDraft } from '../lib/api';

export function useDraft(id: string) {
  const [draft, setDraft] = useState<Draft | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const loadDraft = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetchDraft(id);
      setDraft(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    if (id) {
      loadDraft();
    }
  }, [id, loadDraft]);

  const saveDraft = async (data: Partial<Draft>) => {
    try {
      const updated = await updateDraft(id, data);
      setDraft(updated);
      return updated;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to save draft'));
      throw err;
    }
  };

  return { draft, loading, error, saveDraft, refresh: loadDraft };
}
