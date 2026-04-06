export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Google Sans', 'Roboto', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        googlelight: {
          "primary": "#1a73e8", // Google Blue
          "primary-content": "#ffffff",
          "secondary": "#f4b400", // Google Yellow
          "accent": "#0f9d58", // Google Green
          "neutral": "#5f6368", // Google Dark Gray
          "base-100": "#ffffff", // Pure White surface
          "base-200": "#f8f9fa", // Google Background Gray
          "base-300": "#f1f3f4", // Google Lighter Gray
          "info": "#1976d2",
          "success": "#188038",
          "warning": "#ea4335", // Google Red
          "error": "#d93025",
          "--rounded-box": "1.5rem", // Slightly more rounded cards
          "--rounded-btn": "9999px", // Pill-shaped buttons
        },
      },
    ],
  },
}