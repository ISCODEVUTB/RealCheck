FROM node:16.20.0-bullseye
WORKDIR /RealCheck/client
COPY . ..
RUN apt update && apt install -y python3 python3-pip \
    && pip install -r ../requirements.txt --no-cache-dir \
    && npm install \
    && npm run build
EXPOSE 5000
EXPOSE 3000
CMD ["npm", "start"]
