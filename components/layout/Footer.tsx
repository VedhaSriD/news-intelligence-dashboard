import Link from "next/link";
import { ALL_CATEGORIES, CATEGORY_META } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="border-t border-[var(--border)] bg-white mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">

          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-6 h-6 rounded-md bg-mauve-800 flex items-center justify-center">
                <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 16 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <circle cx="8" cy="8" r="6" /><path d="M8 4v4l3 2" />
                </svg>
              </div>
              <span className="font-display text-[13px] font-semibold text-ink">NewsIntel</span>
            </div>
            <p className="text-[12px] text-ink-muted leading-relaxed max-w-xs">
              Verified, deduplicated global news. Powered by NewsAPI + GDELT. Refreshed every 6 hours.
            </p>
          </div>

          <div>
            <h3 className="text-[11px] font-semibold text-ink uppercase tracking-wider mb-3">Categories</h3>
            <div className="grid grid-cols-2 gap-y-1.5 gap-x-2">
              {ALL_CATEGORIES.map((slug) => (
                <Link key={slug} href={`/category/${slug}`}
                  className="text-[12px] text-ink-muted hover:text-mauve-700 transition-colors">
                  {CATEGORY_META[slug].label}
                </Link>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-[11px] font-semibold text-ink uppercase tracking-wider mb-3">Pages</h3>
            <div className="flex flex-col gap-1.5">
              {[
                { href: "/",          label: "Latest feed"  },
                { href: "/archive",   label: "Archive"      },
                { href: "/search",    label: "Search"       },
                { href: "/bookmarks", label: "Bookmarks"    },
                { href: "/sources",   label: "Sources"      },
              ].map((l) => (
                <Link key={l.href} href={l.href}
                  className="text-[12px] text-ink-muted hover:text-mauve-700 transition-colors">
                  {l.label}
                </Link>
              ))}
            </div>
          </div>
        </div>

        <div className="border-t border-[var(--border)] pt-5 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p className="text-[11px] text-ink-muted">© {new Date().getFullYear()} NewsIntel. Portfolio project.</p>
          <p className="text-[11px] text-ink-muted">Next.js · FastAPI · PostgreSQL · Clerk</p>
        </div>
      </div>
    </footer>
  );
}