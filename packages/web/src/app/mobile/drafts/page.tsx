'use client';

import { useEffect, useState } from 'react';
import { Draft, fetchDrafts } from '@/lib/api';
import { DraftList } from '@/components/DraftList';

export default function MobileDraftsPage() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDrafts().then(setDrafts).finally(() => setLoading(false));
  }, []);

  return (
    <main style={{ padding: '16px' }}>
      <h1 style={{ fontSize: '1.5rem', marginBottom: '16px' }}>My Drafts</h1>
      {loading ? <p>Loading...</p> : <DraftList drafts={drafts} mobile={true} />}
    </main>
  );
}
