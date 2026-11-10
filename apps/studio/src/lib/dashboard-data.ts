/**
 * Dashboard data - Centralized data for the NEXUS DESIGN AI dashboard
 * This file provides mock data that can be replaced with real API calls
 */

import { Clock, Zap, FolderOpen, Lightbulb, Palette, Bot, Plug, History, Settings, CheckCircle, AlertTriangle, XCircle, Activity, Sparkles, Cpu, HardDrive, Wifi, Server, Database, Plus } from "lucide-react";

export interface StatData {
  label: string;
  value: string | number;
  change: string;
  trend: "up" | "down" | "neutral";
  icon: React.ElementType;
  delay: number;
}

export interface ProjectData {
  id: string;
  name: string;
  type: string;
  status: "draft" | "in_progress" | "review" | "completed";
  progress: number;
  lastUpdated: string;
  avatar: string;
  delay: number;
}

export interface AgentData {
  id: string;
  name: string;
  type: string;
  status: "idle" | "running" | "completed" | "error" | "pending";
  progress: number;
  description: string;
  lastRun?: string;
  avatar?: string;
  color?: string;
  delay: number;
}

export interface SystemMetric {
  name: string;
  value: string;
  unit: string;
  icon: React.ElementType;
  status: "healthy" | "warning" | "critical";
  trend?: "up" | "down" | "stable";
  description: string;
}

export interface WorkflowStep {
  id: string;
  name: string;
  description: string;
  status: "pending" | "running" | "completed" | "error" | "skipped";
  duration?: string;
  agent?: string;
  logs?: string[];
}

export interface QuickActionData {
  id: string;
  label: string;
  description: string;
  icon: React.ElementType;
  variant: "primary" | "secondary" | "ghost" | "brutal" | "clay" | "glass";
  gradient?: string;
  shortcut?: string;
  badge?: string;
  badgeColor?: "success" | "warning" | "destructive" | "primary";
}

/**
 * Stats cards data
 */
export const statsData: StatData[] = [
  {
    label: "Projets actifs",
    value: 24,
    change: "+12% ce mois",
    trend: "up",
    icon: FolderOpen,
    delay: 0,
  },
  {
    label: "Workflows exécutés",
    value: 156,
    change: "+8% cette semaine",
    trend: "up",
    icon: Zap,
    delay: 100,
  },
  {
    label: "Agents en cours",
    value: 7,
    change: "2 en attente",
    trend: "neutral",
    icon: Bot,
    delay: 200,
  },
  {
    label: "Taux de succès",
    value: "98.2%",
    change: "+0.3% vs mois dernier",
    trend: "up",
    icon: CheckCircle,
    delay: 300,
  },
];

/**
 * Projects data
 */
export const projectsData: ProjectData[] = [
  {
    id: "proj-1",
    name: "Redesign E-commerce",
    type: "Design System",
    status: "in_progress",
    progress: 68,
    lastUpdated: "Il y a 2h",
    avatar: "R",
    delay: 0,
  },
  {
    id: "proj-2",
    name: "Dashboard Analytics",
    type: "Application",
    status: "review",
    progress: 92,
    lastUpdated: "Il y a 4h",
    avatar: "D",
    delay: 100,
  },
  {
    id: "proj-3",
    name: "Mobile App Onboarding",
    type: "Mobile Design",
    status: "completed",
    progress: 100,
    lastUpdated: "Hier",
    avatar: "M",
    delay: 200,
  },
  {
    id: "proj-4",
    name: "Brand Identity Kit",
    type: "Branding",
    status: "in_progress",
    progress: 45,
    lastUpdated: "Il y a 30min",
    avatar: "B",
    delay: 300,
  },
  {
    id: "proj-5",
    name: "Design Tokens Audit",
    type: "Design System",
    status: "draft",
    progress: 12,
    lastUpdated: "Il y a 1j",
    avatar: "T",
    delay: 400,
  },
  {
    id: "proj-6",
    name: "Component Library v2",
    type: "Design System",
    status: "completed",
    progress: 100,
    lastUpdated: "Il y a 2j",
    avatar: "C",
    delay: 500,
  },
];

/**
 * Agents data
 */
export const agentsData: AgentData[] = [
  {
    id: "agent-1",
    name: "Researcher",
    type: "researcher",
    status: "completed",
    progress: 100,
    description: "Analyse concurrentielle et tendances design",
    lastRun: "Il y a 15min",
    color: "#8B5CF6",
    delay: 0,
  },
  {
    id: "agent-2",
    name: "Planner",
    type: "planner",
    status: "running",
    progress: 67,
    description: "Planification sprint et allocation ressources",
    lastRun: "En cours",
    color: "#3B82F6",
    delay: 100,
  },
  {
    id: "agent-3",
    name: "Designer",
    type: "designer",
    status: "idle",
    progress: 0,
    description: "Génération maquettes et variations UI",
    color: "#EC4899",
    delay: 200,
  },
  {
    id: "agent-4",
    name: "Developer",
    type: "developer",
    status: "pending",
    progress: 23,
    description: "Génération code React/TypeScript",
    lastRun: "Planifié",
    color: "#10B981",
    delay: 300,
  },
  {
    id: "agent-5",
    name: "Reviewer",
    type: "reviewer",
    status: "error",
    progress: 0,
    description: "Revue code et accessibilité",
    lastRun: "Échoué il y a 1h",
    color: "#F59E0B",
    delay: 400,
  },
];

/**
 * System metrics data
 */
export const systemMetrics: SystemMetric[] = [
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
    icon: Sparkles,
    status: "healthy",
    trend: "stable",
    description: "Négligeable",
  },
];

/**
 * Workflow timeline data
 */
export const workflowSteps: WorkflowStep[] = [
  {
    id: "step-1",
    name: "Analyse du brief",
    description: "Compréhension des objectifs, contraintes et publics cibles",
    status: "completed",
    duration: "2m 34s",
    agent: "Researcher",
    logs: [
      "[INFO] Brief reçu: Redesign E-commerce",
      "[INFO] 12 concurrents identifiés",
      "[INFO] 47 patterns design extraits",
      "[SUCCESS] Analyse terminée",
    ],
  },
  {
    id: "step-2",
    name: "Recherche d'inspiration",
    description: "Collecte de références visuelles et tendances actuelles",
    status: "completed",
    duration: "1m 12s",
    agent: "Researcher",
    logs: [
      "[INFO] Recherche sur Dribbble, Behance, Pinterest",
      "[INFO] 89 références collectées",
      "[INFO] Catégorisées par style: Glassmorphism, Neo-brutalism, Clay",
      "[SUCCESS] Moodboard généré",
    ],
  },
  {
    id: "step-3",
    name: "Planification architecture",
    description: "Définition de la structure, composants et flux utilisateur",
    status: "running",
    duration: "En cours...",
    agent: "Planner",
    logs: [
      "[INFO] Structure sitemap créée",
      "[INFO] 8 écrans principaux définis",
      "[INFO] Flux utilisateur: 5 parcours critiques",
      "[WARN] Dépendance composant 'DataTable' non résolue",
    ],
  },
  {
    id: "step-4",
    name: "Design System Setup",
    description: "Création tokens, couleurs, typographie, composants de base",
    status: "pending",
    agent: "Designer",
  },
  {
    id: "step-5",
    name: "Maquettes haute fidélité",
    description: "Design des écrans principaux avec tous les états",
    status: "pending",
    agent: "Designer",
  },
  {
    id: "step-6",
    name: "Génération code React",
    description: "Conversion designs → composants TypeScript/React",
    status: "pending",
    agent: "Developer",
  },
  {
    id: "step-7",
    name: "Revue accessibilité",
    description: "Audit WCAG 2.2, contrastes, navigation clavier",
    status: "pending",
    agent: "Reviewer",
  },
  {
    id: "step-8",
    name: "Livraison & Documentation",
    description: "Package final, Storybook, guide d'utilisation",
    status: "pending",
    agent: "Planner",
  },
];

/**
 * Quick actions data
 */
export const quickActionsData: QuickActionData[] = [
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

/**
 * Navigation items
 */
export const navigationItems = [
  { name: "Tableau de bord", href: "/", icon: LayoutDashboard },
  { name: "Mes projets", href: "/projects", icon: FolderOpen },
  { name: "Inspiration", href: "/inspiration", icon: Lightbulb },
  { name: "Design System", href: "/design-system", icon: Palette },
  { name: "Mes agents", href: "/agents", icon: Bot },
  { name: "Connecteurs", href: "/connectors", icon: Plug },
  { name: "Historique", href: "/history", icon: History },
  { name: "Paramètres", href: "/settings", icon: Settings },
];

// Re-export icons for convenience
import { LayoutDashboard } from "lucide-react";
export { LayoutDashboard, Clock, Zap, FolderOpen, Lightbulb, Palette, Bot, Plug, History, Settings, CheckCircle, AlertTriangle, XCircle, Activity, Sparkles, Cpu, HardDrive, Wifi, Server, Database };