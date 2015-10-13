#!/bin/sh

echo "Updating repos..."

sudo apt-get update

echo "Updating packages..."

sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade

