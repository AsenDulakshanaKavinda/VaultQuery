const Icon = ({ children }) => (
  <svg
    width="45%"
    height="45%"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.8"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {children}
  </svg>
);

const icons = {
  shield: (
    <Icon>
      <path d="M12 3l8 3v6c0 4.5-3.2 7.8-8 9-4.8-1.2-8-4.5-8-9V6l8-3z" />
      <path d="M9 12l2 2 4-4" />
    </Icon>
  ),
  search: (
    <Icon>
      <circle cx="11" cy="11" r="6" />
      <path d="M20 20l-4.2-4.2" />
    </Icon>
  ),
  lock: (
    <Icon>
      <rect x="5" y="11" width="14" height="9" rx="2" />
      <path d="M8 11V8a4 4 0 018 0v3" />
    </Icon>
  ),
  file: (
    <Icon>
      <path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8l-5-5z" />
      <path d="M14 3v5h5M9 13h6M9 17h6" />
    </Icon>
  ),
  key: (
    <Icon>
      <circle cx="8" cy="15" r="4" />
      <path d="M11 12l9-9M16 7l3 3" />
    </Icon>
  ),
  folder: (
    <Icon>
      <path d="M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V7z" />
    </Icon>
  ),
};

// Positions are percentages of the artwork panel.
const bubbles = [
  { x: 14, y: 40, size: 52, color: "#7c6fd6", icon: "shield" },
  { x: 58, y: 24, size: 40, color: "#4b7bec", icon: "search" },
  { x: 40, y: 60, size: 36, color: "#e8a06a", icon: "lock" },
  { x: 84, y: 55, size: 60, color: "#c9c2ee", icon: "key", dark: true },
  { x: 62, y: 74, size: 42, color: "#f2b84b", icon: "file" },
  { x: 28, y: 86, size: 38, color: "#4aa58a", icon: "folder" },
  { x: 36, y: 20, size: 6, color: "#7c6fd6" },
  { x: 24, y: 58, size: 9, color: "#f2b84b" },
  { x: 54, y: 46, size: 7, color: "#1a1a1a" },
  { x: 88, y: 86, size: 9, color: "#f2b84b" },
];

export default function AuthLayout({ children }) {
  return (
    <div className="auth-page">
      <div className="auth-frame">
        <div className="auth-logo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" strokeWidth="2.4" />
            <circle cx="12" cy="12" r="3" fill="currentColor" />
          </svg>
          <span>VaultQuery</span>
        </div>

        <main className="auth-form-side">{children}</main>

        <aside className="auth-art" aria-hidden="true">
          {bubbles.map((b, i) => (
            <span
              key={i}
              className={`bubble${b.dark ? " bubble-dark" : ""}`}
              style={{
                left: `${b.x}%`,
                top: `${b.y}%`,
                width: b.size,
                height: b.size,
                background: b.color,
              }}
            >
              {b.icon && icons[b.icon]}
            </span>
          ))}
        </aside>
      </div>
    </div>
  );
}