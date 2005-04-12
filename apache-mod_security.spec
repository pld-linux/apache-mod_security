%define		mod_name	security
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: securing web applications
Summary(pl):	Modu³ do apache: ochrona aplikacji WWW
Name:		apache-mod_%{mod_name}
Version:	1.8.7
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.modsecurity.org/download/modsecurity-%{version}.tar.gz
# Source0-md5:	0dd48656e451c711358c097dc80e0369
URL:		http://www.modsecurity.org/
BuildRequires:	apache-devel
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir     %(%{apxs} -q SYSCONFDIR)

%description
ModSecurity is an open source intrusion detection and prevention
engine for web applications. It operates embedded into the web server,
acting as a powerful umbrella - shielding web applications from
attacks.

%description -l pl
ModSecurity jest otwartym silnikiem wykrywania i zapobiegania intruzom
dla aplikacji WWW. Operuje w ramach serwera WWW, dzia³aj±c jak
potê¿ny parasol chroni±cy aplikacje WWW przed atakami.

%prep
%setup -q -n modsecurity-%{version}

%build
cd apache2
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install apache2/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES httpd.conf*
%attr(755,root,root) %{_pkglibdir}/*
