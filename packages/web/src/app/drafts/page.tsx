'use client';

import { useEffect, useState } from 'react';
import { Draft, fetchDrafts } from '@/lib/api';
import { DraftList } from '@/components/DraftList';

export default function DraftsPage() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDrafts().then(setDrafts).finally(() => setLoading(false));
  }, []);

  return (
    <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px' }}>
      <h1 style={{ marginBottom: '24px' }}>Quotation Drafts</h1>
      {loading ? <p>Loading drafts...</p> : <DraftList drafts={drafts} />}
    </main>
  );
}
