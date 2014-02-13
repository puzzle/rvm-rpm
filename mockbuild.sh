#!/bin/sh -e

chroot=$1
dist=$2
version=$3
release=$4

cd `dirname $0`

mock -r $chroot --buildsrpm --spec rvm-ruby.spec --sources ~/rpmbuild/SOURCES
cp -v /var/lib/mock/$chroot/result/rvm-ruby-$version-puzzle.$release.$dist.src.rpm ~/rpmbuild/SRPMS
mock -r $chroot --rebuild ~/rpmbuild/SRPMS/rvm-ruby-$version-puzzle.$release.$dist.src.rpm
cp -v /var/lib/mock/$chroot/result/rvm-ruby-$version-puzzle.$release.$dist.x86_64.rpm ~/rpmbuild/RPMS
