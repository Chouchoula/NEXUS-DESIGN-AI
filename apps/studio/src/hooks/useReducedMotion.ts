"use client";

import { useEffect, useState } from "react";

export function useReducedMotion(): boolean {
  const [shouldReduce, setShouldReduce] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setShouldReduce(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setShouldReduce(event.matches);
    };

    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, []);

  return shouldReduce;
}

export function usePrefersColorScheme(): "light" | "dark" {
  const [scheme, setScheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    setScheme(mediaQuery.matches ? "dark" : "light");

    const handler = (event: MediaQueryListEvent) => {
      setScheme(event.matches ? "dark" : "light");
    };

    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, []);

  return scheme;
}