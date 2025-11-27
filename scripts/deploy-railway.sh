#!/bin/bash

set -e

echo "railway deployment script"
echo "========================="
echo ""

# check if railway cli is installed
if ! command -v railway &> /dev/null; then
    echo "railway cli is not installed on this machine."
    echo "please install it with 'brew install railway' or 'npm install -g @railway/cli' and then run this script again."
    exit 1
fi

echo "checking railway authentication..."
if ! railway whoami >/dev/null 2>&1; then
    echo "you are not logged in to railway. opening login flow..."
    railway login
fi

# link to project if not already linked
if [ ! -f ".railway" ]; then
    echo ""
    echo "linking this repository to a railway project..."
    railway link
fi

echo ""
echo "current deployment status:"
railway status

echo ""
read -p "deploy latest code to railway by pushing to main? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "pushing code to github main branch..."
    git push origin main

    echo ""
    echo "github push finished. railway will automatically build and deploy the new version."
    echo "you can watch the deployment in the railway dashboard."
    echo ""
    read -p "open railway dashboard in browser? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        railway open
    else
        echo "ok, you can open the dashboard manually later."
    fi
else
    echo "deployment cancelled."
fi