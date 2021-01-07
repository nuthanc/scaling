git config --global user.name "nuthanc"
git config --global user.email "nuthanc@juniper.net"
git config --global credential.helper "cache --timeout=864000"

git add .
git commit -m "Update"
branch=`git rev-parse --abbrev-ref HEAD`
git push origin $branch
