/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./software/**/*.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cosmic-black': '#000000',
        'cosmic-navy': '#1a1a2e',
        'cosmic-purple': '#16213e',
        'neon-purple': '#ff00ff',
        'neon-cyan': '#00ffff',
        'neon-pink': '#ff006e',
        'neon-blue': '#00d4ff',
      },
      fontFamily: {
        sans: ['Space Grotesk', 'Inter', 'system-ui', 'sans-serif'],
        display: ['Orbitron', 'sans-serif'],
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.5s ease-out',
        'fade-in': 'fadeIn 0.6s ease-out',
        'spin-slow': 'spin 8s linear infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glow: {
          '0%': {
            textShadow: '0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 30px #ff00ff',
          },
          '100%': {
            textShadow: '0 0 20px #ff00ff, 0 0 30px #ff00ff, 0 0 40px #ff00ff, 0 0 50px #ff00ff',
          },
        },
        slideUp: {
          '0%': { transform: 'translateY(50px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      backgroundImage: {
        'gradient-cosmic': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient-neon': 'linear-gradient(135deg, #ff00ff 0%, #00ffff 100%)',
        'gradient-dark': 'linear-gradient(180deg, #000000 0%, #1a1a2e 100%)',
      },
      boxShadow: {
        'neon': '0 0 5px theme("colors.neon-purple"), 0 0 20px theme("colors.neon-purple")',
        'neon-cyan': '0 0 5px theme("colors.neon-cyan"), 0 0 20px theme("colors.neon-cyan")',
        'glow': '0 0 15px rgba(255, 0, 255, 0.5)',
      },
    },
  },
  plugins: [],
}
