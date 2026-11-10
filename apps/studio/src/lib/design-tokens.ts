/**
 * Nexus Design AI — Design Tokens
 *
 * Three aesthetic directions combined:
 * 1. KINETIC TYPE — Motion-driven typography, expressive letterforms
 * 2. GLASSMORPHISM — Layered glass surfaces, depth through transparency
 * 3. WIREFRAMER3D — Structural wireframes, 3D spatial awareness
 */

export const designTokens = {
  // ============================================
  // COLOR PALETTE — Glassmorphism base with Kinetic accents
  // ============================================
  colors: {
    // Base surfaces (Glassmorphism)
    glass: {
      surface: 'rgba(255, 255, 255, 0.08)',
      surfaceStrong: 'rgba(255, 255, 255, 0.12)',
      surfaceHover: 'rgba(255, 255, 255, 0.16)',
      border: 'rgba(255, 255, 255, 0.18)',
      borderStrong: 'rgba(255, 255, 255, 0.28)',
      shadow: 'rgba(0, 0, 0, 0.25)',
      shadowStrong: 'rgba(0, 0, 0, 0.4)',
    },

    // Dark mode glass
    glassDark: {
      surface: 'rgba(15, 15, 25, 0.7)',
      surfaceStrong: 'rgba(20, 20, 35, 0.8)',
      surfaceHover: 'rgba(25, 25, 45, 0.85)',
      border: 'rgba(255, 255, 255, 0.1)',
      borderStrong: 'rgba(255, 255, 255, 0.18)',
      shadow: 'rgba(0, 0, 0, 0.5)',
      shadowStrong: 'rgba(0, 0, 0, 0.7)',
    },

    // Kinetic Type accents — Electric, expressive
    kinetic: {
      primary: '#00FF88',      // Electric mint — primary action
      primaryDim: '#00CC6A',
      secondary: '#FF006E',    // Hot pink — secondary/alert
      tertiary: '#FFBE0B',     // Solar yellow — highlight
      quaternary: '#3A86FF',   // Electric blue — info
      accent: '#8338EC',       // Violet — creative
    },

    // Wireframer3D — Structural, technical
    wireframe: {
      grid: 'rgba(0, 255, 136, 0.15)',
      gridStrong: 'rgba(0, 255, 136, 0.3)',
      line: 'rgba(255, 255, 255, 0.2)',
      lineStrong: 'rgba(255, 255, 255, 0.4)',
      vertex: '#00FF88',
      vertexActive: '#FF006E',
      axis: {
        x: '#FF006E',  // Red - X axis
        y: '#00FF88',  // Green - Y axis
        z: '#3A86FF',  // Blue - Z axis
      },
    },

    // Semantic (preserved for compatibility)
    semantic: {
      success: '#00FF88',
      warning: '#FFBE0B',
      error: '#FF006E',
      info: '#3A86FF',
    },

    // Text hierarchy
    text: {
      primary: '#FFFFFF',
      secondary: 'rgba(255, 255, 255, 0.7)',
      tertiary: 'rgba(255, 255, 255, 0.45)',
      inverted: '#0A0A0F',
      kinetic: '#00FF88',
    },

    // Background layers
    background: {
      base: '#0A0A0F',
      elevated: '#0F0F1A',
      overlay: 'rgba(10, 10, 15, 0.9)',
      noise: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\'/%3E%3C/svg%3E")',
    },
  },

  // ============================================
  // TYPOGRAPHY — Kinetic Type System
  // ============================================
  typography: {
    // Display faces — Kinetic, expressive
    display: {
      family: '"Space Grotesk", "Syne", system-ui, sans-serif',
      fallback: 'system-ui, sans-serif',
      weights: {
        light: 300,
        regular: 400,
        medium: 500,
        bold: 600,
        extrabold: 700,
        black: 800,
      },
    },

    // Mono for technical/wireframe data
    mono: {
      family: '"JetBrains Mono", "Fira Code", "SF Mono", monospace',
      fallback: 'monospace',
      weights: {
        regular: 400,
        medium: 500,
        bold: 700,
      },
    },

    // UI text — clean, readable
    ui: {
      family: '"Inter", "DM Sans", system-ui, sans-serif',
      fallback: 'system-ui, sans-serif',
      weights: {
        regular: 400,
        medium: 500,
        semibold: 600,
      },
    },

    // Type scale — Fluid, clamp-based
    scale: {
      // Display sizes (Kinetic hero)
      displayXl: 'clamp(3.5rem, 2rem + 8vw, 8rem)',
      displayLg: 'clamp(2.5rem, 1.5rem + 5vw, 5rem)',
      displayMd: 'clamp(2rem, 1.25rem + 3vw, 3.5rem)',
      displaySm: 'clamp(1.5rem, 1rem + 2vw, 2.5rem)',

      // Heading sizes
      h1: 'clamp(2rem, 1.5rem + 2.5vw, 3rem)',
      h2: 'clamp(1.75rem, 1.25rem + 2vw, 2.5rem)',
      h3: 'clamp(1.375rem, 1rem + 1.5vw, 2rem)',
      h4: 'clamp(1.125rem, 0.875rem + 1vw, 1.5rem)',
      h5: 'clamp(1rem, 0.875rem + 0.5vw, 1.25rem)',
      h6: 'clamp(0.875rem, 0.75rem + 0.5vw, 1rem)',

      // Body sizes
      bodyLg: 'clamp(1.125rem, 1rem + 0.5vw, 1.25rem)',
      bodyMd: 'clamp(1rem, 0.95rem + 0.25vw, 1.125rem)',
      bodySm: 'clamp(0.875rem, 0.85rem + 0.125vw, 1rem)',
      bodyXs: 'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',

      // UI sizes
      label: 'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',
      caption: 'clamp(0.625rem, 0.6rem + 0.125vw, 0.75rem)',
      micro: 'clamp(0.5rem, 0.45rem + 0.125vw, 0.625rem)',
    },

    // Line heights
    leading: {
      tight: 1.1,
      snug: 1.25,
      normal: 1.5,
      relaxed: 1.625,
      loose: 2,
    },

    // Letter spacing for kinetic effect
    tracking: {
      tightest: '-0.03em',
      tighter: '-0.02em',
      tight: '-0.01em',
      normal: '0',
      wide: '0.02em',
      wider: '0.04em',
      widest: '0.08em',
      kinetic: '0.12em', // For animated text
    },
  },

  // ============================================
  // SPACING — Rhythmic, not uniform
  // ============================================
  spacing: {
    // Base unit: 4px
    base: '0.25rem',

    // Semantic spacing tokens
    space: {
      '0': '0',
      '1': '0.25rem',   // 4px
      '2': '0.5rem',    // 8px
      '3': '0.75rem',   // 12px
      '4': '1rem',      // 16px
      '5': '1.25rem',   // 20px
      '6': '1.5rem',    // 24px
      '7': '1.75rem',   // 28px
      '8': '2rem',      // 32px
      '10': '2.5rem',   // 40px
      '12': '3rem',     // 48px
      '16': '4rem',     // 64px
      '20': '5rem',     // 80px
      '24': '6rem',     // 96px
      '32': '8rem',     // 128px
    },

    // Section rhythms (not uniform!)
    section: {
      compact: 'clamp(2rem, 1.5rem + 2vw, 4rem)',
      comfortable: 'clamp(4rem, 3rem + 4vw, 8rem)',
      generous: 'clamp(6rem, 4rem + 6vw, 12rem)',
      heroic: 'clamp(10rem, 6rem + 10vw, 20rem)',
    },

    // Component internal spacing
    component: {
      tight: '0.5rem',
      snug: '0.75rem',
      normal: '1rem',
      relaxed: '1.5rem',
      loose: '2rem',
    },
  },

  // ============================================
  // MOTION — Kinetic, purposeful
  // ============================================
  motion: {
    // Durations
    duration: {
      instant: '50ms',
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
      slower: '800ms',
      cinematic: '1200ms',
    },

    // Easings — Expressive, not standard
    easing: {
      // Kinetic easings
      kinetic: 'cubic-bezier(0.16, 1, 0.3, 1)',      // Expo out — expressive
      kineticIn: 'cubic-bezier(0.7, 0, 0.84, 0)',     // Expo in — sharp entry
      kineticSpring: 'cubic-bezier(0.34, 1.56, 0.64, 1)', // Overshoot — playful

      // Glassmorphism easings
      glass: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',  // Smooth, premium
      glassSharp: 'cubic-bezier(0.4, 0, 0.2, 1)',     // Material-like

      // Wireframe easings
      wireframe: 'cubic-bezier(0.5, 0, 0.5, 1)',      // Linear-ish, technical
      wireframeSnap: 'cubic-bezier(0.25, 0.1, 0.25, 1)', // Precise

      // Standard
      standard: 'cubic-bezier(0.4, 0, 0.2, 1)',
      emphasize: 'cubic-bezier(0.05, 0.7, 0.1, 1)',
    },

    // Stagger delays
    stagger: {
      fast: '30ms',
      normal: '60ms',
      slow: '100ms',
      cascade: '120ms',
    },

    // Reduced motion
    reduced: {
      duration: '0.01ms',
      easing: 'linear',
    },
  },

  // ============================================
  // BORDER RADIUS — Glassmorphism language
  // ============================================
  radius: {
    none: '0',
    xs: '0.125rem',   // 2px
    sm: '0.25rem',    // 4px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px
    '3xl': '1.5rem',  // 24px
    full: '9999px',

    // Glassmorphism specific
    glass: '1rem',
    glassLg: '1.5rem',
    glassXl: '2rem',
  },

  // ============================================
  // SHADOWS & DEPTH — Layered glass
  // ============================================
  shadows: {
    // Glassmorphism elevation
    glass: {
      level1: '0 2px 8px -2px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.08)',
      level2: '0 8px 24px -4px rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(255, 255, 255, 0.1)',
      level3: '0 16px 48px -8px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.12)',
      level4: '0 32px 96px -16px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.15)',

      // Colored glass shadows (kinetic)
      kinetic: '0 8px 32px -4px rgba(0, 255, 136, 0.2), 0 0 0 1px rgba(0, 255, 136, 0.15)',
      kineticStrong: '0 16px 64px -8px rgba(0, 255, 136, 0.3), 0 0 0 1px rgba(0, 255, 136, 0.25)',
    },

    // Wireframe — no shadows, only lines
    wireframe: {
      none: 'none',
    },

    // Inner shadows for pressed states
    inset: {
      sm: 'inset 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
      md: 'inset 0 4px 8px -2px rgba(0, 0, 0, 0.25)',
      lg: 'inset 0 8px 16px -4px rgba(0, 0, 0, 0.3)',
    },
  },

  // ============================================
  // BLUR & BACKDROP — Glassmorphism core
  // ============================================
  blur: {
    none: '0',
    sm: '4px',
    md: '8px',
    lg: '16px',
    xl: '24px',
    '2xl': '40px',
    '3xl': '64px',

    // Glassmorphism presets
    glass: '20px',
    glassStrong: '40px',
    glassSubtle: '10px',
  },

  // ============================================
  // Z-INDEX — Layered architecture
  // ============================================
  zIndex: {
    base: 0,
    dropdown: 100,
    sticky: 200,
    overlay: 300,
    modal: 400,
    popover: 500,
    tooltip: 600,
    toast: 700,
    wireframeGrid: -10,  // Behind everything
    wireframeOverlay: 800,
  },

  // ============================================
  // BREAKPOINTS
  // ============================================
  breakpoints: {
    xs: '320px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
    '3xl': '1920px',
  },

  // ============================================
  // WIREFRAME 3D — Structural tokens
  // ============================================
  wireframe3d: {
    gridSize: '60px',
    gridOpacity: 0.08,
    gridOpacityStrong: 0.2,
    lineWidth: '1px',
    lineWidthBold: '2px',
    vertexSize: '6px',
    vertexSizeActive: '10px',
    perspective: '1000px',
    rotateX: '15deg',
    rotateY: '-5deg',
    translateZ: '0px',
  },
} as const;

// Type exports for TypeScript
export type DesignTokens = typeof designTokens;
export type ColorTokens = typeof designTokens.colors;
export type TypographyTokens = typeof designTokens.typography;
export type SpacingTokens = typeof designTokens.spacing;
export type MotionTokens = typeof designTokens.motion;
export type ShadowTokens = typeof designTokens.shadows;
export type BlurTokens = typeof designTokens.blur;
export type RadiusTokens = typeof designTokens.radius;
export type ZIndexTokens = typeof designTokens.zIndex;
export type Wireframe3DTokens = typeof designTokens.wireframe3d;

// ============================================
// CSS CUSTOM PROPERTIES GENERATOR
// ============================================
export function generateCSSVariables(): string {
  const tokens = designTokens;
  let css = ':root {\n';

  // Colors
  css += '  /* Glassmorphism Surfaces */\n';
  Object.entries(tokens.colors.glass).forEach(([key, value]) => {
    css += `  --glass-${key}: ${value};\n`;
  });
  Object.entries(tokens.colors.glassDark).forEach(([key, value]) => {
    css += `  --glass-dark-${key}: ${value};\n`;
  });

  css += '\n  /* Kinetic Accents */\n';
  Object.entries(tokens.colors.kinetic).forEach(([key, value]) => {
    css += `  --kinetic-${key}: ${value};\n`;
  });

  css += '\n  /* Wireframe */\n';
  Object.entries(tokens.colors.wireframe).forEach(([key, value]) => {
    if (typeof value === 'object') {
      Object.entries(value).forEach(([subKey, subValue]) => {
        css += `  --wireframe-${key}-${subKey}: ${subValue};\n`;
      });
    } else {
      css += `  --wireframe-${key}: ${value};\n`;
    }
  });

  css += '\n  /* Text */\n';
  Object.entries(tokens.colors.text).forEach(([key, value]) => {
    css += `  --text-${key}: ${value};\n`;
  });

  css += '\n  /* Background */\n';
  Object.entries(tokens.colors.background).forEach(([key, value]) => {
    css += `  --bg-${key}: ${value};\n`;
  });

  // Typography
  css += '\n  /* Typography */\n';
  css += `  --font-display: ${tokens.typography.display.family};\n`;
  css += `  --font-mono: ${tokens.typography.mono.family};\n`;
  css += `  --font-ui: ${tokens.typography.ui.family};\n`;

  Object.entries(tokens.typography.scale).forEach(([key, value]) => {
    css += `  --text-${key}: ${value};\n`;
  });

  Object.entries(tokens.typography.leading).forEach(([key, value]) => {
    css += `  --leading-${key}: ${value};\n`;
  });

  Object.entries(tokens.typography.tracking).forEach(([key, value]) => {
    css += `  --tracking-${key}: ${value};\n`;
  });

  // Spacing
  css += '\n  /* Spacing */\n';
  Object.entries(tokens.spacing.space).forEach(([key, value]) => {
    css += `  --space-${key}: ${value};\n`;
  });

  Object.entries(tokens.spacing.section).forEach(([key, value]) => {
    css += `  --section-${key}: ${value};\n`;
  });

  Object.entries(tokens.spacing.component).forEach(([key, value]) => {
    css += `  --comp-${key}: ${value};\n`;
  });

  // Motion
  css += '\n  /* Motion */\n';
  Object.entries(tokens.motion.duration).forEach(([key, value]) => {
    css += `  --duration-${key}: ${value};\n`;
  });

  Object.entries(tokens.motion.easing).forEach(([key, value]) => {
    css += `  --easing-${key}: ${value};\n`;
  });

  Object.entries(tokens.motion.stagger).forEach(([key, value]) => {
    css += `  --stagger-${key}: ${value};\n`;
  });

  // Radius
  css += '\n  /* Radius */\n';
  Object.entries(tokens.radius).forEach(([key, value]) => {
    css += `  --radius-${key}: ${value};\n`;
  });

  // Shadows
  css += '\n  /* Shadows */\n';
  Object.entries(tokens.shadows.glass).forEach(([key, value]) => {
    css += `  --shadow-glass-${key}: ${value};\n`;
  });

  Object.entries(tokens.shadows.inset).forEach(([key, value]) => {
    css += `  --shadow-inset-${key}: ${value};\n`;
  });

  // Blur
  css += '\n  /* Blur */\n';
  Object.entries(tokens.blur).forEach(([key, value]) => {
    css += `  --blur-${key}: ${value};\n`;
  });

  // Z-Index
  css += '\n  /* Z-Index */\n';
  Object.entries(tokens.zIndex).forEach(([key, value]) => {
    css += `  --z-${key}: ${value};\n`;
  });

  // Wireframe 3D
  css += '\n  /* Wireframe 3D */\n';
  Object.entries(tokens.wireframe3d).forEach(([key, value]) => {
    css += `  --wf3d-${key}: ${value};\n`;
  });

  // Breakpoints
  css += '\n  /* Breakpoints */\n';
  Object.entries(tokens.breakpoints).forEach(([key, value]) => {
    css += `  --bp-${key}: ${value};\n`;
  });

  css += '}\n';

  return css;
}

// Generate and export CSS variables string
export const cssVariables = generateCSSVariables();

// Utility to get token value with fallback
export function getToken<T extends keyof DesignTokens>(
  category: T,
  path: string
): DesignTokens[T] | undefined {
  const keys = path.split('.');
  let current: any = designTokens[category];

  for (const key of keys) {
    if (current && typeof current === 'object' && key in current) {
      current = current[key];
    } else {
      return undefined;
    }
  }

  return current;
}

// Theme-aware token resolver
export function resolveToken(
  tokenPath: string,
  theme: 'light' | 'dark' = 'dark'
): string {
  // For now, return dark theme tokens (our primary)
  // In a full implementation, this would resolve based on theme
  const keys = tokenPath.split('.');
  let current: any = designTokens;

  for (const key of keys) {
    if (current && typeof current === 'object' && key in current) {
      current = current[key];
    } else {
      return `var(--${tokenPath.replace(/\./g, '-')})`;
    }
  }

  return current as string;
}

export default designTokens;