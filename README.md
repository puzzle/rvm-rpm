RVM RPM Package
===============

RPM package for [rvm](https://github.com/wayneeseguin/rvm) suitable for CentOS 6.5 x86_64 (might also work with other versions and RHEL).

Stolen from [rvm-rpm](https://github.com/mdkent/rvm-rpm).

Howto
-----

1. Go to [rvm](https://github.com/wayneeseguin/rvm), select the proper version tag and download the ZIP to ~/rpmbuild/SOURCES
2. Install mock, add your user to the mock group
3. Start the build, e.g. with the included mockbuild script: `./mockbuild.sh epel-6-x86_64 el6 1.25.18 1`

About
-----

From the package description:

RVM is the Ruby Version Manager (rvm). It manages Ruby interpreter environments and switching between them.

This package is meant for use by multiple users maintaining a shared copy of RVM. Users added to the 'rvm' group will be able to modify all aspects of RVM. These users will also have their default umask changed to g+w (0022) to ensure correct permissions for the shared RVM content.

RVM is activated for all logins by default. To disable remove `/etc/profile.d/rvm.sh` and source rvm from each users shell.

Goal
-----

This package was created for numerous reasons:

1. To simplify the install process.
2. To more easily install rvm during a Kickstart install.
3. To simplify the upgrade process when using package management.
4. To conform to standard filesystem paths.

Credit
-----

mdkent on [GitHub](https://github.com/mdkent) for letting us steal.
