import { SignUp } from "@clerk/nextjs";

export default function SignUpPage() {
  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-lg bg-mauve-800 flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 16 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                <circle cx="8" cy="8" r="6" /><path d="M8 4v4l3 2" />
              </svg>
            </div>
            <span className="font-display text-[15px] font-semibold text-ink">NewsIntel</span>
          </div>
          <h1 className="font-display text-2xl font-semibold text-ink">Create account</h1>
          <p className="text-[13px] text-ink-muted mt-1">Email verification required · No social login</p>
        </div>
        <SignUp
          appearance={{
            elements: {
              rootBox:            "w-full",
              card:               "shadow-none border border-[var(--border)] rounded-2xl p-6 bg-white",
              headerTitle:        "hidden",
              headerSubtitle:     "hidden",
              socialButtonsBlock: "hidden",
              dividerRow:         "hidden",
              formFieldInput:     "border border-[var(--border-md)] rounded-xl text-[13px]",
              formButtonPrimary:  "bg-mauve-800 hover:bg-mauve-900 rounded-xl text-[13px] font-medium",
              footerActionLink:   "text-mauve-600 hover:text-mauve-700",
            },
          }}
        />
      </div>
    </div>
  );
}