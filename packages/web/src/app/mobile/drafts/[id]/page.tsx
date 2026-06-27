'use client';

import React from 'react';
import { useDraft } from '@/src/hooks/useDraft';
import { DraftForm } from '@/src/components/DraftForm';
import Link from 'next/link';

export default function MobileReviewPage({ params }: { params: { id: string } }) {
  const { draft, loading, error, saveDraft } = useDraft(params.id);

  if (loading) return <div style={{ padding: '2rem' }}>Loading...</div>;
  if (error) return <div style={{ padding: '2rem' }}>Error: {error.message}</div>;
  if (!draft) return <div style={{ padding: '2rem' }}>Not found</div>;

  return (
    <div style={{ maxWidth: '375px', margin: '0 auto', background: 'white', minHeight: '100vh' }}>
      <header style={{ padding: '1rem', background: '#3182ce', color: 'white', display: 'flex', alignItems: 'center' }}>
        <Link href="/mobile/drafts" style={{ color: 'white', textDecoration: 'none', marginRight: '1rem' }}>&larr;</Link>
        <h1 style={{ fontSize: '1.1rem', margin: 0 }}>Review Quotation</h1>
      </header>
      <div style={{ padding: '1rem', background: '#ebf8ff', fontSize: '0.875rem' }}>
        <strong>Customer:</strong> {draft.customer_id}
      </div>
      <DraftForm draft={draft} onSave={saveDraft} />
    </div>
  );
}
