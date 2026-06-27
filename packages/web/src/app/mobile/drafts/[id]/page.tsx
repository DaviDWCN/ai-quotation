'use client';

import { useDraft } from '@/hooks/useDraft';
import { useParams, useRouter } from 'next/navigation';
import DraftForm from '@/components/DraftForm';
import FilePreview from '@/components/FilePreview';
import styles from './page.module.css';

export default function MobileReviewPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const { draft, loading, error, update } = useDraft(id);

  if (loading) return <div className={styles.loading}>Loading...</div>;
  if (error) return <div className={styles.error}>Error: {error.message}</div>;
  if (!draft) return <div className={styles.error}>Not found</div>;

  const handleUpdate = async (data: any) => {
    await update({ ...data, status: 'APPROVED' });
    router.push('/mobile/drafts');
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <button onClick={() => router.back()}>Back</button>
        <h2>审核草稿</h2>
      </header>
      <div className={styles.preview}>
        <FilePreview url={draft.file_url || ''} />
      </div>
      <div className={styles.form}>
        <DraftForm draft={draft} onSubmit={handleUpdate} />
      </div>
    </div>
  );
}
