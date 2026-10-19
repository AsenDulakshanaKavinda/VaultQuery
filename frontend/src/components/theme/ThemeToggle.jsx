import React from 'react';
import { useTheme } from '../../theme/ThemeContext';


export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      style={{
        padding: '8px 16px',
        borderRadius: '6px',
        border: '1px solid var(--border)',
        backgroundColor: 'var(--surface-card)',
        color: 'var(--text-primary)',
        cursor: 'pointer',
        fontSize: '14px',
        fontWeight: '500'
      }}
    >
      {theme === 'light' ? '🌙 Switch to Dark' : '☀️ Switch to Light'}
    </button>
  );
}