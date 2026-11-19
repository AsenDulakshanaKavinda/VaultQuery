import React from 'react';
import './styles/globals.css'
import { ThemeProvider } from './theme/ThemeContext';
import { LoginScreen } from './components/auth/LoginScreen';
import { Route, Routes } from 'react-router-dom';
import { PasswordReset } from './components/auth/PasswordReset';
import { RequestAccess } from './components/auth/RequestAccess';


export default function App() {
  return (
    <ThemeProvider>
      <div style={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
        {
        /*<SidebarLeft />
        <AnswerWorkspace />
        */}

        

        <Routes>
          <Route path='/' element={<LoginScreen />} />
          <Route path="/password-reset" element={<PasswordReset />} />
          <Route path="/request-access" element={<RequestAccess />} />
        </Routes>
      </div>
    </ThemeProvider>
    

    

    
  );
}