import React from 'react';
import styles from './ConfidenceBadge.module.css';

interface ConfidenceBadgeProps {
  confidence: 'high' | 'medium' | 'low';
}

export const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({ confidence }) => {
  const label = confidence.toUpperCase();
  return (
    <span className={`${styles.badge} ${styles[confidence]}`}>
      {label}
    </span>
  );
};
