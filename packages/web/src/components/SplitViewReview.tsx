import React from 'react';
import FilePreview from './FilePreview';
import DraftForm from './DraftForm';
import { QuotationDraft } from '../lib/api';
import styles from './SplitViewReview.module.css';

interface Props {
  draft: QuotationDraft;
  onUpdate: (data: Partial<QuotationDraft>) => Promise<void>;
}

export default function SplitViewReview({ draft, onUpdate }: Props) {
  return (
    <div className={styles.splitView}>
      <div className={styles.leftPane}>
        <div className={styles.paneHeader}>Original Document</div>
        <div className={styles.previewContainer}>
          <FilePreview url={draft.file_url || ''} />
        </div>
      </div>
      <div className={styles.rightPane}>
        <div className={styles.paneHeader}>Edit & Confirm</div>
        <div className={styles.formContainer}>
          <DraftForm draft={draft} onSubmit={onUpdate} />
        </div>
      </div>
    </div>
  );
}
