%define		mod_name	security
%define		apxs		/usr/sbin/apxs
Summary:	Apache module: securing web applications
Summary(pl.UTF-8):	Moduł do apache: ochrona aplikacji WWW
Name:		apache-mod_%{mod_name}
Version:	2.5.9
Release:	2
License:	GPL v2
Group:		Networking/Daemons/HTTP
Source0:	http://www.modsecurity.org/download/modsecurity-apache_%{version}.tar.gz
# Source0-md5:	b7bf44a7e041b49b0da5043495660375
Source1:	%{name}.conf
Patch0:		%{name}-branding.patch
URL:		http://www.modsecurity.org/
BuildRequires:	apache-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_unique_id
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
ModSecurity is an open source intrusion detection and prevention
engine for web applications. It operates embedded into the web server,
acting as a powerful umbrella - shielding web applications from
attacks.

%description -l pl.UTF-8
ModSecurity jest otwartym silnikiem wykrywania i zapobiegania intruzom
dla aplikacji WWW. Operuje w ramach serwera WWW, działając jak potężny
parasol chroniący aplikacje WWW przed atakami.

%prep
%setup -q -n modsecurity-apache_%{version}
mv rules/README{,.rules}
mv rules/CHANGELOG{,.rules}
%patch0 -p1

%build
cd apache2
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{optflags}" \
	top_dir="%{apachelibdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachelibdir},%{apacheconfdir}}

install apache2/.libs/mod_%{mod_name}2.so $RPM_BUILD_ROOT%{apachelibdir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/90_mod_%{mod_name}.conf

install -d $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d/blocking
cp -a rules/*.conf $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d
#cp -a rules/blocking/*.conf $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d/blocking
echo '# Drop your local rules in here.' > $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d/modsecurity_localrules.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc CHANGES MODSECURITY_LICENSING_EXCEPTION README.* modsecurity* doc/* rules/optional_rules rules/README.rules rules/CHANGELOG.rules
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*_mod_%{mod_name}.conf
%dir %{apacheconfdir}/modsecurity.d
%dir %{apacheconfdir}/modsecurity.d/blocking
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity.d/*.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity.d/blocking/*.conf
%attr(755,root,root) %{apachelibdir}/*.so
