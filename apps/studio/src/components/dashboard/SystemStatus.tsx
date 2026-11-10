"use client";

import { Cpu, HardDrive, Wifi, Server, Zap, Database, CheckCircle, AlertTriangle, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { Badge } from "@/components/ui/badge";

interface MetricItem {
  name: string;
  value: string;
  unit: string;
  icon: React.ElementType;
  status: "healthy" | "warning" | "critical";
  trend?: "up" | "down" | "stable";
  description: string;
}

interface SystemStatusProps {
  metrics?: MetricItem[];
  className?: string;
}

const defaultMetrics: MetricItem[] = [
  {
    name: "CPU",
    value: "24",
    unit: "%",
    icon: Cpu,
    status: "healthy",
    trend: "stable",
    description: "Utilisation normale",
  },
  {
    name: "Mémoire",
    value: "68",
    unit: "%",
    icon: HardDrive,
    status: "healthy",
    trend: "up",
    description: "Dans les normes",
  },
  {
    name: "Réseau",
    value: "1.2",
    unit: "Gbps",
    icon: Wifi,
    status: "healthy",
    trend: "stable",
    description: "Débit stable",
  },
  {
    name: "API Latence",
    value: "42",
    unit: "ms",
    icon: Server,
    status: "healthy",
    trend: "down",
    description: "Performance optimale",
  },
  {
    name: "File d'attente",
    value: "3",
    unit: "jobs",
    icon: Database,
    status: "warning",
    trend: "up",
    description: "En augmentation",
  },
  {
    name: "Taux d'erreur",
    value: "0.02",
    unit: "%",
    icon: Zap,
    status: "healthy",
    trend: "stable",
    description: "Negligeable",
  },
];

const statusConfig = {
  healthy: { color: "text-success bg-success/10 border-success/20", icon: CheckCircle, label: "Sain" },
  warning: { color: "text-warning bg-warning/10 border-warning/20", icon: AlertTriangle, label: "Attention" },
  critical: { color: "text-destructive bg-destructive/10 border-destructive/20", icon: XCircle, label: "Critique" },
};

export function SystemStatus({ metrics = defaultMetrics, className }: SystemStatusProps) {
  const shouldReduce = useReducedMotion();

  return (
    <section className={cn("animate-slide-up", className)} aria-labelledby="system-status-heading">
      <div className="flex items-center justify-between mb-6">
        <h2 id="system-status-heading" className="text-headline font-bold text-foreground">
          État du système
        </h2>
        <Badge variant="outline" className="gap-1.5 px-2.5 py-1 text-xs font-medium text-success bg-success/10 border-success/20">
          <CheckCircle className="w-3 h-3" aria-hidden="true" />
          Tous systèmes opérationnels
        </Badge>
      </div>

      <div
        className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3"
        role="list"
        aria-label="Métriques système"
      >
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          const config = statusConfig[metric.status];
          const StatusIcon = config.icon;
          const trendIcon = metric.trend === "up" ? "↗" : metric.trend === "down" ? "↘" : "→";

          return (
            <article
              key={metric.name}
              className={cn(
                "relative group overflow-hidden rounded-2xl p-4",
                "glass-card",
                "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
                "border border-[hsl(var(--glass-border))]",
                "transition-all duration-300 ease-out-expo",
                "hover:shadow-[var(--depth-3)] hover:border-[hsl(var(--glass-border)/0.9)] hover:-translate-y-0.5",
                "animate-slide-up",
                !shouldReduce && `stagger-${(index % 8) + 1}`
              )}
              style={{ animationDelay: `${index * 50}ms` }}
              role="listitem"
            >
              {/* Brutal top accent border */}
              <div
                className={cn(
                  "absolute top-0 left-0 right-0 h-1 rounded-t-2xl",
                  metric.status === "healthy" && "bg-gradient-to-r from-success to-green-400",
                  metric.status === "warning" && "bg-gradient-to-r from-warning to-yellow-400",
                  metric.status === "critical" && "bg-gradient-to-r from-destructive to-orange-500"
                )}
                aria-hidden="true"
              />

              {/* Background depth orb */}
              <div className="absolute top-2 right-2 w-12 h-12 bg-primary/5 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />

              <div className="relative flex flex-col h-full">
                {/* Header: Icon + Status */}
                <div className="flex items-start justify-between mb-3">
                  <div
                    className={cn(
                      "w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0",
                      "bg-[hsl(var(--primary)/0.12)] text-primary"
                    )}
                  >
                    <Icon className="w-5 h-5" aria-hidden="true" />
                  </div>
                  <Badge
                    variant="outline"
                    className={cn(
                      "gap-1 px-2 py-0.5 text-[10px] font-medium",
                      config.color,
                      "border-[hsl(var(--glass-border))]",
                      "shadow-[var(--depth-1)]"
                    )}
                  >
                    <StatusIcon className="w-2.5 h-2.5" aria-hidden="true" />
                    {config.label}
                  </Badge>
                </div>

                {/* Value */}
                <div className="flex-1 flex flex-col justify-between mb-3">
                  <div>
                    <div className="flex items-baseline gap-1">
                      <span className="text-display font-bold text-foreground tabular-nums">{metric.value}</span>
                      <span className="text-sm text-muted-foreground font-medium">{metric.unit}</span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1 truncate">{metric.name}</p>
                  </div>

                  {/* Trend indicator */}
                  {metric.trend && (
                    <div className="flex items-center gap-1">
                      <span
                        className={cn(
                          "text-[10px] font-bold",
                          metric.trend === "up" && "text-success",
                          metric.trend === "down" && "text-destructive",
                          metric.trend === "stable" && "text-muted-foreground"
                        )}
                        aria-label={`Tendance ${metric.trend === "up" ? "hausse" : metric.trend === "down" ? "baisse" : "stable"}`}
                      >
                        {trendIcon}
                      </span>
                      <span className="text-[10px] text-muted-foreground">{metric.trend === "up" ? "+" : metric.trend === "down" ? "" : "~"}vs préc.</span>
                    </div>
                  )}
                </div>

                {/* Description */}
                <p className="text-xs text-muted-foreground/80">{metric.description}</p>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}