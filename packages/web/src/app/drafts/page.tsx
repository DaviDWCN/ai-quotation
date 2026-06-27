'use client';

import { useDrafts } from '@/hooks/useDraft';
import DraftList from '@/components/DraftList';
import styles from './page.module.css';

export default function DraftsPage() {
  const { drafts, loading, error } = useDrafts();

  if (loading) return <div>Loading drafts...</div>;
  if (error) return <div>Error loading drafts: {error.message}</div>;

  return (
    <div className="container">
      <header className={styles.header}>
        <h1>Quotation Drafts</h1>
        <p>Manage and review AI-extracted quotations.</p>
      </header>
      <DraftList drafts={drafts} baseUrl="/drafts" />
    </div>
  );
}
