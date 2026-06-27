'use client';

import React, { useState } from 'react';
import { QuotationDraft, FieldMetadata } from '../lib/api';
import ConfidenceBadge from './ConfidenceBadge';
import MissingFieldAlert from './MissingFieldAlert';
import styles from './DraftForm.module.css';

interface Props {
  draft: QuotationDraft;
  onSubmit: (data: Partial<QuotationDraft>) => Promise<void>;
}

export default function DraftForm({ draft, onSubmit }: Props) {
  const [formData, setFormData] = useState(draft);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showErrors, setShowErrors] = useState(false);

  const validate = () => {
    const missing: string[] = [];
    draft.fields_config.forEach(field => {
      if (field.required && !formData.data[field.name]) {
        missing.push(field.label);
      }
    });
    // Simplified item validation
    if (formData.items.length === 0) missing.push('At least one item');
    return missing;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const missing = validate();
    if (missing.length > 0) {
      setShowErrors(true);
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleFieldChange = (name: string, value: any) => {
    setFormData({
      ...formData,
      data: { ...formData.data, [name]: value }
    });
  };

  const handleItemChange = (index: number, fieldName: string, value: any) => {
    const newItems = [...formData.items];
    newItems[index] = { ...newItems[index], [fieldName]: value };
    setFormData({ ...formData, items: newItems });
  };

  const currentMissing = validate();

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      {showErrors && <MissingFieldAlert fields={currentMissing} />}

      <div className={styles.metaSection}>
        {draft.fields_config.map(field => {
          const isMissing = showErrors && field.required && !formData.data[field.name];
          const confidence = formData.data[`${field.name}_confidence`] || 'high';

          return (
            <div key={field.name} className={styles.section}>
              <label>{field.label} {field.required && '*'}</label>
              <div className={`${styles.inputWrapper} ${styles[confidence]} ${isMissing ? styles.errorInput : ''}`}>
                <input
                  type={field.type}
                  value={formData.data[field.name] || ''}
                  onChange={(e) => handleFieldChange(field.name, e.target.value)}
                />
                <ConfidenceBadge confidence={confidence} />
              </div>
            </div>
          );
        })}
      </div>

      <div className={styles.itemsSection}>
        <h3>Items</h3>
        {formData.items.map((item, index) => (
          <div key={index} className={styles.itemRow}>
            {draft.item_fields_config?.map(field => {
              const confidence = item[`${field.name}_confidence`] || 'high';
              return (
                <div key={field.name} className={styles.fieldGroup}>
                  <label>{field.label}</label>
                  <div className={`${styles.inputWrapper} ${styles[confidence]}`}>
                    <input
                      type={field.type}
                      value={item[field.name] || ''}
                      onChange={(e) => handleItemChange(index, field.name, e.target.value)}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        ))}
      </div>

      <button type="submit" className="primary" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Confirm and Submit'}
      </button>
    </form>
  );
}
