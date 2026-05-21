"use client";

import {
  createContext,
  useContext,
  useState,
  useCallback,
  useRef,
} from "react";
import type { ToastItem, ToastType } from "@/types";

interface ToastCtx {
  toasts:  ToastItem[];
  success: (msg: string) => void;
  error:   (msg: string) => void;
  info:    (msg: string) => void;
  warning: (msg: string) => void;
  dismiss: (id: string) => void;
}

export const ToastContext = createContext<ToastCtx>({
  toasts:  [],
  success: () => {},
  error:   () => {},
  info:    () => {},
  warning: () => {},
  dismiss: () => {},
});

export function useToast() {
  return useContext(ToastContext);
}

export function useToastState(): ToastCtx {
  const [toasts, setToasts] = useState<ToastItem[]>([]);
  const timers = useRef<Map<string, ReturnType<typeof setTimeout>>>(new Map());

  const dismiss = useCallback((id: string) => {
    setToasts((p) => p.filter((t) => t.id !== id));
    const t = timers.current.get(id);
    if (t) { clearTimeout(t); timers.current.delete(id); }
  }, []);

  const add = useCallback((message: string, type: ToastType) => {
    const id = `${Date.now()}-${Math.random()}`;
    setToasts((p) => [...p.slice(-3), { id, message, type }]);
    timers.current.set(id, setTimeout(() => dismiss(id), 4000));
  }, [dismiss]);

  return {
    toasts,
    dismiss,
    success: (m) => add(m, "success"),
    error:   (m) => add(m, "error"),
    info:    (m) => add(m, "info"),
    warning: (m) => add(m, "warning"),
  };
}