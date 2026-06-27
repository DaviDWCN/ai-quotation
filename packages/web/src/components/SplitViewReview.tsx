import { ReactNode } from 'react';
import styles from './SplitViewReview.module.css';

interface Props {
  left: ReactNode;
  right: ReactNode;
}

export function SplitViewReview({ left, right }: Props) {
  return (
    <div className={styles.container}>
      <div className={styles.left}>
        {left}
      </div>
      <div className={styles.right}>
        {right}
      </div>
    </div>
  );
}
