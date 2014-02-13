%global rvm_dir /usr/lib/rvm
%global rvm_group rvm

Name: rvm-ruby
Summary: Ruby Version Manager
Version: 1.25.18
Release: 1%{?dist:%{dist}}
License: ASL 2.0
URL: http://github.com/puzzle/rvm-rpm
Group: Applications/System
Source: rvm-%{version}.zip
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires(pre): shadow-utils
# For rvm
Requires: bash curl git
# Basics for building ruby
Requires: gcc-c++ patch readline readline-devel zlib-devel libyaml-devel libffi-devel openssl-devel autoconf automake libtool bison 
# Used by the scripts
Requires: sed grep tar gzip bzip2 make file

%description
RVM is the Ruby Version Manager (rvm). It manages Ruby interpreter environments
and switching between them.

This package is meant for use by multiple users maintaining a shared copy of
RVM. Users added to the '%{rvm_group}' group will be able to modify all aspects
of RVM. These users will also have their default umask modified ("g+w") to allow
group write permission (usually resulting in a umask of "0002") in order to
ensure correct permissions for the shared RVM content.

RVM is activated for all logins by default. To disable remove 
%{_sysconfdir}/profile.d/rvm.sh and source rvm from each users shell.

%prep
%setup -q -n rvm-%{version}

%build

%install
rm -rf %{buildroot}

# Clean the env
for i in `env | grep ^rvm_ | cut -d"=" -f1`; do 
  unset $i;
done

# Install everything into one directory
rvm_ignore_rvmrc=1 \
  rvm_user_install_flag=0 \
  rvm_path="%{buildroot}%{rvm_dir}" \
  rvm_bin_path="%{buildroot}%{rvm_dir}%{_bindir}" \
  rvm_man_path="%{buildroot}%{rvm_dir}%{_mandir}" \
  ./install

# So members of the rvm group can write to it
find %{buildroot}%{rvm_dir} -exec chmod ug+w {} \;
find %{buildroot}%{rvm_dir} -type d -exec chmod g+s {} \;

mkdir -p %{buildroot}%{_sysconfdir}

# We use selfcontained so binaries end up in rvm/bin
cat > %{buildroot}%{_sysconfdir}/rvmrc <<END_OF_RVMRC
# Setup default configuration for rvm.
# If an rvm install exists in the home directory, don't load this.'
if [[ ! -s "\${HOME}/.rvm/scripts/rvm" ]]; then

  # Only users in the rvm group need the umask modification
  for i in \$(id -G -n); do
    if [ \$i = "rvm" ]; then
      umask g+w
      break
    fi
  done

  export rvm_user_install_flag=1
  export rvm_path="%{rvm_dir}"
fi
END_OF_RVMRC

mkdir -p %{buildroot}%{_sysconfdir}/profile.d

cat > %{buildroot}%{_sysconfdir}/profile.d/rvm.sh <<END_OF_RVMSH
# rvm loading hook
#
if [ -s "\${HOME}/.rvm/scripts/rvm" ]; then
  source "\${HOME}/.rvm/scripts/rvm"
elif [ -s "%{rvm_dir}/scripts/rvm" ]; then
  source "%{rvm_dir}/scripts/rvm"
fi
END_OF_RVMSH

chmod 644 %{buildroot}%{_sysconfdir}/profile.d/rvm.sh

mv %{buildroot}%{rvm_dir}%{_bindir}/rake %{buildroot}%{rvm_dir}%{_bindir}/rvm-rake

%clean
rm -rf %{buildroot}

%pre
getent group %{rvm_group} >/dev/null || groupadd -r %{rvm_group}
exit 0

%files
%defattr(-,root,root)
%config(noreplace) /etc/rvmrc
%config(noreplace) /etc/profile.d/rvm.sh
%attr(-,root,%{rvm_group}) %{rvm_dir}
%{rvm_dir}%{_bindir}/rvm*
%{rvm_dir}%{_bindir}/bundle
%{rvm_dir}%{_bindir}/ruby-rvm-env
%{rvm_dir}%{_mandir}/man1/*

%changelog
* Thu Feb 13 2014 Anselm Strauss <strauss@puzzle.ch> - 1.25.18
- Updated to new RVM version
- Changed download link and version
- Fixed installing bin files into separate /usr/lib/rvm/bin directory, otherwise shell profile does remove standard /usr/bin path from PATH variable
- Added missing requires
- Only tested on CentOS 6.5 x86_64

* Tue Dec 13 2011 Matthew Kent <mkent@magoazul.com> - 1.10.0-2
- New upstream release
- Drop rvm_prefix
- Rename rvm_user_install to rvm_user_install_flag
- Rename rake wrapper to rvm-rake
- Add file dependency

* Thu Aug 4 2011 Matthew Kent <mkent@magoazul.com> - 1.6.32-1
- New upstream release

* Tue Apr 19 2011 Matthew Kent <mkent@magoazul.com> - 1.6.3-1
- Initial package based off Gentoo work
