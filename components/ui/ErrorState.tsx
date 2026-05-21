export function ErrorState({
  message = "Something went wrong loading content.",
  onRetry,
}: {
  message?: string;
  onRetry?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <span className="text-4xl mb-4">⚠️</span>
      <p className="font-display text-base font-semibold text-ink mb-1">
        Unable to load content
      </p>
      <p className="text-[13px] text-ink-muted max-w-xs leading-relaxed">
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-5 px-5 py-2 rounded-xl border border-[var(--border-md)] text-[13px] font-medium text-ink-muted hover:bg-mauve-50 transition-colors"
        >
          Try again
        </button>
      )}
    </div>
  );
}