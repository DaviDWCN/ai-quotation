'use client';

import React, { useEffect, useState } from 'react';
import { Draft, fetchDrafts } from '@/src/lib/api';
import { DraftList } from '@/src/components/DraftList';

export default function DraftsPage() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchDrafts()
      .then(setDrafts)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading drafts...</div>;
  if (error) return <div>Error loading drafts: {error.message}</div>;

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '2rem' }}>
      <h1>Quotation Drafts</h1>
      <DraftList drafts={drafts} />
    </div>
  );
}
