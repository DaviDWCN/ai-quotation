import styles from './FilePreview.module.css';

interface Props {
  url: string;
  type: string;
}

export function FilePreview({ url, type }: Props) {
  if (!url) return <div className={styles.empty}>No file to preview</div>;

  return (
    <div className={styles.container}>
      {type === 'pdf' || type === 'excel' ? (
        <iframe src={url} className={styles.preview} title="File Preview" />
      ) : (
        <img src={url} className={styles.image} alt="Preview" />
      )}
    </div>
  );
}
