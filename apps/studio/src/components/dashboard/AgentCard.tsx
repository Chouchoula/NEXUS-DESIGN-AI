"use client";

import { ArrowRight, Zap, Cpu, Sparkles, Check, AlertCircle, XCircle, Activity, Settings, MoreHorizontal, Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface AgentCardProps {
  id: string;
  name: string;
  type: string;
  status: "idle" | "running" | "completed" | "error" | "pending";
  progress: number;
  description: string;
  lastRun?: string;
  avatar?: string;
  color?: string;
  delay?: number;
  className?: string;
}

const statusConfig = {
  idle: { label: "Inactif", icon: Cpu, color: "text-muted-foreground bg-muted border-border", pulse: "bg-muted-foreground" },
  running: { label: "En cours", icon: Activity, color: "text-primary bg-primary/10 border-primary/20", pulse: "bg-primary animate-pulse-glow" },
  completed: { label: "Terminé", icon: Check, color: "text-success bg-success/10 border-success/20", pulse: "bg-success" },
  error: { label: "Erreur", icon: AlertCircle, color: "text-destructive bg-destructive/10 border-destructive/20", pulse: "bg-destructive" },
  pending: { label: "En attente", icon: Sparkles, color: "text-warning bg-warning/10 border-warning/20", pulse: "bg-warning animate-pulse-glow" },
};

const typeConfig: Record<string, { icon: React.ElementType; gradient: string }> = {
  researcher: { icon: Sparkles, gradient: "from-purple-500 to-pink-500" },
  planner: { icon: Cpu, gradient: "from-blue-500 to-cyan-500" },
  designer: { icon: Palette, gradient: "from-pink-500 to-rose-500" },
  developer: { icon: Bot, gradient: "from-green-500 to-emerald-500" },
  reviewer: { icon: Check, gradient: "from-orange-500 to-amber-500" },
  default: { icon: Zap, gradient: "from-primary to-electric" },
};

import { Palette, Bot } from "lucide-react";

export function AgentCard({ id, name, type, status, progress, description, lastRun, avatar, color, delay = 0, className }: AgentCardProps) {
  const shouldReduce = useReducedMotion();
  const config = statusConfig[status];
  const StatusIcon = config.icon;
  const typeInfo = typeConfig[type] || typeConfig.default;
  const TypeIcon = typeInfo.icon;

  const circumference = 2 * Math.PI * 28;
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
        !shouldReduce && "stagger-2",
        className
      )}
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Brutal top accent border based on status */}
      <div
        className={cn(
          "absolute top-0 left-0 right-0 h-1.5 rounded-t-2xl",
          status === "running" && "bg-gradient-to-r from-primary to-electric",
          status === "completed" && "bg-gradient-to-r from-success to-green-400",
          status === "error" && "bg-gradient-to-r from-destructive to-orange-500",
          status === "pending" && "bg-gradient-to-r from-warning to-yellow-400",
          status === "idle" && "bg-gradient-to-r from-muted-foreground to-muted"
        )}
        aria-hidden="true"
      />

      {/* Background depth orbs */}
      <div className="absolute top-2 right-2 w-16 h-16 bg-primary/5 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />
      <div className="absolute bottom-2 left-2 w-10 h-10 bg-electric/5 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />

      <div className="relative flex items-start gap-4">
        {/* Avatar with kinetic status pulse */}
        <div className="relative flex-shrink-0">
          <div className="relative">
            <Avatar className="w-14 h-14 rounded-xl ring-4 ring-[hsl(var(--background))]">
              {avatar ? (
                <AvatarImage src={avatar} alt="" />
              ) : (
                <AvatarFallback className="text-white font-bold text-lg" style={{ background: `linear-gradient(135deg, ${color || "hsl(var(--primary))"}, ${color || "hsl(var(--electric))"})` }}>
                  {name.charAt(0).toUpperCase()}
                </AvatarFallback>
              )}
            </Avatar>
            {/* Kinetic status pulse ring */}
            {!shouldReduce && status !== "idle" && (
              <div
                className={cn(
                  "absolute inset-0 rounded-[inherit] ring-2 pointer-events-none -z-10",
                  config.pulse
                )}
                aria-hidden="true"
              />
            )}
            {status === "running" && !shouldReduce && (
              <div className="absolute inset-0 rounded-[inherit] bg-primary/20 animate-pulse-glow pointer-events-none -z-10" aria-hidden="true" />
            )}
          </div>
        </div>

        <div className="flex-1 min-w-0">
          {/* Header: Type badge + Name + Status */}
          <div className="flex items-start justify-between gap-3 mb-2">
            <div className="flex items-center gap-2">
              <Badge
                variant="outline"
                className={cn(
                  "gap-1 px-2 py-0.5 text-[11px] font-medium uppercase tracking-wider",
                  "bg-gradient-to-r text-white border-0 shadow-[var(--depth-1)]",
                  typeInfo.gradient
                )}
              >
                <TypeIcon className="w-2.5 h-2.5" aria-hidden="true" />
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </Badge>
              <h3 className="font-semibold text-foreground truncate">{name}</h3>
            </div>
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

          {/* Description */}
          <p className="text-sm text-muted-foreground mb-3 line-clamp-2">{description}</p>

          {/* Progress Ring + Bar (only for running/pending) */}
          {(status === "running" || status === "pending") && (
            <div className="flex items-center gap-3 mb-3">
              <div className="relative w-10 h-10 flex-shrink-0">
                <svg className="w-10 h-10" viewBox="0 0 56 56" aria-hidden="true">
                  <circle
                    cx="28"
                    cy="28"
                    r="28"
                    fill="none"
                    stroke="hsl(var(--muted))"
                    strokeWidth="3.5"
                    className="opacity-30"
                  />
                  <circle
                    cx="28"
                    cy="28"
                    r="28"
                    fill="none"
                    strokeWidth="3.5"
                    strokeLinecap="round"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    className="transition-all duration-500 ease-spring"
                    style={{
                      stroke: status === "running" ? "hsl(var(--primary))" : "hsl(var(--warning))",
                    }}
                  />
                </svg>
                <span className="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-foreground">
                  {progress}%
                </span>
              </div>
              <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500 ease-spring"
                  style={{
                    width: `${progress}%`,
                    background: status === "running" ? "hsl(var(--primary))" : "hsl(var(--warning))",
                  }}
                />
              </div>
            </div>
          )}

          {/* Footer: Last run + Action */}
          <div className="flex items-center justify-between pt-3 border-t border-[hsl(var(--glass-border))/0.5]">
            <div className="flex items-center gap-3">
              {lastRun && (
                <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
                  <Clock className="w-3 h-3" aria-hidden="true" />
                  Dernier run: {lastRun}
                </span>
              )}
              {(status === "completed" || status === "error") && (
                <Badge variant="secondary" className="text-[10px] px-2 py-0.5">
                  {status === "completed" ? "Succès" : "Échoué"}
                </Badge>
              )}
            </div>
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
                  <Settings className="w-4 h-4" aria-hidden="true" />
                  Configurer
                </DropdownMenuItem>
                <DropdownMenuItem className="flex items-center gap-2 text-foreground hover:bg-[hsl(var(--accent)/0.08)]">
                  <Activity className="w-4 h-4" aria-hidden="true" />
                  Voir logs
                </DropdownMenuItem>
                <DropdownMenuSeparator className="border-[hsl(var(--glass-border))]" />
                <DropdownMenuItem className="flex items-center gap-2 text-destructive hover:bg-[hsl(var(--destructive)/0.08)]">
                  <XCircle className="w-4 h-4" aria-hidden="true" />
                  Arrêter
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