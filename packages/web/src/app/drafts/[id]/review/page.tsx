'use client';

import { useDraft } from '@/hooks/useDraft';
import { useParams, useRouter } from 'next/navigation';
import SplitViewReview from '@/components/SplitViewReview';
import styles from './page.module.css';

export default function ReviewPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const { draft, loading, error, update } = useDraft(id);

  if (loading) return <div>Loading draft...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!draft) return <div>Draft not found</div>;

  const handleUpdate = async (data: any) => {
    await update({ ...data, status: 'APPROVED' });
    router.push('/drafts');
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <button onClick={() => router.back()} className={styles.backBtn}>← Back</button>
        <h2>Review Draft #{id.slice(0, 8)}</h2>
      </header>
      <SplitViewReview draft={draft} onUpdate={handleUpdate} />
    </div>
  );
}
