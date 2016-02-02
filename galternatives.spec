Summary:	Alternatives Configurator
Name:		galternatives
Version:	0.13.4
Release:	0.1
License:	GPL+
Group:		Applications/System
#Source0:	http://ftp.debian.org/debian/pool/main/g/galternatives/%{name}_%{version}.tar.gz
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/galternatives/%{name}_%{version}.tar.gz/6148901a78623e85e3265a63588a2d23/galternatives_%{version}.tar.gz
# Source0-md5:	6148901a78623e85e3265a63588a2d23
Source1:	org.fedoraproject.pkexec.run-%{name}.policy
Source2:	%{name}.pamd
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-fedora.patch
URL:		http://packages.qa.debian.org/g/galternatives.html
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools
BuildRequires:	intltool
BuildRequires:	python-devel
BuildRequires:	python-pygtk-glade
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	/usr/sbin/update-alternatives
Requires:	python-pygtk-glade
Requires:	python-pygtk-gtk
Requires:	usermode
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Graphical setup tool for the alternatives system. A GUI to help the
system administrator to choose what program should provide a given
service

%prep
%setup -q
%patch0 -p0
%patch1 -p0

# To silence rpmlint
sed -i '/^#!\%{_prefix}\/bin\/python/ d' galternatives/*.py

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT
%py_install
%py_postclean

desktop-file-install --delete-original	\
	--dir $RPM_BUILD_ROOT%{_desktopdir}	\
	--mode 0644					\
	galternatives.desktop

# polkit/pkexec wrapper
install -d $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/galternatives $RPM_BUILD_ROOT%{_sbindir}
cat << 'EOF' > $RPM_BUILD_ROOT%{_bindir}/galternatives
#!/bin/sh
pkexec --disable-internal-agent %{_sbindir}/galternatives "$@"
EOF
chmod a+rx $RPM_BUILD_ROOT%{_bindir}/galternatives

# polkit policy
install -d $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions

install -d $RPM_BUILD_ROOT/etc/pam.d
cp -p %{SOURCE2}  $RPM_BUILD_ROOT/etc/pam.d/galternatives

cd translations
LANGS=$(find -name '*.po' | cut -d '.' -f 2 | tr -d '/')
for lang in ${LANGS}; do
	echo ${lang}:
	install -d $RPM_BUILD_ROOT%{_localedir}/${lang}/LC_MESSAGES
	cp -p ${lang}.mo $RPM_BUILD_ROOT%{_localedir}/${lang}/LC_MESSAGES/galternatives.mo
done
cd -

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc debian/copyright
%doc TODO debian/changelog
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/galternatives
%attr(755,root,root) %{_bindir}/galternatives
%attr(755,root,root) %{_sbindir}/galternatives
%{_datadir}/polkit-1/actions/org.fedoraproject.pkexec.run-galternatives.policy
%{_datadir}/galternatives
%{py_sitescriptdir}/galternatives
%{py_sitescriptdir}/galternatives*.egg-info
%{_desktopdir}/galternatives.desktop
%{_pixmapsdir}/galternatives.png
