"use client";

import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "./useReducedMotion";

interface UseCountUpOptions {
  end: number;
  start?: number;
  duration?: number;
  delay?: number;
  decimals?: number;
  separator?: string;
  prefix?: string;
  suffix?: string;
  easing?: (t: number) => number;
  onComplete?: () => void;
}

const easeOutExpo = (t: number): number => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t));

export function useCountUp({
  end,
  start = 0,
  duration = 1200,
  delay = 0,
  decimals = 0,
  separator = ",",
  prefix = "",
  suffix = "",
  easing = easeOutExpo,
  onComplete,
}: UseCountUpOptions) {
  const [count, setCount] = useState(start);
  const [isAnimating, setIsAnimating] = useState(false);
  const frameRef = useRef<number | undefined>(undefined);
  const startTimeRef = useRef<number | undefined>(undefined);
  const shouldReduce = useReducedMotion();

  const formatNumber = (num: number): string => {
    const fixed = num.toFixed(decimals);
    const parts = fixed.split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, separator);
    return `${prefix}${parts.join(".")}${suffix}`;
  };

  const animate = (timestamp: number) => {
    if (!startTimeRef.current) startTimeRef.current = timestamp;

    const elapsed = timestamp - startTimeRef.current - delay;

    if (elapsed < 0) {
      frameRef.current = requestAnimationFrame(animate);
      return;
    }

    const progress = Math.min(elapsed / duration, 1);
    const easedProgress = easing(progress);
    const current = start + (end - start) * easedProgress;

    setCount(current);

    if (progress < 1) {
      frameRef.current = requestAnimationFrame(animate);
    } else {
      setCount(end);
      setIsAnimating(false);
      onComplete?.();
    }
  };

  const startAnimation = () => {
    if (shouldReduce) {
      setCount(end);
      onComplete?.();
      return;
    }

    setIsAnimating(true);
    startTimeRef.current = undefined;
    frameRef.current = requestAnimationFrame(animate);
  };

  const reset = () => {
    if (frameRef.current) cancelAnimationFrame(frameRef.current);
    setCount(start);
    setIsAnimating(false);
  };

  useEffect(() => {
    startAnimation();
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current);
    };
  }, [end, start, duration, delay, shouldReduce]);

  return { count: formatNumber(count), rawCount: count, isAnimating, startAnimation, reset };
}

export function useCountUpOnView(
  options: UseCountUpOptions,
  threshold = 0.1,
  rootMargin = "0px"
) {
  const [hasAnimated, setHasAnimated] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const shouldReduce = useReducedMotion();

  const countUp = useCountUp({
    ...options,
    delay: hasAnimated ? options.delay : options.delay,
  });

  useEffect(() => {
    const element = ref.current;
    if (!element || hasAnimated) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setHasAnimated(true);
            observer.unobserve(element);
          }
        });
      },
      { threshold, rootMargin }
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, [hasAnimated, threshold, rootMargin]);

  return { ...countUp, ref };
}