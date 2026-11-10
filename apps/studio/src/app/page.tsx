"use client";

import { useState } from "react";
import { Sidebar } from "@/components/dashboard/Sidebar";
import { TopBar } from "@/components/dashboard/TopBar";
import { StatCard } from "@/components/dashboard/StatCard";
import { ProjectCard } from "@/components/dashboard/ProjectCard";
import { AgentCard } from "@/components/dashboard/AgentCard";
import { SystemStatus } from "@/components/dashboard/SystemStatus";
import { WorkflowTimeline } from "@/components/dashboard/WorkflowTimeline";
import { QuickActions } from "@/components/dashboard/QuickActions";
import {
  statsData,
  projectsData,
  agentsData,
  systemMetrics,
  workflowSteps,
  quickActionsData,
} from "@/lib/dashboard-data";
import { FolderOpen, Zap, Bot, CheckCircle, ArrowRight, Sparkles, Plus, Badge } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge as BadgeComponent } from "@/components/ui/badge";

export default function Dashboard() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className="min-h-screen bg-[hsl(var(--background))]">
      {/* Background atmospheric orbs */}
      <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden" aria-hidden="true">
        <div className="orb-1" />
        <div className="orb-2" />
        <div className="orb-3" />
        {/* Subtle grid pattern overlay */}
        <div className="absolute inset-0 bg-grid-subtle opacity-50" />
      </div>

      {/* Sidebar */}
      <Sidebar collapsed={sidebarCollapsed} onToggle={setSidebarCollapsed} />

      {/* Main Content */}
      <main className={cn("transition-all duration-350 ease-spring", sidebarCollapsed ? "ml-18" : "ml-70")} style={{ minHeight: "100vh" }}>
        {/* Top Bar */}
        <TopBar />

        {/* Page Content */}
        <div className="p-4 md:p-6 lg:p-8 space-y-8 animate-slide-up">
          {/* Page Header */}
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-2">
            <div>
              <h1 className="text-display font-bold text-foreground tracking-tight">Tableau de bord</h1>
              <p className="text-muted-foreground mt-1">Vue d'ensemble de votre studio de design autonome</p>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="ghost" size="icon" className="h-10 w-10 rounded-xl glass border-[hsl(var(--glass-border))]">
                <Sparkles className="w-5 h-5 text-primary" />
              </Button>
              <Button asChild className="brutal gap-2 px-4 py-2">
                <Link href="/projects/new">
                  <Plus className="w-4 h-4" />
                  Nouveau projet
                </Link>
              </Button>
            </div>
          </div>

          {/* Quick Actions */}
          <QuickActions actions={quickActionsData} />

          {/* Stats Grid */}
          <section className="animate-slide-up" aria-labelledby="stats-heading">
            <h2 id="stats-heading" className="sr-only">Statistiques clés</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {statsData.map((stat, index) => (
                <StatCard
                  key={stat.label}
                  label={stat.label}
                  value={stat.value}
                  change={stat.change}
                  trend={stat.trend}
                  icon={<stat.icon className="w-6 h-6" />}
                  delay={stat.delay + index * 50}
                />
              ))}
            </div>
          </section>

          {/* Main Grid Layout */}
          <div className="grid gap-6 lg:grid-cols-[1fr_380px]">
            {/* Left Column */}
            <div className="space-y-6">
              {/* Projects Section */}
              <section className="animate-slide-up" aria-labelledby="projects-heading">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 id="projects-heading" className="text-headline font-bold text-foreground">Projets récents</h2>
                    <p className="text-muted-foreground text-sm mt-0.5">{projectsData.length} projets actifs</p>
                  </div>
                  <Button variant="ghost" size="sm" asChild className="glass border-[hsl(var(--glass-border))]">
                    <Link href="/projects">
                      Voir tout <ArrowRight className="w-4 h-4 ml-1" />
                    </Link>
                  </Button>
                </div>

                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {projectsData.map((project, index) => (
                    <ProjectCard
                      key={project.id}
                      id={project.id}
                      name={project.name}
                      type={project.type}
                      status={project.status}
                      progress={project.progress}
                      lastUpdated={project.lastUpdated}
                      avatar={project.avatar}
                      delay={project.delay + index * 50}
                    />
                  ))}
                </div>
              </section>

              {/* Workflow Timeline */}
              <WorkflowTimeline
                title="Pipeline d'exécution actuel"
                steps={workflowSteps}
                currentStep="step-3"
              />
            </div>

            {/* Right Column */}
            <div className="space-y-6 lg:sticky lg:top-24 lg:max-h-[calc(100vh-8rem)] lg:overflow-y-auto lg:pr-2">
              {/* Agents Status */}
              <section className="animate-slide-up" aria-labelledby="agents-heading">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 id="agents-heading" className="text-headline font-bold text-foreground">Mes agents</h2>
                    <p className="text-muted-foreground text-sm mt-0.5">{agentsData.length} agents spécialisés</p>
                  </div>
                  <BadgeComponent variant="outline" className="gap-1.5 px-2.5 py-1 text-xs font-medium text-primary bg-primary/10 border-primary/20">
                    <Bot className="w-3 h-3" />
                    {`${agentsData.filter(a => a.status === "running").length} actif(s)`}
                  </BadgeComponent>
                </div>

                <div className="space-y-3">
                  {agentsData.map((agent, index) => (
                    <AgentCard
                      key={agent.id}
                      id={agent.id}
                      name={agent.name}
                      type={agent.type}
                      status={agent.status}
                      progress={agent.progress}
                      description={agent.description}
                      lastRun={agent.lastRun}
                      color={agent.color}
                      delay={agent.delay + index * 50}
                    />
                  ))}
                </div>
              </section>

              {/* System Status */}
              <SystemStatus metrics={systemMetrics} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}