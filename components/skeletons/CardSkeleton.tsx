function Bone({ className }: { className?: string }) {
  return <div className={`bg-mauve-100 animate-shimmer rounded ${className ?? ""}`} />;
}

export function CardSkeleton() {
  return (
    <div className="bg-white border border-[var(--border)] rounded-2xl p-4 flex flex-col gap-3">
      <div className="flex justify-between">
        <Bone className="h-4 w-16 rounded-full" />
        <Bone className="h-3 w-10" />
      </div>
      <div className="space-y-2">
        <Bone className="h-4 w-full" />
        <Bone className="h-4 w-10/12" />
        <Bone className="h-4 w-4/5" />
      </div>
      <div className="space-y-1.5">
        <Bone className="h-3 w-full" />
        <Bone className="h-3 w-2/3" />
      </div>
      <div className="flex justify-between pt-2 border-t border-[var(--border)]">
        <Bone className="h-3 w-24" />
        <Bone className="h-3 w-10" />
      </div>
    </div>
  );
}

export function SkeletonGrid({ count = 6 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  );
}