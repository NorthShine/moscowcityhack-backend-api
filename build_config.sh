#!/bin/bash
touch config.yml

echo "Enter domain or url the service is hosted on"
read domain
echo -e "DOMAIN: '$domain'" >> config.yml 

echo "Enter URL of articles parser. Note that its URI should be like: /api/v1?url="
read news_parser
echo -e "NEWS_PARSER: '$news_parser'" >> config.yml

echo "Enter URL of a deployed SearX instance"
read searx_url
echo -e "SEARX_URL: '$searx_url'" >> config.yml

echo "Now let's register an admin account"

echo "Enter admin account username"
read admin_username
echo -e "ADMIN_USERNAME: '$admin_username'" >> config.yml

echo "Enter admin account password"
read admin_password
echo -e "ADMIN_PASSWORD: '$admin_password'" >> config.yml

echo "Enter your generated secret key"
read secret_key
echo -e "SECRET_KEY: '$secret_key'" >> config.yml

echo -e "MODEL_PATH: $(pwd)/d2v.model" >> config.yml