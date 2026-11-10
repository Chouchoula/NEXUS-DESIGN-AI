"use client";

import { ArrowRight, Clock, Zap, Eye, CheckCircle, MoreHorizontal } from "lucide-react";
import { cn } from "@/lib/utils";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface ProjectCardProps {
  id: string;
  name: string;
  type: string;
  status: "draft" | "in_progress" | "review" | "completed";
  progress: number;
  lastUpdated: string;
  avatar: string;
  delay?: number;
  className?: string;
}

const statusConfig = {
  draft: { label: "Brouillon", icon: Clock, color: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300", bg: "bg-gray-500/10" },
  in_progress: { label: "En cours", icon: Zap, color: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400", bg: "bg-blue-500/10" },
  review: { label: "Revue", icon: Eye, color: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400", bg: "bg-yellow-500/10" },
  completed: { label: "Terminé", icon: CheckCircle, color: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400", bg: "bg-green-500/10" },
};

export function ProjectCard({ id, name, type, status, progress, lastUpdated, avatar, delay = 0, className }: ProjectCardProps) {
  const shouldReduce = useReducedMotion();
  const config = statusConfig[status];
  const StatusIcon = config.icon;

  const circumference = 2 * Math.PI * 40;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <article
      className={cn(
        "relative group overflow-hidden rounded-2xl p-5",
        "glass-card",
        "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
        "border border-[hsl(var(--glass-border))]",
        "transition-all duration-300 ease-out-expo",
        "hover:shadow-[var(--depth-3)] hover:border-[hsl(var(--glass-border)/0.9)] hover:-translate-y-1",
        "animate-slide-up",
        !shouldReduce && "stagger-1",
        className
      )}
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Brutal left accent border based on status */}
      <div
        className={cn(
          "absolute left-0 top-0 bottom-0 w-1.5 rounded-l-2xl",
          status === "draft" && "bg-gray-400",
          status === "in_progress" && "bg-gradient-to-b from-primary to-electric",
          status === "review" && "bg-gradient-to-b from-yellow-500 to-warning",
          status === "completed" && "bg-gradient-to-b from-green-500 to-success"
        )}
        aria-hidden="true"
      />

      {/* Background depth orbs */}
      <div className="absolute top-3 right-3 w-20 h-20 bg-primary/5 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />
      <div className="absolute bottom-3 left-3 w-12 h-12 bg-electric/5 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />

      <div className="relative flex items-start gap-4">
        {/* Avatar with status ring */}
        <div className="relative flex-shrink-0">
          <div
            className={cn(
              "w-14 h-14 rounded-xl flex items-center justify-center text-white font-bold text-lg",
              "shadow-[0_0_0_3px_hsl(var(--background))]",
              "relative z-10"
            )}
            style={{
              background: `hsl(var(--${status === "completed" ? "success" : status === "in_progress" ? "primary" : status === "review" ? "warning" : "muted-foreground"}) / 0.9)`,
            }}
          >
            {avatar}
          </div>
          {/* Status pulse ring when in_progress */}
          {status === "in_progress" && !shouldReduce && (
            <div
              className="absolute -inset-1 rounded-xl bg-primary/30 animate-pulse-glow pointer-events-none -z-10"
              aria-hidden="true"
            />
          )}
        </div>

        <div className="flex-1 min-w-0">
          {/* Header: Name + Status */}
          <div className="flex items-start justify-between gap-3 mb-2">
            <h3 className="font-semibold text-foreground truncate pr-8">{name}</h3>
            <Badge
              variant="outline"
              className={cn(
                "gap-1.5 px-2.5 py-1 text-xs font-medium",
                config.color,
                "border-[hsl(var(--glass-border))]",
                "shadow-[var(--depth-1)]"
              )}
            >
              <StatusIcon className="w-3 h-3" aria-hidden="true" />
              {config.label}
            </Badge>
          </div>

          {/* Type */}
          <p className="text-sm text-muted-foreground mb-3">{type}</p>

          {/* Progress Ring + Percentage */}
          <div className="flex items-center gap-3">
            <div className="relative w-12 h-12 flex-shrink-0">
              <svg className="w-12 h-12 progress-ring" viewBox="0 0 80 80" aria-hidden="true">
                <circle
                  cx="40"
                  cy="40"
                  r="40"
                  fill="none"
                  stroke="hsl(var(--muted))"
                  strokeWidth="4"
                  className="opacity-30"
                />
                <circle
                  cx="40"
                  cy="40"
                  r="40"
                  fill="none"
                  strokeWidth="4"
                  strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={offset}
                  className={cn(
                    "transition-all duration-700 ease-spring",
                    status === "in_progress" && "stroke-primary animate-pulse-glow",
                    status === "completed" && "stroke-success",
                    status === "review" && "stroke-warning",
                    status === "draft" && "stroke-muted-foreground"
                  )}
                  style={{
                    stroke: status === "in_progress"
                      ? "hsl(var(--primary))"
                      : status === "completed"
                      ? "hsl(var(--success))"
                      : status === "review"
                      ? "hsl(var(--warning))"
                      : "hsl(var(--muted-foreground))",
                  }}
                />
              </svg>
              <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-foreground">
                {progress}%
              </span>
            </div>

            <div className="flex-1 min-w-0">
              <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700 ease-spring"
                  style={{
                    width: `${progress}%`,
                    background: status === "in_progress"
                      ? "hsl(var(--primary))"
                      : status === "completed"
                      ? "hsl(var(--success))"
                      : status === "review"
                      ? "hsl(var(--warning))"
                      : "hsl(var(--muted-foreground))",
                  }}
                />
              </div>
            </div>

            <span className="text-sm font-bold text-foreground tabular-nums w-12 text-right">
              {progress}%
            </span>
          </div>

          {/* Footer: Last updated + Action */}
          <div className="mt-4 flex items-center justify-between pt-3 border-t border-[hsl(var(--glass-border))/0.5]">
            <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Clock className="w-3 h-3" aria-hidden="true" />
              {lastUpdated}
            </span>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 rounded-xl text-muted-foreground hover:text-foreground hover:bg-[hsl(var(--accent)/0.08)] transition-all group"
                  aria-label="Plus d'options"
                >
                  <MoreHorizontal className="w-4 h-4 transition-transform group-hover:rotate-90" aria-hidden="true" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="glass-strong rounded-xl border-[hsl(var(--glass-border))] shadow-[var(--depth-3)] animate-scale-in">
                <DropdownMenuItem className="flex items-center gap-2 text-foreground hover:bg-[hsl(var(--accent)/0.08)]">
                  <Eye className="w-4 h-4" aria-hidden="true" />
                  Voir le projet
                </DropdownMenuItem>
                <DropdownMenuItem className="flex items-center gap-2 text-foreground hover:bg-[hsl(var(--accent)/0.08)]">
                  <Zap className="w-4 h-4" aria-hidden="true" />
                  Lancer workflow
                </DropdownMenuItem>
                <DropdownMenuSeparator className="border-[hsl(var(--glass-border))]" />
                <DropdownMenuItem className="flex items-center gap-2 text-destructive hover:bg-[hsl(var(--destructive)/0.08)]">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Supprimer
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>

        {/* Arrow indicator on hover */}
        <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all duration-200 ease-out-expo opacity-0 group-hover:opacity-100" aria-hidden="true" />
      </div>
    </article>
  );
}