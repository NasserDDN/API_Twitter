FROM node:10-alpine as builder
WORKDIR /frontend
COPY package*.json ./
RUN npm install
RUN npm i axios
RUN npm i vue-axios
COPY . .
RUN npm run serve

FROM nginx:alpine as production-build
COPY /nginx.conf /etc/nginx/nginx.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /vue-ui/dist /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;" ]