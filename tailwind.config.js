/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./parslib/templates/**/*.html", "./parslib/static/js/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        'roboto': ['Roboto', 'sans-serif'],
      },
      colors: {
        'sidebar-bg': '#2c3e50',
        'sidebar-hover': '#34495e',
      },
    },
  },
  plugins: [],
}