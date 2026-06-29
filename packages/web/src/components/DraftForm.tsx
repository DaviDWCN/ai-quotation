import { Draft } from '@/lib/api';
import { ConfidenceBadge } from './ConfidenceBadge';
import { MissingFieldAlert } from './MissingFieldAlert';
import styles from './DraftForm.module.css';

interface Props {
  draft: Draft;
  onUpdateField: (key: string, value: any) => void;
  onSave: () => void;
  saving: boolean;
}

export function DraftForm({ draft, onUpdateField, onSave, saving }: Props) {
  const missingFields = Object.entries(draft.fields || {})
    .filter(([_, f]) => f.required && !f.value)
    .map(([_, f]) => f.label);

  const canSubmit = missingFields.length === 0;

  return (
    <div className={styles.form}>
      <MissingFieldAlert fields={missingFields} />

      {Object.entries(draft.fields || {}).map(([key, field]) => (
        <div key={key} className={`${styles.field} ${field.required && !field.value ? styles.error : ''}`}>
          <label className={styles.label}>
            {field.label}
            {field.required && <span className={styles.required}>*</span>}
            <ConfidenceBadge level={field.confidence} />
          </label>
          <input
            className={styles.input}
            type="text"
            value={field.value || ''}
            onChange={(e) => onUpdateField(key, e.target.value)}
          />
        </div>
      ))}

      <button
        className={styles.submitButton}
        onClick={onSave}
        disabled={saving || !canSubmit}
      >
        {saving ? 'Saving...' : 'Confirm & Submit'}
      </button>
    </div>
  );
}
