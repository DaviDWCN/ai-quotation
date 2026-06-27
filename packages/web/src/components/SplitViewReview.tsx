import React from 'react';
import { Draft } from '../lib/api';
import { FilePreview } from './FilePreview';
import { DraftForm } from './DraftForm';
import styles from './SplitViewReview.module.css';

interface SplitViewReviewProps {
  draft: Draft;
  onSave: (data: Partial<Draft>) => Promise<any>;
}

export const SplitViewReview: React.FC<SplitViewReviewProps> = ({ draft, onSave }) => {
  return (
    <div className={styles.container}>
      <div className={styles.leftPanel}>
        <div className={styles.panelHeader}>Original Document</div>
        <div className={styles.content}>
          <FilePreview url={draft.file_url} />
        </div>
      </div>
      <div className={styles.rightPanel}>
        <div className={styles.panelHeader}>Extracted Information</div>
        <div className={styles.content}>
          <DraftForm draft={draft} onSave={onSave} />
        </div>
      </div>
    </div>
  );
};
