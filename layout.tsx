/**
 * Auth route group layout.
 * Renders without Navbar/Footer — clean centered page for sign-in and sign-up.
 * The root layout's ClerkProvider still wraps this via Next.js layout nesting.
 */
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#faf7f9] flex flex-col">
      {children}
    </div>
  );
}