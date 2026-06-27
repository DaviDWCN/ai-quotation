'use client';

import React from 'react';
import Link from 'next/link';
import styles from './page.module.css';

export default function Page() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>AI Quotation System</h1>
      <div className={styles.links}>
        <Link href="/drafts" className={styles.card}>
          <h2>PC Interface</h2>
          <p>Full-screen review with document side-by-side</p>
        </Link>
        <Link href="/mobile/drafts" className={styles.card}>
          <h2>Mobile H5</h2>
          <p>Quick review optimized for WeCom</p>
        </Link>
      </div>
    </div>
  );
}
