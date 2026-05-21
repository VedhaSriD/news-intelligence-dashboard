"use client";

import type { ReactNode } from "react";
import { AnimatePresence, motion } from "motion/react";
import { useToastState, ToastContext } from "@/hooks/useToast";
import type { ToastType } from "@/types";

const STYLE: Record<ToastType, { cls: string; icon: string }> = {
  success: { cls: "bg-emerald-50 border-emerald-200 text-emerald-800", icon: "✓" },
  error:   { cls: "bg-red-50 border-red-200 text-red-800",             icon: "✕" },
  info:    { cls: "bg-blue-50 border-blue-200 text-blue-800",           icon: "ℹ" },
  warning: { cls: "bg-amber-50 border-amber-200 text-amber-800",       icon: "⚠" },
};

export function ToastProvider({ children }: { children: ReactNode }) {
  const state = useToastState();
  return (
    <ToastContext.Provider value={state}>
      {children}
      <div
        className="fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none"
        aria-live="polite"
      >
        <AnimatePresence>
          {state.toasts.map((t) => (
            <motion.div
              key={t.id}
              initial={{ opacity: 0, x: 40, scale: 0.94 }}
              animate={{ opacity: 1, x: 0,  scale: 1    }}
              exit={{    opacity: 0, x: 40, scale: 0.94 }}
              transition={{ type: "spring", damping: 28, stiffness: 300 }}
              className={`pointer-events-auto flex items-center gap-2.5 px-4 py-2.5 rounded-xl border text-[13px] font-medium shadow-card max-w-xs ${STYLE[t.type].cls}`}
            >
              <span>{STYLE[t.type].icon}</span>
              <span className="flex-1">{t.message}</span>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}