import Link from 'next/link';
import { Draft } from '@/lib/api';
import styles from './DraftList.module.css';

interface Props {
  drafts: Draft[];
  mobile?: boolean;
}

export function DraftList({ drafts, mobile }: Props) {
  const sortedDrafts = [...drafts].sort((a, b) =>
    new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  const groups = sortedDrafts.reduce((acc, draft) => {
    const status = draft.status || 'UNKNOWN';
    if (!acc[status]) acc[status] = [];
    acc[status].push(draft);
    return acc;
  }, {} as Record<string, Draft[]>);

  return (
    <div className={mobile ? styles.mobileList : styles.list}>
      {Object.entries(groups).map(([status, groupDrafts]) => (
        <div key={status} className={styles.group}>
          <h2 className={styles.groupTitle}>{status} ({groupDrafts.length})</h2>
          <div className={styles.groupItems}>
            {groupDrafts.map(draft => (
              <Link
                key={draft.id}
                href={mobile ? `/mobile/drafts/${draft.id}` : `/drafts/${draft.id}/review`}
                className={styles.card}
              >
                <div className={styles.cardHeader}>
                  <span className={styles.id}>#{draft.id.slice(-6)}</span>
                  <span className={`${styles.status} ${styles[(draft.status || '').toLowerCase()]}`}>
                    {draft.status}
                  </span>
                </div>
                <div className={styles.cardBody}>
                  <p>Created: {new Date(draft.created_at).toLocaleString()}</p>
                  <p>Fields: {Object.keys(draft.fields || {}).length}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      ))}
      {drafts.length === 0 && <p className={styles.empty}>No drafts found.</p>}
    </div>
  );
}
