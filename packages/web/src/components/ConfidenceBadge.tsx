import styles from './ConfidenceBadge.module.css';

interface Props {
  level: 'high' | 'medium' | 'low';
}

export function ConfidenceBadge({ level }: Props) {
  return (
    <span className={`${styles.badge} ${styles[level]}`}>
      {level.toUpperCase()}
    </span>
  );
}
