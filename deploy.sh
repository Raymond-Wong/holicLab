echo yes | python manage.py collectstatic
git add .
git commit -m "auto submit"
git push sae $1:1
