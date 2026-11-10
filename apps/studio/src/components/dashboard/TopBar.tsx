"use client";

import { useState, useRef, useEffect } from "react";
import { Search, Filter, Sun, Moon, Command, Sparkles, Bell, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { useReducedMotion } from "@/hooks/useReducedMotion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function TopBar() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchFocused, setSearchFocused] = useState(false);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const shouldReduce = useReducedMotion();
  const searchRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        searchRef.current?.focus();
        setShowShortcuts(true);
      }
      if (e.key === "Escape") {
        setShowShortcuts(false);
        searchRef.current?.blur();
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <header className="sticky top-0 z-40 px-4 md:px-6 lg:px-8 py-4">
      <div className="flex items-center justify-between gap-4">
        {/* Page Title */}
        <div className="flex items-center gap-3">
          <h2 className="text-headline font-bold text-foreground tracking-tight">Tableau de bord</h2>
          <span className="glass px-2.5 py-0.5 rounded-full text-xs font-medium text-muted-foreground border-[hsl(var(--glass-border))]">
            <Sparkles className="w-3 h-3 mr-1 inline-block align-middle" aria-hidden="true" />
            v1.0.0 Beta
          </span>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-3">
          {/* Search - Glass floating */}
          <div className="relative hidden md:block group">
            <div
              className={cn(
                "relative transition-all duration-300 ease-spring",
                "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
                "border border-[hsl(var(--glass-border))]",
                "rounded-xl",
                "shadow-[var(--depth-1)]",
                "hover:shadow-[var(--depth-2)]",
                searchFocused && "shadow-[var(--depth-3)] border-primary/30 bg-[hsl(var(--glass-bg)/0.9)]",
                searchFocused && "w-96",
                !searchFocused && "w-72"
              )}
            >
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground transition-all duration-200 group-focus-within:text-primary" aria-hidden="true" />
              <kbd className="hidden absolute -top-6 right-4 px-2 py-1 text-xs bg-[hsl(var(--muted))] text-muted-foreground rounded opacity-0 pointer-events-none transition-opacity group-focus-within:opacity-100 group-focus-within:translate-y-1 group-hover:opacity-100 group-hover:translate-y-1">
                ⌘K
              </kbd>
              <Input
                ref={searchRef}
                placeholder="Rechercher projets, assets, agents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => { setSearchFocused(true); setShowShortcuts(true); }}
                onBlur={() => { setSearchFocused(false); setTimeout(() => setShowShortcuts(false), 200); }}
                className={cn(
                  "pl-12 pr-4 py-2.5 bg-transparent border-0 outline-none placeholder:text-muted-foreground",
                  "text-sm font-medium text-foreground",
                  "w-full"
                )}
              />
            </div>
            {showShortcuts && searchFocused && (
              <div className="absolute top-full left-0 mt-2 w-64 glass-strong rounded-xl p-3 shadow-[var(--depth-3)] animate-slide-down z-50">
                <p className="text-xs font-medium text-muted-foreground mb-2">Raccourcis</p>
                <div className="space-y-1.5 text-sm">
                  <div className="flex justify-between text-muted-foreground"><span>Ouvrir recherche</span><kbd className="px-2 py-0.5 bg-[hsl(var(--muted))] rounded text-foreground font-mono">⌘K</kbd></div>
                  <div className="flex justify-between text-muted-foreground"><span>Nouveau projet</span><kbd className="px-2 py-0.5 bg-[hsl(var(--muted))] rounded text-foreground font-mono">⌘N</kbd></div>
                  <div className="flex justify-between text-muted-foreground"><span>Basculer thème</span><kbd className="px-2 py-0.5 bg-[hsl(var(--muted))] rounded text-foreground font-mono">⌘⇧T</kbd></div>
                  <div className="flex justify-between text-muted-foreground"><span>Ouvrir sidebar</span><kbd className="px-2 py-0.5 bg-[hsl(var(--muted))] rounded text-foreground font-mono">⌘B</kbd></div>
                </div>
              </div>
            )}
          </div>

          {/* Filter Button - Glass */}
          <Button
            variant="ghost"
            size="icon"
            className={cn(
              "relative h-10 w-10 rounded-xl",
              "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
              "border border-[hsl(var(--glass-border))]",
              "text-muted-foreground hover:text-foreground",
              "hover:bg-[hsl(var(--accent)/0.08)] hover:border-[hsl(var(--accent)/0.3)]",
              "transition-all duration-200 ease-out-expo",
              "shadow-[var(--depth-1)]"
            )}
            aria-label="Filtrer"
          >
            <Filter className="w-5 h-5" aria-hidden="true" />
          </Button>

          {/* Theme Toggle - Kinetic morph */}
          <Button
            variant="ghost"
            size="icon"
            className={cn(
              "relative h-10 w-10 rounded-xl",
              "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
              "border border-[hsl(var(--glass-border))]",
              "text-muted-foreground hover:text-foreground",
              "hover:bg-[hsl(var(--primary)/0.08)] hover:border-[hsl(var(--primary)/0.3)]",
              "transition-all duration-300 ease-spring",
              "shadow-[var(--depth-1)]",
              "group"
            )}
            aria-label="Basculer le thème"
          >
            <span className="absolute inset-0 flex items-center justify-center transition-all duration-300 ease-spring rotate-0 scale-100 opacity-100 dark:-rotate-90 dark:scale-0 dark:opacity-0 group-data-[theme=dark]:rotate-90 group-data-[theme=dark]:scale-100 group-data-[theme=dark]:opacity-100">
              <Sun className="w-5 h-5" aria-hidden="true" />
            </span>
            <span className="absolute inset-0 flex items-center justify-center transition-all duration-300 ease-spring rotate-90 scale-0 opacity-0 dark:rotate-0 dark:scale-100 dark:opacity-100 group-data-[theme=dark]:-rotate-90 group-data-[theme=dark]:scale-0 group-data-[theme=dark]:opacity-0">
              <Moon className="w-5 h-5" aria-hidden="true" />
            </span>
          </Button>

          {/* Notifications - Glass with badge */}
          <Button
            variant="ghost"
            size="icon"
            className={cn(
              "relative h-10 w-10 rounded-xl",
              "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
              "border border-[hsl(var(--glass-border))]",
              "text-muted-foreground hover:text-foreground",
              "hover:bg-[hsl(var(--accent)/0.08)] hover:border-[hsl(var(--accent)/0.3)]",
              "transition-all duration-200 ease-out-expo",
              "shadow-[var(--depth-1)]"
            )}
            aria-label="Notifications"
          >
            <Bell className="w-5 h-5" aria-hidden="true" />
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-destructive text-destructive-foreground text-[10px] font-bold rounded-full flex items-center justify-center animate-pulse-glow" aria-label="3 notifications">
              3
            </span>
          </Button>

          {/* User Menu - Glass dropdown */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                className={cn(
                  "relative h-10 w-10 rounded-xl pr-3",
                  "bg-[hsl(var(--glass-bg))] backdrop-blur-[20px] backdrop-saturate-[180%]",
                  "border border-[hsl(var(--glass-border))]",
                  "transition-all duration-200 ease-out-expo",
                  "hover:bg-[hsl(var(--primary)/0.08)] hover:border-[hsl(var(--primary)/0.3)]",
                  "shadow-[var(--depth-1)]"
                )}
                aria-label="Menu utilisateur"
              >
                <Avatar className="h-10 w-10">
                  <AvatarFallback className="bg-gradient-to-br from-primary to-electric text-primary-foreground">
                    U
                  </AvatarFallback>
                </Avatar>
                <ChevronDown className="w-4 h-4 ml-2 text-muted-foreground transition-transform duration-200 group-open:rotate-180" aria-hidden="true" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              align="end"
              className={cn(
                "w-56 glass-strong rounded-2xl border-[hsl(var(--glass-border))]",
                "shadow-[var(--depth-3)]",
                "animate-scale-in",
                !shouldReduce && "animate-slide-down"
              )}
            >
              <div className="px-3 py-2 border-b border-[hsl(var(--glass-border))]">
                <p className="font-medium text-sm text-foreground">Utilisateur</p>
                <p className="text-xs text-muted-foreground truncate">plan@nexus.design</p>
              </div>
              <DropdownMenuItem className="text-foreground hover:bg-[hsl(var(--accent)/0.08)]">
                <span className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                  Profil
                </span>
              </DropdownMenuItem>
              <DropdownMenuItem className="text-foreground hover:bg-[hsl(var(--accent)/0.08)]">
                <span className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                  Paramètres
                </span>
              </DropdownMenuItem>
              <DropdownMenuItem className="text-foreground hover:bg-[hsl(var(--accent)/0.08)]">
                <span className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  Facturation
                </span>
              </DropdownMenuItem>
              <DropdownMenuSeparator className="border-[hsl(var(--glass-border))] my-1" />
              <DropdownMenuItem className="text-destructive hover:bg-[hsl(var(--destructive)/0.08)]">
                <span className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                  Déconnexion
                </span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}