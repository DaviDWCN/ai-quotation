import React from 'react';
import styles from './FilePreview.module.css';

interface FilePreviewProps {
  url?: string;
}

export const FilePreview: React.FC<FilePreviewProps> = ({ url }) => {
  if (!url) {
    return <div className={styles.empty}>No file to preview</div>;
  }

  // Very simple preview for demo/initial implementation
  // In a real app, you might use react-pdf or a more specialized viewer
  const isExcel = url.endsWith('.xlsx') || url.endsWith('.xls');

  if (isExcel) {
    return (
      <div className={styles.excelPlaceholder}>
        <p>Excel file preview not available in iframe. Please download to view.</p>
        <a href={url} target="_blank" rel="noopener noreferrer" className={styles.downloadBtn}>
          Download Excel
        </a>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <iframe src={url} className={styles.iframe} title="File Preview" />
    </div>
  );
};
