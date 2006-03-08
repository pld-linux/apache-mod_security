%define		mod_name	security
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: securing web applications
Summary(pl):	Modu³ do apache: ochrona aplikacji WWW
Name:		apache-mod_%{mod_name}
Version:	1.9.2
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.modsecurity.org/download/modsecurity-apache-%{version}.tar.gz
# Source0-md5:	c28b66f02adb1ddb2d0885483f6f8e0e
URL:		http://www.modsecurity.org/
BuildRequires:	apache-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
ModSecurity is an open source intrusion detection and prevention
engine for web applications. It operates embedded into the web server,
acting as a powerful umbrella - shielding web applications from
attacks.

%description -l pl
ModSecurity jest otwartym silnikiem wykrywania i zapobiegania intruzom
dla aplikacji WWW. Operuje w ramach serwera WWW, dzia³aj±c jak potê¿ny
parasol chroni±cy aplikacje WWW przed atakami.

%prep
%setup -q -n modsecurity-apache-%{version}

%build
cd apache2
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install apache2/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%preun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES INSTALL httpd.conf*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
