/** @type {import('tailwindcss').Config} */
const primeui = require('tailwindcss-primeui');

export default {
    darkMode: 'selector',
    content: [
        "./presets/**/*.{js,vue,ts}",
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            extend: {},
        },
    },
    plugins: [primeui]
}

