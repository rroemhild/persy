Name:           persy
Version:        0.9
Release:        1%{?dist}
Summary:        Personal syncronization

Group:          Applications/Archiving
License:        GPLv2+
URL:            http://kinkerl.github.com/persy/
BuildArch:      noarch
Source0:        persy-0.9.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         %{name}-0.9.patch

BuildRequires:  gettext
BuildRequires:  python-sphinx
BuildRequires:  python-devel
Requires:       python python-paramiko python-inotify gnome-python2-rsvg librsvg2 git gitk


%description
backup or synchronize your data with multiple machines. 
persy is designed to run by its own on the computer or in an environment with 
at least one server in reach of every computer with synced files.


%prep
%setup -q

%patch0 -p1


%build
./configure && make


%install
make install \
     PREFIX="%{_prefix}" \
     DEST="%{buildroot}/usr"
 
 
%files
%defattr(-,root,root,-)
%doc
/%{_bindir}/%{name}
/usr/lib/%{name}/*
/%{_datadir}/doc/%{name}/*
/%{_datadir}/man/man1/%{name}.1.gz
/%{_datadir}/applications/%{name}.desktop
/%{_datadir}/icons/%{name}.svg
/etc/bash_completion.d/persy


%changelog
* Wed Mar 10 2010 Rafael Roemhild <rafael@roemhild.de> 0.9-1
- Initial packaging
