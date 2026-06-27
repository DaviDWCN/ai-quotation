import styles from './MissingFieldAlert.module.css';

interface Props {
  fields: string[];
}

export function MissingFieldAlert({ fields }: Props) {
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
}
