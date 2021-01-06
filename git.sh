git config --global user.name "nuthanc"
git config --global user.email "nuthanc@juniper.net"

git add .
git commit -m "Update"
branch=`git rev-parse --abbrev-ref HEAD`
git push origin $branch