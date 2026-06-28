'use client';

import { useDraft } from '@/hooks/useDraft';
import { FilePreview } from '@/components/FilePreview';
import { DraftForm } from '@/components/DraftForm';
import { SplitViewReview } from '@/components/SplitViewReview';
import { useRouter } from 'next/navigation';

export default function ReviewPage({ params }: { params: { id: string } }) {
  const { draft, loading, error, saving, updateField, saveDraft } = useDraft(params.id);
  const router = useRouter();

  if (loading) return <div style={{ padding: '40px' }}>Loading...</div>;
  if (error) return <div style={{ padding: '40px', color: 'red' }}>Error: {error}</div>;
  if (!draft) return <div style={{ padding: '40px' }}>Draft not found</div>;

  const handleSave = async () => {
    await saveDraft('APPROVED');
    router.push('/drafts');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <header style={{ padding: '16px 20px', borderBottom: '1px solid #eee', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2 style={{ fontSize: '1.2rem' }}>Review Quotation #{draft.id.slice(-6)}</h2>
        <button onClick={() => router.back()} style={{ background: 'none', border: 'none', color: '#0070f3', cursor: 'pointer' }}>Back to List</button>
      </header>
      <SplitViewReview
        left={<FilePreview url={draft.file_url} type={draft.file_type} />}
        right={<DraftForm draft={draft} onUpdateField={updateField} onSave={handleSave} saving={saving} />}
      />
    </div>
  );
}
