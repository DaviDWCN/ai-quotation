import React from 'react';
import Link from 'next/link';
import { QuotationDraft } from '../lib/api';
import styles from './DraftList.module.css';

interface Props {
  drafts: QuotationDraft[];
  baseUrl: string;
}

export default function DraftList({ drafts, baseUrl }: Props) {
  const groups = drafts.reduce((acc, draft) => {
    const status = draft.status || 'UNKNOWN';
    if (!acc[status]) acc[status] = [];
    acc[status].push(draft);
    return acc;
  }, {} as Record<string, QuotationDraft[]>);

  const statusOrder = ['PENDING', 'APPROVED', 'REJECTED'];

  return (
    <div className={styles.container}>
      {drafts.length === 0 && <p>No drafts found.</p>}
      {statusOrder.map(status => {
        const group = groups[status];
        if (!group || group.length === 0) return null;
        return (
          <div key={status} className={styles.group}>
            <h3 className={styles.groupTitle}>{status}</h3>
            <div className={styles.list}>
              {group.map(draft => (
                <Link href={`${baseUrl}/${draft.id}`} key={draft.id} className={styles.item}>
                  <div className={styles.header}>
                    <span className={styles.id}>#{draft.id.slice(0, 8)}</span>
                    <span className={`${styles.status} ${styles[draft.status.toLowerCase()]}`}>
                      {draft.status}
                    </span>
                  </div>
                  <div className={styles.customer}>
                    {draft.data?.customer_name || 'Unnamed Customer'}
                  </div>
                  <div className={styles.footer}>
                    <span>{new Date(draft.created_at).toLocaleString()}</span>
                    <span className={styles.score}>Confidence: {(draft.confidence_score * 100).toFixed(0)}%</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
