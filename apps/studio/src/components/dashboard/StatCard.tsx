"use client";

import { ArrowUpRight, ArrowDownRight, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { cn } from "@/lib/utils";
import { useCountUpOnView } from "@/hooks/useCountUp";
import { useReducedMotion } from "@/hooks/useReducedMotion";

interface StatCardProps {
  label: string;
  value: string | number;
  change?: string;
  trend?: "up" | "down" | "neutral";
  icon?: React.ReactNode;
  delay?: number;
  className?: string;
}

const trendIcons = {
  up: ArrowUpRight,
  down: ArrowDownRight,
  neutral: Minus,
};

const trendColors = {
  up: "text-success bg-success/10 border-success/20",
  down: "text-destructive bg-destructive/10 border-destructive/20",
  neutral: "text-muted-foreground bg-muted border-border",
};

export function StatCard({ label, value, change, trend = "neutral", icon, delay = 0, className }: StatCardProps) {
  const shouldReduce = useReducedMotion();
  const numericValue = typeof value === "string" ? parseFloat(value.replace(/[^0-9.-]/g, "")) : value;
  const suffix = typeof value === "string" ? value.replace(/[\d.,]/g, "").trim() : "";

  const { count, ref } = useCountUpOnView({
    end: numericValue,
    duration: 1000,
    delay,
    decimals: 0,
    separator: " ",
    suffix,
  });

  const TrendIcon = trendIcons[trend];
  const trendClass = trendColors[trend];

  return (
    <div
      ref={ref}
      className={cn(
        "relative overflow-hidden rounded-2xl p-6",
        "glass-card",
        "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
        "border border-[hsl(var(--glass-border))]",
        "transition-all duration-300 ease-out-expo",
        "hover:shadow-[var(--depth-3)] hover:border-[hsl(var(--glass-border)/0.9)]",
        "animate-slide-up",
        !shouldReduce && "stagger-1",
        className
      )}
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Brutal top accent border */}
      <div
        className={cn(
          "absolute top-0 left-0 right-0 h-1.5 rounded-t-2xl",
          trend === "up" && "bg-gradient-to-r from-success to-primary",
          trend === "down" && "bg-gradient-to-r from-destructive to-orange-500",
          trend === "neutral" && "bg-gradient-to-r from-primary to-electric"
        )}
        aria-hidden="true"
      />

      {/* Background orbs for depth */}
      <div className="absolute top-4 right-4 w-24 h-24 bg-primary/5 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />
      <div className="absolute bottom-4 left-4 w-16 h-16 bg-electric/5 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />

      <div className="relative flex items-start justify-between">
        <div className="min-w-0">
          <p className="text-sm font-medium text-muted-foreground mb-2 tracking-wide uppercase">{label}</p>
          <p className="text-display font-bold text-foreground tabular-nums" aria-live="polite">
            {count}
          </p>
        </div>

        {icon && (
          <div className="flex-shrink-0 ml-4 w-12 h-12 rounded-xl bg-[hsl(var(--primary)/0.12)] flex items-center justify-center text-primary">
            {icon}
          </div>
        )}
      </div>

      {change && (
        <div className="mt-4 flex items-center gap-2" role="status" aria-live="polite">
          <span className={cn(
            "flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold border",
            trendClass,
            "transition-all duration-200 ease-out-expo"
          )}>
            <TrendIcon className="w-3 h-3" aria-hidden="true" />
            {change}
          </span>
          <span className="text-xs text-muted-foreground">vs période précédente</span>
        </div>
      )}
    </div>
  );
}