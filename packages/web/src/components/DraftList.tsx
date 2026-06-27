import React from 'react';
import Link from 'next/link';
import { Draft } from '../lib/api';
import styles from './DraftList.module.css';

interface DraftListProps {
  drafts: Draft[];
  mobile?: boolean;
}

export const DraftList: React.FC<DraftListProps> = ({ drafts, mobile = false }) => {
  if (drafts.length === 0) {
    return <div className={styles.empty}>No drafts found</div>;
  }

  const grouped = drafts.reduce((acc, draft) => {
    const status = draft.status;
    if (!acc[status]) acc[status] = [];
    acc[status].push(draft);
    return acc;
  }, {} as Record<string, Draft[]>);

  // Sort groups by custom order if needed, here just by keys
  const statusOrder = ['DRAFT', 'PENDING', 'COMPLETED'];
  const statuses = Object.keys(grouped).sort((a, b) => statusOrder.indexOf(a) - statusOrder.indexOf(b));

  return (
    <div className={styles.list}>
      {statuses.map(status => (
        <div key={status} className={styles.section}>
          <h3 className={styles.sectionTitle}>{status}</h3>
          {grouped[status].sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()).map(draft => (
            <Link
              key={draft.id}
              href={mobile ? `/mobile/drafts/${draft.id}` : `/drafts/${draft.id}/review`}
              className={styles.card}
            >
              <div className={styles.cardHeader}>
                <span className={styles.customerId}>{draft.customer_id}</span>
                <span className={`${styles.status} ${styles[draft.status.toLowerCase()]}`}>
                  {draft.status}
                </span>
              </div>
              <div className={styles.cardBody}>
                <div className={styles.info}>
                  <span>ID: {draft.id}</span>
                  <span>Updated: {new Date(draft.updated_at).toLocaleString()}</span>
                </div>
                <div className={styles.fields}>
                  {draft.fields.length} fields detected
                </div>
              </div>
            </Link>
          ))}
        </div>
      ))}
    </div>
  );
};
