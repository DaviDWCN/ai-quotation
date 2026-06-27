'use client';

import { useDrafts } from '@/hooks/useDraft';
import DraftList from '@/components/DraftList';
import styles from './page.module.css';

export default function MobileDraftsPage() {
  const { drafts, loading, error } = useDrafts();

  if (loading) return <div className={styles.loading}>Loading...</div>;
  if (error) return <div className={styles.error}>Error: {error.message}</div>;

  return (
    <div className={styles.mobileContainer}>
      <header className={styles.header}>
        <h1>待处理草稿</h1>
      </header>
      <div className={styles.content}>
        <DraftList drafts={drafts} baseUrl="/mobile/drafts" />
      </div>
    </div>
  );
}
