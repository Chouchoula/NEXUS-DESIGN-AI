"use client";

import { Plus, Zap, FolderOpen, Lightbulb, Palette, Bot, Sparkles, ArrowRight, Settings, Download, Upload, Share2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface QuickAction {
  id: string;
  label: string;
  description: string;
  icon: React.ElementType;
  variant: "primary" | "secondary" | "ghost" | "brutal" | "clay" | "glass";
  gradient?: string;
  shortcut?: string;
  onClick?: () => void;
  disabled?: boolean;
  badge?: string;
  badgeColor?: "success" | "warning" | "destructive" | "primary";
}

interface QuickActionsProps {
  title?: string;
  actions?: QuickAction[];
  className?: string;
}

const defaultActions: QuickAction[] = [
  {
    id: "new-project",
    label: "Nouveau projet",
    description: "Créer un projet de design",
    icon: Plus,
    variant: "brutal",
    gradient: "from-primary to-electric",
    shortcut: "⌘N",
    badge: "Nouveau",
    badgeColor: "primary",
  },
  {
    id: "run-workflow",
    label: "Lancer workflow",
    description: "Exécuter un pipeline d'agents",
    icon: Zap,
    variant: "primary",
    gradient: "from-electric to-primary",
    shortcut: "⌘⇧W",
    badge: "Populaire",
    badgeColor: "success",
  },
  {
    id: "browse-projects",
    label: "Mes projets",
    description: "Voir tous vos projets",
    icon: FolderOpen,
    variant: "glass",
    shortcut: "⌘P",
  },
  {
    id: "inspiration",
    label: "Inspiration",
    description: "Découvrir des designs",
    icon: Lightbulb,
    variant: "clay",
    gradient: "from-warning to-orange-500",
  },
  {
    id: "design-system",
    label: "Design System",
    description: "Gérer vos tokens",
    icon: Palette,
    variant: "secondary",
    shortcut: "⌘D",
  },
  {
    id: "agents",
    label: "Mes agents",
    description: "Configurer les agents IA",
    icon: Bot,
    variant: "ghost",
    shortcut: "⌘A",
  },
];

const variantStyles = {
  primary: "bg-gradient-to-br from-primary to-electric text-primary-foreground hover:from-primary/90 hover:to-electric/90 shadow-[var(--depth-2)] hover:shadow-[var(--depth-3)]",
  secondary: "bg-[hsl(var(--secondary))] text-secondary-foreground hover:bg-[hsl(var(--secondary)/0.8)] border border-[hsl(var(--border))]",
  ghost: "bg-transparent hover:bg-[hsl(var(--accent)/0.08)] text-foreground border border-[hsl(var(--glass-border))]",
  brutal: "bg-[hsl(var(--background))] text-foreground border-2 border-[hsl(var(--foreground))] hover:bg-[hsl(var(--foreground))] hover:text-[hsl(var(--background))] hover:border-[hsl(var(--foreground))] shadow-[4px_4px_0px_0px_hsl(var(--foreground))] hover:shadow-[6px_6px_0px_0px_hsl(var(--foreground))] transition-all duration-200 ease-out-expo",
  clay: "bg-[hsl(var(--background))] text-foreground border-0 shadow-[var(--clay-shadow)] hover:shadow-[var(--clay-shadow-hover)] active:shadow-[var(--clay-shadow-active)] transition-all duration-200 ease-out-expo",
  glass: "glass-card bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%] border border-[hsl(var(--glass-border))] text-foreground hover:border-[hsl(var(--glass-border)/0.9)] hover:shadow-[var(--depth-2)] transition-all duration-200 ease-out-expo",
};

export function QuickActions({ title = "Actions rapides", actions = defaultActions, className }: QuickActionsProps) {
  const shouldReduce = useReducedMotion();

  return (
    <section className={cn("animate-slide-up", className)} aria-labelledby="quick-actions-heading">
      <h2 id="quick-actions-heading" className="text-headline font-bold text-foreground mb-6">
        {title}
      </h2>

      <TooltipProvider>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3" role="list" aria-label="Actions rapides">
          {actions.map((action, index) => {
            const Icon = action.icon;
            const isBrutal = action.variant === "brutal";
            const isClay = action.variant === "clay";
            const hasGradient = action.gradient;

            return (
              <Tooltip key={action.id} delayDuration={200}>
                <TooltipTrigger asChild>
                  <Button
                    type="button"
                    onClick={action.onClick}
                    disabled={action.disabled}
                    className={cn(
                      "relative overflow-hidden group h-28 md:h-32 flex flex-col items-center justify-center gap-3 p-4 text-center",
                      "rounded-2xl font-medium transition-all duration-300 ease-spring",
                      "focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background",
                      "disabled:opacity-50 disabled:cursor-not-allowed",
                      variantStyles[action.variant],
                      !shouldReduce && `stagger-${(index % 8) + 1}`,
                      isBrutal && "hover:-translate-y-1 hover:translate-x-[-2px]",
                      isClay && "active:translate-y-1 active:translate-x-[2px]",
                      !isBrutal && !isClay && "hover:-translate-y-1 hover:shadow-[var(--depth-3)]"
                    )}
                    style={{
                      animationDelay: `${index * 60}ms`,
                      ...(hasGradient && action.variant === "primary" && {
                        background: `linear-gradient(135deg, ${hasGradient.split(" ")[1]}, ${hasGradient.split(" ")[3]})`,
                      }),
                    }}
                    role="listitem"
                    aria-label={`${action.label}${action.shortcut ? `, raccourci ${action.shortcut}` : ""}`}
                  >
                    {/* Gradient overlay for primary/brutal variants */}
                    {(action.variant === "primary" || action.variant === "brutal") && hasGradient && (
                      <div
                        className="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                        style={{ background: `linear-gradient(135deg, ${hasGradient.split(" ")[1]}, ${hasGradient.split(" ")[3]})` }}
                        aria-hidden="true"
                      />
                    )}

                    {/* Background depth orb */}
                    <div className="absolute top-2 right-2 w-12 h-12 bg-primary/10 rounded-full blur-2xl pointer-events-none group-hover:scale-150 transition-transform duration-500" aria-hidden="true" />

                    {/* Icon */}
                    <div
                      className={cn(
                        "relative z-10 w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300 ease-spring",
                        "group-hover:scale-110",
                        action.variant === "primary" && "bg-[hsl(var(--primary-foreground)/0.15)] text-primary",
                        action.variant === "secondary" && "bg-[hsl(var(--primary)/0.12)] text-primary",
                        action.variant === "ghost" && "bg-[hsl(var(--primary)/0.1)] text-primary",
                        action.variant === "brutal" && "bg-[hsl(var(--foreground)/0.1)] text-foreground group-hover:bg-[hsl(var(--foreground))] group-hover:text-[hsl(var(--background))]",
                        action.variant === "clay" && "bg-[hsl(var(--primary)/0.1)] text-primary",
                        action.variant === "glass" && "bg-[hsl(var(--primary)/0.1)] text-primary"
                      )}
                    >
                      <Icon className="w-6 h-6" aria-hidden="true" />
                    </div>

                    {/* Label & Badge */}
                    <div className="relative z-10 flex flex-col items-center gap-1 w-full">
                      <span className="text-sm font-semibold leading-tight truncate max-w-full">
                        {action.label}
                      </span>

                      {action.badge && (
                        <Badge
                          variant="outline"
                          className={cn(
                            "gap-1 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider",
                            action.badgeColor === "success" && "text-success bg-success/10 border-success/20",
                            action.badgeColor === "warning" && "text-warning bg-warning/10 border-warning/20",
                            action.badgeColor === "destructive" && "text-destructive bg-destructive/10 border-destructive/20",
                            action.badgeColor === "primary" && "text-primary bg-primary/10 border-primary/20"
                          )}
                        >
                          {action.badge}
                        </Badge>
                      )}

                      {action.shortcut && (
                        <kbd className="relative z-10 px-2 py-0.5 text-[10px] font-mono bg-[hsl(var(--muted)/0.5)] rounded text-muted-foreground/70 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                          {action.shortcut}
                        </kbd>
                      )}
                    </div>

                    {/* Arrow indicator */}
                    <ArrowRight className="relative z-10 w-4 h-4 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all duration-200 ease-out-expo" aria-hidden="true" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top" align="start" className="glass-strong rounded-xl border-[hsl(var(--glass-border))] shadow-[var(--depth-3)] p-3 animate-scale-in">
                  <p className="font-medium text-sm text-foreground">{action.label}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{action.description}</p>
                  {action.shortcut && (
                    <p className="text-[10px] text-muted-foreground/70 mt-1 font-mono">Raccourci: {action.shortcut}</p>
                  )}
                </TooltipContent>
              </Tooltip>
            );
          })}
        </div>
      </TooltipProvider>
    </section>
  );
}