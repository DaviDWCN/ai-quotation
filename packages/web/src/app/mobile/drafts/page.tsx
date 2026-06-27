'use client';

import React, { useEffect, useState } from 'react';
import { Draft, fetchDrafts } from '@/src/lib/api';
import { DraftList } from '@/src/components/DraftList';

export default function MobileDraftsPage() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchDrafts()
      .then(setDrafts)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: '2rem' }}>Loading...</div>;

  return (
    <div style={{ maxWidth: '375px', margin: '0 auto', minHeight: '100vh', background: '#f7fafc' }}>
      <header style={{ padding: '1rem', background: 'white', borderBottom: '1px solid #e2e8f0', textAlign: 'center' }}>
        <h1 style={{ fontSize: '1.25rem', margin: 0 }}>My Drafts</h1>
      </header>
      <DraftList drafts={drafts} mobile />
    </div>
  );
}
