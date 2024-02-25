FROM node:16.13.0

RUN mkdir /code

WORKDIR /code

ADD frontend/package.json /code
RUN yarn install --non-interactive
ADD frontend/ /code


CMD yarn build	
