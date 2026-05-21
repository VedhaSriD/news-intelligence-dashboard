"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { SignedIn, SignedOut, UserButton } from "@clerk/nextjs";
import { motion } from "motion/react";

const LINKS = [
  { href: "/",          label: "Feed"      },
  { href: "/archive",   label: "Archive"   },
  { href: "/search",    label: "Search"    },
  { href: "/bookmarks", label: "Bookmarks" },
  { href: "/sources",   label: "Sources"   },
];

export function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="sticky top-0 z-30 bg-white/90 backdrop-blur-sm border-b border-[var(--border)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">

        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-7 h-7 rounded-lg bg-mauve-800 flex items-center justify-center flex-shrink-0">
            <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 16 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <circle cx="8" cy="8" r="6" />
              <path d="M8 4v4l3 2" />
            </svg>
          </div>
          <span className="font-display text-[14px] font-semibold text-ink group-hover:text-mauve-700 transition-colors">
            NewsIntel
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-0.5">
          {LINKS.map((link) => {
            const active = link.href === "/" ? pathname === "/" : pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`relative px-3 py-1.5 rounded-lg text-[12px] font-medium transition-colors ${
                  active ? "text-mauve-700" : "text-ink-muted hover:text-ink-soft"
                }`}
              >
                {link.label}
                {active && (
                  <motion.div
                    layoutId="nav-active"
                    className="absolute inset-0 bg-mauve-50 rounded-lg -z-10"
                    transition={{ type: "spring", damping: 30, stiffness: 400 }}
                  />
                )}
              </Link>
            );
          })}
        </div>

        <div className="flex items-center gap-3">
          <SignedOut>
            <Link href="/sign-in"
              className="text-[12px] font-medium text-ink-muted hover:text-ink transition-colors hidden sm:block">
              Sign in
            </Link>
            <Link href="/sign-up"
              className="px-3.5 py-1.5 rounded-lg bg-mauve-800 text-white text-[12px] font-medium hover:bg-mauve-900 transition-colors">
              Sign up
            </Link>
          </SignedOut>
          <SignedIn>
            <UserButton afterSignOutUrl="/" />
          </SignedIn>
        </div>
      </div>
    </nav>
  );
}