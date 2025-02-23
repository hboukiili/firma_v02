FROM node:20

WORKDIR /app

COPY ./* .

RUN npm i -g npm

RUN npm i react react-dom

RUN npm i chroma-js

RUN npm i redux-persist

RUN npm i react-plotlyjs

RUN npm install react-plotly.js plotly.js

RUN npm i --save-dev @types/leaflet

RUN npm i

RUN npm i @eunchurn/react-windrose

RUN npm i react-type-animation

RUN npm i echarts

RUN npm i echarts-liquidfill

RUN npm i date-fns

RUN npm i recharts

RUN npm i react-type-animation

RUN npx update-browserslist-db@latest

CMD ["npm", "run", "dev"]