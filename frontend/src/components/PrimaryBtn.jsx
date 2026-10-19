import React from 'react';
import './../styles/primary/components.css'

/**
 * Primary Button Component
 */
export function PrimaryButton({ children, onClick, type = 'button' }) {
  return (
    <button type={type} onClick={onClick} className="vault-btn-primary">
      {children}
    </button>
  );
}

/**
 * Status Chip Component
 * @param {'success' | 'selected'} type - The style variant matching the guide
 * @param {string} label - The text inside the chip
 */
export function StatusChip({ type = 'success', label }) {
  const variantClass = type === 'success' ? 'vault-chip-success' : 'vault-chip-selected';

  return (
    <span className={`vault-chip ${variantClass}`}>
      {type === 'success' && <span className="vault-chip-dot" />}
      {label}
    </span>
  );
}