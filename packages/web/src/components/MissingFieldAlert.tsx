import React from 'react';
import styles from './MissingFieldAlert.module.css';

interface MissingFieldAlertProps {
  fields: string[];
}

export const MissingFieldAlert: React.FC<MissingFieldAlertProps> = ({ fields }) => {
  if (fields.length === 0) return null;

  return (
    <div className={styles.alert}>
      <strong>Missing Required Fields:</strong>
      <ul>
        {fields.map(field => (
          <li key={field}>{field}</li>
        ))}
      </ul>
    </div>
  );
};
