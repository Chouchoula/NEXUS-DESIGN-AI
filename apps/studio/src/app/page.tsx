"use client";

import { useState } from "react";
import Link from "next/link";
import {
  LayoutDashboard,
  FolderOpen,
  Lightbulb,
  Palette,
  Bot,
  Plug,
  History,
  Settings,
  Plus,
  Search,
  Filter,
  ChevronDown,
  Sparkles,
  Rocket,
  Zap,
  Eye,
  Code,
  CheckCircle,
  AlertCircle,
  Clock,
  ArrowRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Tableau de bord", href: "/", icon: LayoutDashboard, current: true },
  { name: "Mes projets", href: "/projects", icon: FolderOpen },
  { name: "Inspiration", href: "/inspiration", icon: Lightbulb },
  { name: "Design System", href: "/design-system", icon: Palette },
  { name: "Mes agents", href: "/agents", icon: Bot },
  { name: "Connecteurs", href: "/connectors", icon: Plug },
  { name: "Historique", href: "/history", icon: History },
  { name: "Paramètres", href: "/settings", icon: Settings },
];

const stats = [
  { label: "Projets actifs", value: "12", change: "+3", trend: "up" },
  { label: "Écrans conçus", value: "247", change: "+18", trend: "up" },
  { label: "Composants", value: "89", change: "+5", trend: "up" },
  { label: "Taux de réussite", value: "96%", change: "+2%", trend: "up" },
];

const recentProjects = [
  {
    id: "1",
    name: "MOZIKI - App Communautaire",
    type: "Application mobile",
    status: "in_progress",
    progress: 65,
    lastUpdated: "Il y a 2h",
    avatar: "M",
  },
  {
    id: "2",
    name: "Dashboard Admin SaaS",
    type: "Dashboard",
    status: "review",
    progress: 90,
    lastUpdated: "Hier",
    avatar: "D",
  },
  {
    id: "3",
    name: "Site Vitrine Enterprise",
    type: "Site web",
    status: "completed",
    progress: 100,
    lastUpdated: "Il y a 3j",
    avatar: "S",
  },
  {
    id: "4",
    name: "Identité Visuelle Startup",
    type: "Brand Identity",
    status: "draft",
    progress: 15,
    lastUpdated: "Il y a 1j",
    avatar: "I",
  },
];

const agents: Agent[] = [
  { name: "Research Agent", status: "idle", lastTask: "Benchmark fintech", color: "blue" },
  { name: "Art Director", status: "idle", lastTask: "Direction MOZIKI", color: "purple" },
  { name: "UX Designer", status: "running", lastTask: "Flux utilisateur", color: "green" },
  { name: "UI Designer", status: "idle", lastTask: "Design System v2", color: "orange" },
  { name: "Frontend Engineer", status: "idle", lastTask: "Intégration Dashboard", color: "cyan" },
  { name: "Visual QA", status: "idle", lastTask: "Audit accessibilité", color: "red" },
];

const quickActions = [
  { label: "Nouveau projet", icon: Plus, href: "/projects/new", primary: true },
  { label: "Rechercher inspiration", icon: Search, href: "/inspiration/search" },
  { label: "Créer design system", icon: Palette, href: "/design-system/new" },
  { label: "Lancer un workflow", icon: Rocket, href: "/workflows/new" },
];

function StatusBadge({ status }: { status: string }) {
  const styles = {
    draft: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300",
    in_progress: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
    review: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    completed: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
  };
  const icons = {
    draft: <Clock className="w-3 h-3" />,
    in_progress: <Zap className="w-3 h-3 animate-pulse" />,
    review: <Eye className="w-3 h-3" />,
    completed: <CheckCircle className="w-3 h-3" />,
  };

  return (
    <Badge className={cn("gap-1.5", styles[status as keyof typeof styles] || styles.draft)}>
      {icons[status as keyof typeof icons] || <Clock className="w-3 h-3" />}
      {status.replace("_", " ")}
    </Badge>
  );
}

type AgentStatus = "idle" | "running" | "waiting" | "error";

interface Agent {
  name: string;
  status: AgentStatus;
  lastTask: string;
  color: string;
}

function AgentCard({ agent }: { agent: Agent }) {
  const statusColors: Record<AgentStatus, string> = {
    idle: "bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400",
    running: "bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400",
    waiting: "bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400",
    error: "bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400",
  };

  return (
    <Card className="p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 rounded-lg flex items-center justify-center"
            style={{ backgroundColor: `var(--color-${agent.color}-500)` }}
          >
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="font-medium text-sm">{agent.name}</p>
            <p className="text-xs text-muted-foreground">{agent.lastTask}</p>
          </div>
        </div>
        <Badge variant="secondary" className={statusColors[agent.status]}>
          {agent.status === "running" && <span className="w-1.5 h-1.5 rounded-full bg-current mr-1.5 animate-pulse" />}
          {agent.status}
        </Badge>
      </div>
      <div className="h-1.5 bg-muted rounded-full overflow-hidden">
        <div
          className="h-full bg-primary rounded-full transition-all duration-500"
          style={{ width: agent.status === "running" ? "45%" : "0%" }}
        />
      </div>
    </Card>
  );
}

export default function Dashboard() {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="fixed inset-y-0 left-0 z-50 w-64 bg-card border-r hidden lg:block">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center gap-3 px-6 py-5 border-b">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="font-bold text-lg">NEXUS DESIGN AI</h1>
              <p className="text-xs text-muted-foreground">Studio autonome</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                  item.current
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
              >
                <item.icon className="w-5 h-5" />
                {item.name}
              </Link>
            ))}
          </nav>

          {/* User */}
          <div className="p-3 border-t">
            <div className="flex items-center gap-3">
              <Avatar>
                <AvatarFallback className="bg-primary text-primary-foreground">U</AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">Utilisateur</p>
                <p className="text-xs text-muted-foreground truncate">plan@nexus.design</p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 min-h-screen">
        {/* Top Bar */}
        <header className="sticky top-0 z-40 bg-background/95 backdrop-blur border-b">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center gap-4">
              <h2 className="text-2xl font-bold">Tableau de bord</h2>
              <Badge variant="secondary" className="text-xs">
                <Sparkles className="w-3 h-3 mr-1" />
                v1.0.0 Beta
              </Badge>
            </div>

            <div className="flex items-center gap-4">
              <div className="hidden md:block relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Rechercher projets, assets, agents..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 w-80"
                />
              </div>

              <Button variant="ghost" size="icon" className="relative">
                <Filter className="w-5 h-5" />
              </Button>

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                    <Avatar className="h-10 w-10">
                      <AvatarFallback className="bg-primary text-primary-foreground">U</AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <div className="px-3 py-2 border-b">
                    <p className="font-medium text-sm">Utilisateur</p>
                    <p className="text-xs text-muted-foreground">plan@nexus.design</p>
                  </div>
                  <DropdownMenuItem>Profil</DropdownMenuItem>
                  <DropdownMenuItem>Paramètres</DropdownMenuItem>
                  <DropdownMenuItem>Facturation</DropdownMenuItem>
                  <Separator />
                  <DropdownMenuItem className="text-destructive">Déconnexion</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6 space-y-6">
          {/* Quick Actions */}
          <div className="flex flex-wrap gap-3">
            {quickActions.map((action) => (
              <Button
                key={action.label}
                asChild
                className={cn(action.primary && "bg-primary text-primary-foreground hover:bg-primary/90")}
                size="lg"
              >
                <Link href={action.href}>
                  <action.icon className="w-5 h-5 mr-2" />
                  {action.label}
                </Link>
              </Button>
            ))}
          </div>

          {/* Stats Grid */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {stats.map((stat) => (
              <Card key={stat.label}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
                      <p className="text-3xl font-bold mt-1">{stat.value}</p>
                    </div>
                    <div
                      className={cn(
                        "flex items-center gap-1 text-sm font-medium",
                        stat.trend === "up" ? "text-green-600" : "text-red-600"
                      )}
                    >
                      <ArrowRight className="w-4 h-4" />
                      {stat.change}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Main Grid */}
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Recent Projects */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                  <CardTitle>Projets récents</CardTitle>
                  <Button variant="ghost" size="sm" asChild>
                    <Link href="/projects">Voir tout</Link>
                  </Button>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentProjects.map((project) => (
                      <Link
                        key={project.id}
                        href={`/projects/${project.id}`}
                        className="flex items-center gap-4 p-4 rounded-lg hover:bg-accent/50 transition-colors group"
                      >
                        <div
                          className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary font-bold"
                        >
                          {project.avatar}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <p className="font-medium truncate">{project.name}</p>
                            <StatusBadge status={project.status} />
                          </div>
                          <p className="text-sm text-muted-foreground">{project.type}</p>
                          <div className="mt-2 flex items-center gap-2">
                            <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                              <div
                                className="h-full bg-primary rounded-full transition-all duration-500"
                                style={{ width: `${project.progress}%` }}
                              />
                            </div>
                            <span className="text-sm font-medium text-muted-foreground w-10 text-right">
                              {project.progress}%
                            </span>
                          </div>
                        </div>
                        <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
                      </Link>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Agents Status */}
            <div>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    Agents spécialisés
                    <Badge variant="outline" className="text-xs">
                      6 agents
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {agents.map((agent) => (
                      <AgentCard key={agent.name} agent={agent} />
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* System Status */}
              <Card className="mt-4">
                <CardHeader>
                  <CardTitle>État du système</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">API Backend</span>
                    <Badge className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Opérationnel
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Base de données</span>
                    <Badge className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Connectée
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Redis Cache</span>
                    <Badge className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Connecté
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Figma API</span>
                    <Badge variant="secondary">
                      Non configuré
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Modèles IA</span>
                    <Badge variant="secondary">
                      3 disponibles
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Workflow Overview */}
          <Card>
            <CardHeader>
              <CardTitle>Workflow typique NEXUS DESIGN AI</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <div className="flex items-center gap-4 px-2 py-4 min-w-[800px]">
                  {[
                    { label: "Analyser", icon: Search, color: "blue", desc: "Comprendre le projet" },
                    { label: "Rechercher", icon: Lightbulb, color: "purple", desc: "Benchmarks & tendances" },
                    { label: "Direction Art.", icon: Palette, color: "pink", desc: "Couleurs, typo, identité" },
                    { label: "UX Design", icon: LayoutDashboard, color: "green", desc: "Architecture, flux" },
                    { label: "UI Design", icon: Eye, color: "orange", desc: "Écrans, composants" },
                    { label: "Valider", icon: CheckCircle, color: "yellow", desc: "Approbation humaine" },
                    { label: "Développer", icon: Code, color: "cyan", desc: "React, Next.js, Tailwind" },
                    { label: "Tester", icon: AlertCircle, color: "red", desc: "QA visuel, accessibilité" },
                    { label: "Livrer", icon: Rocket, color: "indigo", desc: "Code, specs, assets" },
                  ].map((step, index) => (
                    <TooltipProvider key={step.label}>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <div className="flex flex-col items-center gap-2 relative">
                            <div
                              className={cn(
                                "w-14 h-14 rounded-xl flex items-center justify-center",
                                `bg-${step.color}-100 text-${step.color}-600 dark:bg-${step.color}-900/30 dark:text-${step.color}-400`
                              )}
                            >
                              <step.icon className="w-7 h-7" />
                            </div>
                            <span className="text-xs font-medium text-center w-24">{step.label}</span>
                            {index < 8 && (
                              <div className="absolute top-7 left-[calc(50%+28px)] w-[calc(100%-56px)] h-0.5 bg-muted" />
                            )}
                          </div>
                        </TooltipTrigger>
                        <TooltipContent side="bottom" className="w-40">
                          <p className="text-xs">{step.desc}</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}