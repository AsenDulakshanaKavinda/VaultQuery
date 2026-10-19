import React from 'react';
import { PrimaryButton, StatusChip } from './components/PrimaryBtn';
import { ThemeProvider } from './theme/ThemeContext';
import { ThemeToggle } from './components/theme/ThemeToggle';
import './styles/globals.css'
import { WorkspaceHeader } from './components/answer_workspace/WorkspaceHeader';


export default function App() {
  return (
    
    <ThemeProvider>
      <WorkspaceHeader 
        orgName="VTL" 
        workspaceName="Knowledge workspace" 
        roleName="Account Managers & Ops Supervisors" 
      />
      <main style={{ padding: '32px', minHeight: '100vh' }}>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h1>VaultQuery Workbench</h1>
          <ThemeToggle />
        </header>

        <section style={{ 
          backgroundColor: 'var(--surface-card)', 
          border: '1px solid var(--border)', 
          borderRadius: '8px', 
          padding: '24px',
          display: 'flex',
          gap: '12px',
          alignItems: 'center'
        }}>
          <PrimaryButton>Primary action</PrimaryButton>
          <StatusChip type="success" label="Synced" />
          <StatusChip type="selected" label="Selected source" />
        </section>
      </main>
      
    </ThemeProvider>

    
  );
}