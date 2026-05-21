export function EmptyState({
  icon = "📭",
  title,
  description,
  action,
}: {
  icon?:        string;
  title:        string;
  description?: string;
  action?:      React.ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
      <span className="text-5xl mb-4 block">{icon}</span>
      <p className="font-display text-lg font-semibold text-ink mb-1">{title}</p>
      {description && (
        <p className="text-[13px] text-ink-muted mt-1 max-w-xs leading-relaxed">
          {description}
        </p>
      )}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}