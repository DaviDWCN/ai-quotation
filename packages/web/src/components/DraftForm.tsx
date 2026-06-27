import React, { useState } from 'react';
import { Draft, DraftField } from '../lib/api';
import { ConfidenceBadge } from './ConfidenceBadge';
import { MissingFieldAlert } from './MissingFieldAlert';
import styles from './DraftForm.module.css';

interface DraftFormProps {
  draft: Draft;
  onSave: (data: Partial<Draft>) => Promise<any>;
}

export const DraftForm: React.FC<DraftFormProps> = ({ draft, onSave }) => {
  const [fields, setFields] = useState<DraftField[]>(draft.fields);
  const [saving, setSaving] = useState(false);

  const handleFieldChange = (key: string, value: string) => {
    setFields(prev => prev.map(f => f.key === key ? { ...f, value } : f));
  };

  const missingFields = fields
    .filter(f => f.required && !f.value)
    .map(f => f.label);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (missingFields.length > 0) {
      alert('Please fill in all required fields');
      return;
    }
    setSaving(true);
    try {
      // AC-7: Update status to COMPLETED upon human confirmation
      await onSave({ fields, status: 'COMPLETED' });
      alert('Draft submitted successfully');
    } catch (err) {
      alert('Error saving draft');
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <MissingFieldAlert fields={missingFields} />

      <div className={styles.fieldGroup}>
        {fields.map(field => (
          <div key={field.key} className={`${styles.field} ${field.required && !field.value ? styles.error : ''}`}>
            <div className={styles.labelRow}>
              <label htmlFor={field.key}>
                {field.label} {field.required && <span className={styles.required}>*</span>}
              </label>
              <ConfidenceBadge confidence={field.confidence} />
            </div>
            <input
              id={field.key}
              type="text"
              value={field.value}
              onChange={(e) => handleFieldChange(field.key, e.target.value)}
              className={styles.input}
            />
          </div>
        ))}
      </div>

      <div className={styles.actions}>
        <button type="submit" disabled={saving || missingFields.length > 0} className={styles.submitBtn}>
          {saving ? 'Saving...' : 'Confirm & Submit'}
        </button>
      </div>
    </form>
  );
};
