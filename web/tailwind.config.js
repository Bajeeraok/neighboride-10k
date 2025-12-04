// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    // add any other folders
  ],
  safelist: [
    // These are the exact classes you're using on the input
    'bg-white/20',
    'bg-white/10',        // if you use this elsewhere
    'border-white/40',
    'border-white/20',
    'placeholder-gray-300',
    'text-white',
    'focus:ring-cyan-500/60',
    'focus:border-cyan-400',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
