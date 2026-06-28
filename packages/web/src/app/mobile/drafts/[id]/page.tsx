'use client';

import { useDraft } from '@/hooks/useDraft';
import { FilePreview } from '@/components/FilePreview';
import { DraftForm } from '@/components/DraftForm';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function MobileReviewPage({ params }: { params: { id: string } }) {
  const { draft, loading, error, saving, updateField, saveDraft } = useDraft(params.id);
  const router = useRouter();
  const [view, setView] = useState<'form' | 'preview'>('form');

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;
  if (error) return <div style={{ padding: '20px', color: 'red' }}>Error: {error}</div>;
  if (!draft) return <div style={{ padding: '20px' }}>Draft not found</div>;

  const handleSave = async () => {
    await saveDraft('APPROVED');
    router.push('/mobile/drafts');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <header style={{ padding: '12px 16px', background: '#fff', borderBottom: '1px solid #eee', position: 'sticky', top: 0, zIndex: 10 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ fontSize: '1.1rem' }}>Review Draft</h2>
          <button onClick={() => router.back()} style={{ color: '#0070f3', border: 'none', background: 'none' }}>Close</button>
        </div>
        <div style={{ display: 'flex', marginTop: '12px', border: '1px solid #0070f3', borderRadius: '4px', overflow: 'hidden' }}>
          <button
            onClick={() => setView('form')}
            style={{ flex: 1, padding: '8px', border: 'none', background: view === 'form' ? '#0070f3' : '#fff', color: view === 'form' ? '#fff' : '#0070f3' }}
          >
            Form
          </button>
          <button
            onClick={() => setView('preview')}
            style={{ flex: 1, padding: '8px', border: 'none', background: view === 'preview' ? '#0070f3' : '#fff', color: view === 'preview' ? '#fff' : '#0070f3' }}
          >
            Preview
          </button>
        </div>
      </header>

      <main style={{ flex: 1 }}>
        {view === 'form' ? (
          <DraftForm draft={draft} onUpdateField={updateField} onSave={handleSave} saving={saving} />
        ) : (
          <div style={{ height: 'calc(100vh - 120px)', padding: '12px' }}>
            <FilePreview url={draft.file_url} type={draft.file_type} />
          </div>
        )}
      </main>
    </div>
  );
}
