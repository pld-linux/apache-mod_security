%define		mod_name	security
%define		apxs		/usr/sbin/apxs
Summary:	Apache module: securing web applications
Summary(pl.UTF-8):	Moduł do apache: ochrona aplikacji WWW
Name:		apache-mod_%{mod_name}
Version:	2.9.12
Release:	1
License:	GPL v2
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/owasp-modsecurity/ModSecurity/releases/download/v%{version}/modsecurity-v%{version}.tar.gz
# Source0-md5:	0a53077bc36e53d7c9e8b617d7e08f9d
Source1:	%{name}.conf
URL:		http://www.modsecurity.org/
BuildRequires:	apache-devel
BuildRequires:	autoconf
BuildRequires:	libxml2-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_unique_id
Suggests:	apache-mod_headers
Suggests:	apache-mod_security_crs
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

%package -n mlogc
Summary:	ModSecurity Audit Log Collector
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}

%description -n mlogc
This package contains the ModSecurity Audit Log Collector.

%prep
%setup -q -n modsecurity-v%{version}

%build
%configure
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{optflags}" \
	top_dir="%{apachelibdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachelibdir},%{apacheconfdir}/modsecurity.d/activated_rules} \
	$RPM_BUILD_ROOT{/var/log/mlogc/data,%{_bindir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT/var/lib/%{name}

install apache2/.libs/mod_%{mod_name}2.so $RPM_BUILD_ROOT%{apachelibdir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/90_mod_%{mod_name}.conf

cp -a modsecurity.conf-recommended $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d
echo '# Drop your local rules in here.' > $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d/modsecurity_localrules.conf

install mlogc/mlogc $RPM_BUILD_ROOT%{_bindir}
install mlogc/mlogc-batch-load.pl $RPM_BUILD_ROOT%{_bindir}/mlogc-batch-load
install mlogc/mlogc-default.conf $RPM_BUILD_ROOT%{_sysconfdir}/mlogc.conf

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
%doc CHANGES README.* modsecurity* doc/* tools
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*_mod_%{mod_name}.conf
%dir %{apacheconfdir}/modsecurity.d
%dir %{apacheconfdir}/modsecurity.d/activated_rules
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity.d/*.*
%attr(755,root,root) %{apachelibdir}/*.so
%attr(770,http,root) %dir /var/lib/%{name}

%files -n mlogc
%defattr(644,root,root,755)
%doc mlogc/INSTALL
%attr(0640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mlogc.conf
%attr(0755,root,root) %{_bindir}/mlogc
%attr(0755,root,root) %{_bindir}/mlogc-batch-load
%attr(0755,root,root) %dir /var/log/mlogc
%attr(0770,root,http) %dir /var/log/mlogc/data
