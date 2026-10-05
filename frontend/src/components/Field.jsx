import { useId, useState } from "react";

export default function Field({ label, type = "text", ...props }) {
  const id = useId();
  const [visible, setVisible] = useState(false);
  const isPassword = type === "password";

  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <div className="field-control">
        <input
          id={id}
          type={isPassword && visible ? "text" : type}
          {...props}
        />
        {isPassword && (
          <button
            type="button"
            className="field-toggle"
            onClick={() => setVisible((v) => !v)}
            aria-label={visible ? "Hide password" : "Show password"}
          >
            {visible ? "Hide" : "Show"}
          </button>
        )}
      </div>
    </div>
  );
}