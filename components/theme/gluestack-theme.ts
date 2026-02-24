/**
 * Emocog Theme for Gluestack (React Native)
 * Generated from .claude/manifests/theme.yaml
 *
 * Usage:
 * import { config as gluestackConfig } from '@gluestack-ui/config'
 * import { emocogTheme } from './gluestack-theme'
 *
 * export const config = {
 *   ...gluestackConfig,
 *   tokens: {
 *     colors: emocogTheme.colors,
 *     sizes: emocogTheme.sizes,
 *     space: emocogTheme.space,
 *     ...
 *   }
 * }
 *
 * Color Space: OKLch (perceptually uniform, better than hex for dark/light modes)
 * Dark Mode: Class-based (.dark), not media query
 * Design Style: Flat (no shadows)
 */

export const emocogTheme = {
  colors: {
    /* Light Mode — Primary */
    primary: "oklch(0.488 0.243 264.376)",
    primaryLight: "oklch(0.656 0.237 264.376)",
    primary50: "oklch(0.971 0.052 264.376)",
    primary100: "oklch(0.942 0.104 264.376)",
    primary200: "oklch(0.914 0.156 264.376)",
    primary300: "oklch(0.715 0.217 264.376)",
    primary400: "oklch(0.601 0.230 264.376)",
    primary500: "oklch(0.488 0.243 264.376)",
    primary600: "oklch(0.400 0.215 264.376)",
    primary700: "oklch(0.320 0.172 264.376)",
    primary800: "oklch(0.240 0.129 264.376)",
    primary900: "oklch(0.160 0.086 264.376)",

    /* Light Mode — Secondary */
    secondary: "oklch(0.928 0.082 231.394)",
    secondaryLight: "oklch(0.735 0.189 288.225)",
    secondary50: "oklch(0.985 0.015 231.394)",
    secondary100: "oklch(0.970 0.030 231.394)",
    secondary200: "oklch(0.950 0.060 231.394)",
    secondary300: "oklch(0.880 0.090 231.394)",
    secondary400: "oklch(0.810 0.085 231.394)",
    secondary500: "oklch(0.928 0.082 231.394)",
    secondary600: "oklch(0.820 0.073 231.394)",
    secondary700: "oklch(0.700 0.065 231.394)",
    secondary800: "oklch(0.580 0.058 231.394)",
    secondary900: "oklch(0.460 0.050 231.394)",

    /* Light Mode — Background & Foreground */
    background: "oklch(0.985 0.001 106.423)",
    backgroundLight: "oklch(0.985 0.001 106.423)",
    backgroundDark: "oklch(0.131 0.013 265.755)",

    foreground: "oklch(0.208 0.042 265.755)",
    foregroundLight: "oklch(0.985 0.001 106.423)",
    foregroundMuted: "oklch(0.483 0.066 265.755)",

    /* Light Mode — Semantic Colors */
    accent: "oklch(0.985 0.001 106.423)",
    accentForeground: "oklch(0.208 0.042 265.755)",

    destructive: "oklch(0.577 0.245 27.325)",
    destructiveForeground: "oklch(0.985 0.001 106.423)",

    muted: "oklch(0.898 0.008 106.423)",
    mutedForeground: "oklch(0.483 0.066 265.755)",

    /* Card & Popover */
    card: "oklch(0.985 0.001 106.423)",
    cardForeground: "oklch(0.208 0.042 265.755)",

    popover: "oklch(0.985 0.001 106.423)",
    popoverForeground: "oklch(0.208 0.042 265.755)",

    /* Border & Input */
    border: "oklch(0.898 0.008 106.423)",
    input: "oklch(0.985 0.001 106.423)",
    ring: "oklch(0.488 0.243 264.376)",

    /* Chart Colors */
    chart1: "oklch(0.488 0.243 264.376)",
    chart2: "oklch(0.928 0.082 231.394)",
    chart3: "oklch(0.577 0.245 27.325)",
    chart4: "oklch(0.585 0.194 88.225)",
    chart5: "oklch(0.483 0.066 265.755)",

    /* Sidebar */
    sidebarBackground: "oklch(0.985 0.001 106.423)",
    sidebarForeground: "oklch(0.208 0.042 265.755)",
    sidebarBorder: "oklch(0.898 0.008 106.423)",
    sidebarAccent: "oklch(0.488 0.243 264.376)",

    /* Neutral Grays */
    gray50: "oklch(0.985 0.001 106.423)",
    gray100: "oklch(0.970 0.003 106.423)",
    gray200: "oklch(0.940 0.006 106.423)",
    gray300: "oklch(0.898 0.008 106.423)",
    gray400: "oklch(0.800 0.010 106.423)",
    gray500: "oklch(0.650 0.012 106.423)",
    gray600: "oklch(0.500 0.014 106.423)",
    gray700: "oklch(0.350 0.015 106.423)",
    gray800: "oklch(0.200 0.016 106.423)",
    gray900: "oklch(0.100 0.017 106.423)",

    /* Transparent */
    transparent: "rgba(0, 0, 0, 0)",
    translucentDark: "rgba(0, 0, 0, 0.5)",
    translucentLight: "rgba(255, 255, 255, 0.5)",
  },

  typography: {
    /* Font Families */
    fontFamily: {
      sans: "Poppins",
      serif: "Georgia",
      mono: "Menlo",
    },

    /* Font Sizes (in pixels) */
    fontSize: {
      xs: 12,
      sm: 14,
      base: 16,
      lg: 18,
      xl: 20,
      "2xl": 24,
      "3xl": 30,
      "4xl": 36,
    },

    /* Font Weights */
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },

    /* Line Heights */
    lineHeight: {
      tight: 1.2,
      snug: 1.375,
      normal: 1.5,
      relaxed: 1.625,
      loose: 2,
    },

    /* Letter Spacing */
    letterSpacing: {
      tighter: -0.05,
      tight: -0.025,
      normal: 0,
      wide: 0.025,
      wider: 0.05,
      widest: 0.1,
    },
  },

  space: {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
    6: 24,
    8: 32,
    10: 40,
    12: 48,
    16: 64,
    20: 80,
    24: 96,
    32: 128,
    40: 160,
    48: 192,
    56: 224,
    64: 256,
    80: 320,
    96: 384,
  },

  sizes: {
    /* Pixel Values */
    px: 1,
    0.5: 2,
    1: 4,
    1.5: 6,
    2: 8,
    2.5: 10,
    3: 12,
    3.5: 14,
    4: 16,
    5: 20,
    6: 24,
    7: 28,
    8: 32,
    9: 36,
    10: 40,
    12: 48,
    14: 56,
    16: 64,
    20: 80,
    24: 96,
    28: 112,
    32: 128,
    36: 144,
    40: 160,
    44: 176,
    48: 192,
    52: 208,
    56: 224,
    60: 240,
    64: 256,
    72: 288,
    80: 320,
    96: 384,

    /* Full & Screen */
    full: "100%",
    screen: "100vw",
    screenHeight: "100vh",
  },

  radii: {
    none: 0,
    sm: 5,
    base: 8,
    md: 12,
    lg: 16,
    xl: 24,
    "2xl": 32,
    full: 9999,
  },

  shadows: {
    /* Flat Design — All shadows have opacity: 0 */
    none: {
      shadowColor: "transparent",
      shadowOpacity: 0,
      shadowRadius: 0,
      elevation: 0,
    },
    sm: {
      shadowColor: "#000000",
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0,
      shadowRadius: 1,
      elevation: 0,
    },
    base: {
      shadowColor: "#000000",
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0,
      shadowRadius: 3,
      elevation: 0,
    },
    md: {
      shadowColor: "#000000",
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0,
      shadowRadius: 6,
      elevation: 0,
    },
    lg: {
      shadowColor: "#000000",
      shadowOffset: { width: 0, height: 10 },
      shadowOpacity: 0,
      shadowRadius: 15,
      elevation: 0,
    },
    xl: {
      shadowColor: "#000000",
      shadowOffset: { width: 0, height: 20 },
      shadowOpacity: 0,
      shadowRadius: 25,
      elevation: 0,
    },
  },

  /* Animation Timing */
  animations: {
    "quick-fade": {
      from: { opacity: 0 },
      to: { opacity: 1 },
      duration: 150,
    },
    "slide-in": {
      from: { transform: [{ translateY: 10 }] },
      to: { transform: [{ translateY: 0 }] },
      duration: 300,
    },
    bounce: {
      "0%": { transform: [{ scale: 0 }] },
      "50%": { transform: [{ scale: 1.05 }] },
      "100%": { transform: [{ scale: 1 }] },
      duration: 500,
    },
  },

  /* Opacity */
  opacity: {
    0: 0,
    5: 0.05,
    10: 0.1,
    20: 0.2,
    25: 0.25,
    30: 0.3,
    40: 0.4,
    50: 0.5,
    60: 0.6,
    70: 0.7,
    75: 0.75,
    80: 0.8,
    90: 0.9,
    95: 0.95,
    100: 1,
  },

  /* ZIndex */
  zIndex: {
    hide: -1,
    auto: "auto",
    0: 0,
    10: 10,
    20: 20,
    30: 30,
    40: 40,
    50: 50,
    "2xl": 100,
    "3xl": 1000,
    "4xl": 9999,
  },
};

/**
 * Emocog Color Palette — OKLch Color Space
 *
 * Primary: oklch(0.488 0.243 264.376) — Blue
 * Secondary: oklch(0.928 0.082 231.394) — Light Blue-Gray
 * Destructive: oklch(0.577 0.245 27.325) — Warm Orange
 *
 * Design: Flat (no shadows)
 * Dark Mode: Class-based (.dark selector)
 */

export type EmocogTheme = typeof emocogTheme;
