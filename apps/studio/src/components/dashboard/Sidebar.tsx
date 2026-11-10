"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  FolderOpen,
  Lightbulb,
  Palette,
  Bot,
  Plug,
  History,
  Settings,
  Sparkles,
  ChevronRight,
  ChevronLeft,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

const navigation = [
  { name: "Tableau de bord", href: "/", icon: LayoutDashboard },
  { name: "Mes projets", href: "/projects", icon: FolderOpen },
  { name: "Inspiration", href: "/inspiration", icon: Lightbulb },
  { name: "Design System", href: "/design-system", icon: Palette },
  { name: "Mes agents", href: "/agents", icon: Bot },
  { name: "Connecteurs", href: "/connectors", icon: Plug },
  { name: "Historique", href: "/history", icon: History },
  { name: "Paramètres", href: "/settings", icon: Settings },
];

export function Sidebar({
  collapsed,
  onToggle,
}: {
  collapsed: boolean;
  onToggle: (collapsed: boolean) => void;
}) {
  const pathname = usePathname();
  const shouldReduce = useReducedMotion();
  const [isHovered, setIsHovered] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const effectiveCollapsed = collapsed && !isHovered;

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-50 transition-all duration-350 ease-spring",
        "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%] border-r border-[hsl(var(--glass-border))]",
        "shadow-[var(--depth-2)]",
        effectiveCollapsed ? "w-18" : "w-70",
        !mounted && "w-18"
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      aria-label="Navigation principale"
    >
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div
          className={cn(
            "flex items-center gap-3 px-4 py-5 border-b border-[hsl(var(--glass-border))]",
            "transition-all duration-350 ease-spring",
            effectiveCollapsed && "justify-center px-0"
          )}
        >
          <div
            className={cn(
              "relative w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0",
              "bg-gradient-to-br from-primary to-electric",
              "shadow-[0_0_20px_hsl(var(--warm-glow))]",
              "transition-all duration-300 ease-out-expo",
              "group-hover:scale-105 group-hover:rotate-3"
            )}
          >
            <Sparkles className="w-6 h-6 text-primary-foreground" aria-hidden="true" />
            {!shouldReduce && (
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-accent rounded-full animate-pulse-glow" aria-hidden="true" />
            )}
          </div>
          {!effectiveCollapsed && (
            <div className={cn(
              "overflow-hidden transition-all duration-350 ease-spring",
              "group"
            )}>
              <h1 className="font-bold text-lg text-foreground whitespace-nowrap">NEXUS DESIGN AI</h1>
              <p className="text-xs text-muted-foreground whitespace-nowrap">Studio autonome</p>
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto" aria-label="Navigation">
          {navigation.map((item, index) => {
            const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "relative flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ease-out-expo",
                  "group",
                  isActive
                    ? "bg-[hsl(var(--primary)/0.12)] text-primary"
                    : "text-muted-foreground hover:bg-[hsl(var(--accent)/0.08)] hover:text-accent-foreground",
                  effectiveCollapsed && "justify-center px-0"
                )}
                aria-current={isActive ? "page" : undefined}
                title={effectiveCollapsed ? item.name : undefined}
              >
                <item.icon
                  className={cn(
                    "w-5 h-5 flex-shrink-0 transition-transform duration-200 ease-out-expo",
                    isActive && "text-primary",
                    "group-hover:scale-110"
                  )}
                  aria-hidden="true"
                />
                {!effectiveCollapsed && (
                  <span className={cn(
                    "truncate transition-all duration-200 ease-out-expo",
                    "opacity-100",
                    "group-hover:translate-x-0.5"
                  )}>
                    {item.name}
                  </span>
                )}
                {isActive && !effectiveCollapsed && (
                  <div
                    className={cn(
                      "absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 rounded-r-full",
                      "bg-primary",
                      !shouldReduce && "animate-scale-in"
                    )}
                    aria-hidden="true"
                  />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Toggle & User */}
        <div className="p-3 border-t border-[hsl(var(--glass-border))]">
          <div className="flex items-center gap-3">
            {!effectiveCollapsed && (
              <Avatar className="h-10 w-10">
                <AvatarFallback className="bg-gradient-to-br from-primary to-electric text-primary-foreground">
                  U
                </AvatarFallback>
              </Avatar>
            )}
            <div className={cn(
              "flex-1 min-w-0 transition-all duration-350 ease-spring",
              effectiveCollapsed && "overflow-hidden w-0"
            )}>
              <p className="text-sm font-medium truncate text-foreground">Utilisateur</p>
              <p className="text-xs text-muted-foreground truncate">plan@nexus.design</p>
            </div>
            <button
              onClick={() => onToggle(!collapsed)}
              className={cn(
                "relative flex h-8 w-8 items-center justify-center rounded-lg",
                "bg-[hsl(var(--secondary))] text-muted-foreground",
                "hover:bg-[hsl(var(--accent)/0.12)] hover:text-accent-foreground",
                "transition-all duration-200 ease-out-expo",
                "group",
                effectiveCollapsed && "mx-auto"
              )}
              aria-label={collapsed ? "Étendre la barre latérale" : "Réduire la barre latérale"}
              aria-expanded={!collapsed}
            >
              {collapsed ? (
                <ChevronRight className="w-5 h-5 transition-transform duration-200 group-hover:translate-x-1" />
              ) : (
                <ChevronLeft className="w-5 h-5 transition-transform duration-200 group-hover:-translate-x-1" />
              )}
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}