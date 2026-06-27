import React from 'react';
import styles from './ConfidenceBadge.module.css';

interface Props {
  confidence: 'high' | 'medium' | 'low';
}

export default function ConfidenceBadge({ confidence }: Props) {
  const label = confidence.toUpperCase();
  return (
    <span className={`${styles.badge} ${styles[confidence]}`}>
      {label}
    </span>
  );
}
