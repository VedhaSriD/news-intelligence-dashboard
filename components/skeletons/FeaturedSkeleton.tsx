function Bone({ className }: { className?: string }) {
  return <div className={`bg-mauve-100 animate-shimmer rounded ${className ?? ""}`} />;
}

export function FeaturedSkeleton() {
  return (
    <div className="bg-white border border-[var(--border)] rounded-2xl overflow-hidden">
      <div className="h-0.5 bg-mauve-100" />
      <div className="p-5 md:p-6 flex flex-col md:flex-row gap-6">
        <div className="flex-1 space-y-3">
          <div className="flex gap-2">
            <Bone className="h-4 w-16 rounded-full" />
            <Bone className="h-4 w-14 rounded-full" />
          </div>
          <Bone className="h-6 w-full" />
          <Bone className="h-6 w-4/5" />
          <Bone className="h-4 w-full" />
          <Bone className="h-4 w-11/12" />
          <div className="flex justify-between pt-3 border-t border-[var(--border)]">
            <Bone className="h-3 w-24" />
            <Bone className="h-3 w-20" />
          </div>
        </div>
        <div className="w-full md:w-44 bg-mauve-50 rounded-xl p-4 space-y-3 flex-shrink-0">
          <Bone className="h-3 w-20" />
          <Bone className="h-2 w-full" />
          <Bone className="h-2 w-full" />
          <Bone className="h-2 w-3/4" />
        </div>
      </div>
    </div>
  );
}