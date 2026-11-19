import React, { useState } from 'react';
import { WorkspaceHeader } from './WorkspaceHeader';
import { ConversationThread } from './ConversationThread';
import { QueryInput } from './QueryInput';
import { SourceDrawer } from './SourceDrawer';
import '../../styles/workspace.css'

export function AnswerWorkspace() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(true);

  const handleSelectSource = (sourceId) => {
    setIsDrawerOpen(true);
  };

  const handleCloseDrawer = () => {
    setIsDrawerOpen(false);
  };

  return (
    <div className="answer-workspace">
      {/* Top Navigation Bar */}
      <WorkspaceHeader 
        orgName="VTL" 
        workspaceName="Knowledge workspace" 
        roleName="Account Managers & Ops Supervisors" 
      />

      {/* Main Workspace Body */}
      <div className="workspace-body">
        {/* Center Feed Column */}
        <div className="feed-container">
          {/* Scrollable Conversation Content */}
          <div className="feed-content">
            <ConversationThread onSelectSource={handleSelectSource} />
          </div>

          {/* Fixed Bottom Input Area */}
          <div className="feed-bottom-bar">
            <QueryInput placeholder="Ask a follow-up about this answer..." />
            <div className="workspace-disclaimer">
              Answers use your available sources. Verify important details in the originals.
            </div>
          </div>
        </div>

        {/* Right Source Evidence Drawer */}
        {isDrawerOpen && (
          <SourceDrawer onClose={handleCloseDrawer} />
        )}
      </div>
    </div>
  );
}