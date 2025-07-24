FROM node:24-alpine
COPY . /frontend
WORKDIR /frontend
RUN npm install
ENTRYPOINT [ "npm", "run" ]
CMD [ "dev" ]
