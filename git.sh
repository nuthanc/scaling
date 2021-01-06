git add .
git commit -m "Update"
branch=`git rev-parse --abbrev-ref HEAD`
git push origin $branch