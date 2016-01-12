#!/usr/bin/env bash
# shitty automation
rsync -a var/www/html/characters/ /var/www/html/characters
rsync -a opt/character_levels/ /opt/character_levels
chown -R characterscraper:characterscraper /opt/character_levels
chown -R www-data:www-data /var/www/html/
service apache2 restart
cat <<EOF > /etc/cron.hourly/character_scraper
#!/usr/bin/env bash
python /opt/character_levels/python/character.py
EOF
run-parts --test /etc/cron.hourly
