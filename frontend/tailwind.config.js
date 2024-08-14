/** @type {import('tailwindcss').Config} */
const {nextui} = require("@nextui-org/react");
const withMT = require("@material-tailwind/react/utils/withMT");

module.exports = withMT({
  content: ["./index.html",
  "path-to-your-node_modules/@material-tailwind/react/components/**/*.{js,ts,jsx,tsx}",
  "path-to-your-node_modules/@material-tailwind/react/theme/components/**/*.{js,ts,jsx,tsx}",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@nextui-org/theme/dist/components/button.js", 
    './node_modules/@nextui-org/theme/dist/components/(button|snippet|code|input).js'
],
theme: {
  fontFamily: {
    Myfont : ['Montserrat', 'sans-serif'],
  },
  fontWeight : {
    lt: '300',
    nrml: '400',
    md: '500',
    smbld: '600',
    bld: '700',
  },
  extend: {
    colors: {
      'DarkGreen': '#033323',
      'Green': '#5BAD6B',
      'Red': '#DC4545',
      'Lgreen': '#DFEDDE',
      'lightGreen' : "#43c67e",
      'scBgGreen' : '#EAF3E9',
    },
  },
},
darkMode: "class",
plugins: [nextui()],
});

// export default {
//   content: [
//     "./index.html",
//     "./src/**/*.{js,ts,jsx,tsx}",
//     "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
//     "./node_modules/@nextui-org/theme/dist/components/button.js", 
//     './node_modules/@nextui-org/theme/dist/components/(button|snippet|code|input).js'

//   ],
//   theme: {
//     fontFamily: {
//       Myfont : ['Montserrat', 'sans-serif'],
//     },
//     fontWeight : {
//       lt: '300',
//       nrml: '400',
//       md: '500',
//       smbld: '600',
//       bld: '700',
//     },
//     extend: {
//       colors: {
//         'DarkGreen': '#033323',
//         'Green': '#5BAD6B',
//         'Red': '#DC4545',
//         'Lgreen': '#DFEDDE',
//         'lightGreen' : "#43c67e",
//         'scBgGreen' : '#EAF3E9',
//       },
//     },
//   },
//   darkMode: "class",
//   plugins: [nextui()],
// }

