import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        mauve: {
          50:  "#f8f4f6",
          100: "#eedde8",
          200: "#ddbdd1",
          300: "#c99db8",
          400: "#b07898",
          500: "#8c4d72",
          600: "#73395c",
          700: "#5a2d48",
          800: "#3e1d32",
          900: "#26101e",
        },
        cream: {
          50:  "#fefcf8",
          100: "#fdf8ee",
          200: "#faf0d8",
          300: "#f5e4b8",
        },
        ink: {
          DEFAULT: "#1a1420",
          soft:    "#2e2438",
          muted:   "#6b5a78",
          faint:   "#a898b4",
        },
      },
      fontFamily: {
        display: ["Lora", "Georgia", "serif"],
        sans:    ["Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card:   "0 1px 3px rgba(26,20,32,0.06), 0 4px 12px rgba(26,20,32,0.06)",
        hover:  "0 4px 16px rgba(26,20,32,0.10), 0 1px 3px rgba(26,20,32,0.06)",
        drawer: "-8px 0 32px rgba(26,20,32,0.10)",
      },
      animation: {
        shimmer: "shimmer 1.6s ease-in-out infinite",
        marquee: "marquee 30s linear infinite",
      },
      keyframes: {
        shimmer: {
          "0%, 100%": { opacity: "1" },
          "50%":      { opacity: "0.4" },
        },
        marquee: {
          "0%":   { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;