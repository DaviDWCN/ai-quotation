import React from 'react';
import styles from './FilePreview.module.css';

interface Props {
  url: string;
}

export default function FilePreview({ url }: Props) {
  if (!url) {
    return <div className={styles.empty}>No file to preview</div>;
  }

  const isImage = url.match(/\.(jpeg|jpg|gif|png)$/i);

  if (isImage) {
    return (
      <div className={styles.container}>
        <img src={url} alt="Preview" className={styles.image} />
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <iframe src={url} className={styles.iframe} title="File Preview" />
    </div>
  );
}
