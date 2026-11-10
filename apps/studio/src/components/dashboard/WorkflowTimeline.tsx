"use client";

import { ChevronRight, CheckCircle, Clock, Zap, AlertCircle, XCircle, MoreHorizontal, Loader2 } from "lucide-react";
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

interface WorkflowStep {
  id: string;
  name: string;
  description: string;
  status: "pending" | "running" | "completed" | "error" | "skipped";
  duration?: string;
  agent?: string;
  logs?: string[];
}

interface WorkflowTimelineProps {
  title?: string;
  steps: WorkflowStep[];
  currentStep?: string;
  className?: string;
}

const statusConfig = {
  pending: { label: "En attente", icon: Clock, color: "text-muted-foreground bg-muted border-border", dot: "bg-muted-foreground/30" },
  running: { label: "En cours", icon: Loader2, color: "text-primary bg-primary/10 border-primary/20", dot: "bg-primary animate-pulse-glow" },
  completed: { label: "Terminé", icon: CheckCircle, color: "text-success bg-success/10 border-success/20", dot: "bg-success" },
  error: { label: "Erreur", icon: XCircle, color: "text-destructive bg-destructive/10 border-destructive/20", dot: "bg-destructive" },
  skipped: { label: "Ignoré", icon: AlertCircle, color: "text-warning bg-warning/10 border-warning/20", dot: "bg-warning" },
};

export function WorkflowTimeline({ title = "Pipeline d'exécution", steps, currentStep, className }: WorkflowTimelineProps) {
  const shouldReduce = useReducedMotion();

  return (
    <section className={cn("animate-slide-up", className)} aria-labelledby="workflow-timeline-heading">
      <div className="flex items-center justify-between mb-6">
        <h2 id="workflow-timeline-heading" className="text-headline font-bold text-foreground">
          {title}
        </h2>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span className="font-mono tabular-nums">
            {steps.filter(s => s.status === "completed").length} / {steps.length} étapes
          </span>
        </div>
      </div>

      <div className="relative">
        {/* Vertical timeline connector */}
        <div
          className={cn(
            "absolute left-8 top-0 bottom-0 w-0.5",
            "bg-gradient-to-b from-primary/30 via-electric/20 to-success/30",
            "rounded-full"
          )}
          aria-hidden="true"
        />

        <div className="space-y-6" role="list" aria-label="Étapes du workflow">
          {steps.map((step, index) => {
            const config = statusConfig[step.status];
            const StatusIcon = config.icon;
            const isCurrent = currentStep === step.id;
            const isLast = index === steps.length - 1;

            return (
              <article
                key={step.id}
                className={cn(
                  "relative group flex gap-4",
                  "animate-slide-up",
                  !shouldReduce && `stagger-${(index % 8) + 1}`
                )}
                style={{ animationDelay: `${index * 80}ms` }}
                role="listitem"
              >
                {/* Timeline dot + connector */}
                <div className="relative flex-shrink-0 w-16">
                  <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-[hsl(var(--muted))]" aria-hidden="true" />
                  {!isLast && (
                    <div className="absolute left-8 top-full bottom-0 w-0.5 bg-[hsl(var(--muted))]" aria-hidden="true" />
                  )}

                  <div
                    className={cn(
                      "relative z-10 w-4 h-4 rounded-full border-4 flex-shrink-0 mx-auto",
                      "transition-all duration-300 ease-spring",
                      "shadow-[0_0_0_4px_hsl(var(--background))]",
                      config.dot,
                      isCurrent && "ring-4 ring-primary/20 scale-125",
                      step.status === "running" && !shouldReduce && "animate-pulse-glow"
                    )}
                    aria-hidden="true"
                  >
                    {step.status === "completed" && (
                      <CheckCircle className="w-3 h-3 text-success absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" aria-hidden="true" />
                    )}
                    {step.status === "error" && (
                      <XCircle className="w-3 h-3 text-destructive absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" aria-hidden="true" />
                    )}
                    {step.status === "running" && !shouldReduce && (
                      <Loader2 className="w-3 h-3 text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-spin" aria-hidden="true" />
                    )}
                  </div>

                  {/* Step number */}
                  <span className="absolute left-8 top-1/2 -translate-y-1/2 -translate-x-full mr-3 text-xs font-mono text-muted-foreground/60 w-20 text-right">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                </div>

                {/* Step content - Editorial zigzag layout */}
                <div
                  className={cn(
                    "flex-1 min-w-0",
                    index % 2 === 0 ? "md:pl-4" : "md:pr-4"
                  )}
                >
                  <div
                    className={cn(
                      "relative rounded-2xl p-5",
                      "glass-card",
                      "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
                      "border border-[hsl(var(--glass-border))]",
                      "transition-all duration-300 ease-out-expo",
                      "hover:shadow-[var(--depth-3)] hover:border-[hsl(var(--glass-border)/0.9)]",
                      isCurrent && "ring-2 ring-primary/30",
                      step.status === "completed" && "bg-success/5 border-success/20",
                      step.status === "error" && "bg-destructive/5 border-destructive/20",
                      step.status === "running" && "bg-primary/5 border-primary/20"
                    )}
                  >
                    {/* Brutal left accent */}
                    <div
                      className={cn(
                        "absolute left-0 top-0 bottom-0 w-1.5 rounded-l-2xl",
                        step.status === "completed" && "bg-gradient-to-b from-success to-green-400",
                        step.status === "running" && "bg-gradient-to-b from-primary to-electric",
                        step.status === "error" && "bg-gradient-to-b from-destructive to-orange-500",
                        step.status === "pending" && "bg-gradient-to-b from-muted-foreground to-muted",
                        step.status === "skipped" && "bg-gradient-to-b from-warning to-yellow-400"
                      )}
                      aria-hidden="true"
                    />

                    {/* Background orb */}
                    <div className="absolute top-2 right-2 w-16 h-16 bg-primary/5 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />

                    <div className="relative flex items-start gap-4">
                      <div className="flex-1 min-w-0">
                        {/* Header */}
                        <div className="flex items-start justify-between gap-3 mb-2">
                          <div className="flex items-center gap-2 flex-wrap">
                            <h3 className="font-semibold text-foreground">{step.name}</h3>
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
                            {isCurrent && !shouldReduce && (
                              <span className="flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-primary/10 text-primary animate-pulse-glow">
                                <Zap className="w-2.5 h-2.5" aria-hidden="true" />
                                Actif
                              </span>
                            )}
                          </div>

                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="h-8 w-8 rounded-xl text-muted-foreground hover:text-foreground hover:bg-[hsl(var(--accent)/0.08)] transition-all group opacity-0 group-hover:opacity-100"
                                aria-label="Plus d'options"
                              >
                                <MoreHorizontal className="w-4 h-4 transition-transform group-hover:rotate-90" aria-hidden="true" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="glass-strong rounded-xl border-[hsl(var(--glass-border))] shadow-[var(--depth-3)] animate-scale-in">
                              <DropdownMenuItem className="flex items-center gap-2 text-foreground hover:bg-[hsl(var(--accent)/0.08)]">
                                <Clock className="w-4 h-4" aria-hidden="true" />
                                Voir les logs
                              </DropdownMenuItem>
                              <DropdownMenuItem className="flex items-center gap-2 text-foreground hover:bg-[hsl(var(--accent)/0.08)]">
                                <Zap className="w-4 h-4" aria-hidden="true" />
                                Réexécuter
                              </DropdownMenuItem>
                              <DropdownMenuSeparator className="border-[hsl(var(--glass-border))]" />
                              <DropdownMenuItem className="flex items-center gap-2 text-destructive hover:bg-[hsl(var(--destructive)/0.08)]">
                                <XCircle className="w-4 h-4" aria-hidden="true" />
                                Annuler
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                        </div>

                        {/* Description */}
                        <p className="text-sm text-muted-foreground mb-3">{step.description}</p>

                        {/* Meta info */}
                        <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
                          {step.agent && (
                            <span className="flex items-center gap-1.5">
                              <span className="w-2 h-2 rounded-full bg-primary/50" aria-hidden="true" />
                              Agent: <span className="font-medium text-foreground">{step.agent}</span>
                            </span>
                          )}
                          {step.duration && (
                            <span className="flex items-center gap-1.5">
                              <Clock className="w-3 h-3" aria-hidden="true" />
                              Durée: <span className="font-medium text-foreground tabular-nums">{step.duration}</span>
                            </span>
                          )}
                          {step.status === "running" && (
                            <span className="flex items-center gap-1.5 text-primary">
                              <Loader2 className="w-3 h-3 animate-spin" aria-hidden="true" />
                              En cours d'exécution...
                            </span>
                          )}
                        </div>

                        {/* Logs preview for completed/error */}
                        {step.logs && step.logs.length > 0 && step.status !== "pending" && (
                          <details className="mt-3 group" open={step.status === "error"}>
                            <summary className="flex items-center gap-2 text-xs font-medium text-muted-foreground cursor-pointer hover:text-foreground transition-colors">
                              <ChevronRight className="w-3 h-3 transition-transform duration-200 group-open:rotate-90" aria-hidden="true" />
                              Logs ({step.logs.length})
                            </summary>
                            <div className="mt-2 p-3 bg-[hsl(var(--muted)/0.5)] rounded-xl font-mono text-[11px] text-muted-foreground/80 max-h-32 overflow-auto">
                              {step.logs.map((log, i) => (
                                <div key={i} className="border-l-2 border-[hsl(var(--primary)/0.3)] pl-2 py-0.5">
                                  {log}
                                </div>
                              ))}
                            </div>
                          </details>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}