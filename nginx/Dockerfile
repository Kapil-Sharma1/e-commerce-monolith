# Stage 1 - build frontend app
#FROM node:14.15.4 as build-deps

#14.15-alpine3.10
#WORKDIR /app/

#COPY frontend/package*.json /app/
#RUN yarn install --non-interactive

#COPY frontend /app/
# COPY .env /app/.env
#RUN yarn build

#COPY backend/static /app/build/static/
#RUN echo $(ls /app/)
#RUN echo $(ls /app/build/)
#RUN echo $(ls /app/build/static/)

# Stage 2 - nginx & frontend build
FROM nginx:alpine
COPY nginx/stage.conf /etc/nginx/nginx.conf

# COPY nginx/letsencrypt/live/klkj234xd.aha3d.in/fullchain.pem /etc/nginx/fullchain.pem
# COPY nginx/letsencrypt/live/klkj234xd.aha3d.in/privkey.pem /etc/nginx/privkey.pem
# COPY nginx/letsencrypt/options-ssl-nginx.conf /etc/nginx/options-ssl-nginx.conf
# COPY nginx/letsencrypt/ssl-dhparams.pem /etc/nginx/ssl-dhparams.pem

#COPY backend/templates/choose-client.html /dist/
#COPY --from=build-deps /app/build/ /dist/

COPY backend/static /dist/static/

CMD ["nginx", "-g", "daemon off;"]
