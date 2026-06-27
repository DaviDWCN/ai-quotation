'use client';

import React from 'react';
import { useDraft } from '@/src/hooks/useDraft';
import { SplitViewReview } from '@/src/components/SplitViewReview';
import Link from 'next/link';

export default function PCReviewPage({ params }: { params: { id: string } }) {
  const { draft, loading, error, saveDraft } = useDraft(params.id);

  if (loading) return <div style={{ padding: '2rem' }}>Loading draft details...</div>;
  if (error) return <div style={{ padding: '2rem' }}>Error: {error.message}</div>;
  if (!draft) return <div style={{ padding: '2rem' }}>Draft not found</div>;

  return (
    <div>
      <header style={{ height: '60px', padding: '0 2rem', display: 'flex', alignItems: 'center', background: '#2d3748', color: 'white', justifyContent: 'space-between' }}>
        <h1 style={{ fontSize: '1.25rem' }}>Human-in-the-Loop Review</h1>
        <Link href="/drafts" style={{ color: '#ebf8ff', textDecoration: 'none' }}>&larr; Back to List</Link>
      </header>
      <SplitViewReview draft={draft} onSave={saveDraft} />
    </div>
  );
}
