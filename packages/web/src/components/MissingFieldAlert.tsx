import React from 'react';
import styles from './MissingFieldAlert.module.css';

interface Props {
  fields: string[];
}

export default function MissingFieldAlert({ fields }: Props) {
  if (fields.length === 0) return null;
  return (
    <div className={styles.alert}>
      <strong>Missing Mandatory Fields:</strong>
      <ul>
        {fields.map(f => <li key={f}>{f}</li>)}
      </ul>
    </div>
  );
}
