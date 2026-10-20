import React from 'react';
import './styles/globals.css'
import { AnswerWorkspace } from './components/answer_workspace/AnswerWorkspace';
import { ThemeProvider } from './theme/ThemeContext';
import { SidebarLeft } from './components/answer_workspace/SidebarLeft';



export default function App() {
  return (
    <ThemeProvider>
      <div style={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
        <SidebarLeft />
        <AnswerWorkspace />
      </div>
    </ThemeProvider>
    

    

    
  );
}