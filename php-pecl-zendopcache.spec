# NOTE:
# This version of Zend OPcache is compatible with PHP 5.2.*, 5.3.*, 5.4.*
# and PHP-5.5 development branch. PHP 5.2 support may be removed in the future.
%define		php_name	php%{?php_suffix}
%define		modname	zendopcache
Summary:	Zend Optimizer+ - PHP code optimizer
Summary(pl.UTF-8):	Zend Optimizer+ - optymalizator kodu PHP
Name:		%{php_name}-pecl-%{modname}
Version:	7.0.5
Release:	3
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	0c2710c272e398bea89d41dee42ee633
Source1:	%{modname}.ini
URL:		https://pecl.php.net/package/zendopcache
BuildRequires:	%{php_name}-devel >= 4:5.2
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(opcache) = %{version}
Provides:	php(zendopcache) = %{version}
Obsoletes:	php-pecl-zendopcache < 7.0.3-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Zend OPcache provides faster PHP execution through opcode caching
and optimization. It improves PHP performance by storing precompiled
script bytecode in the shared memory. This eliminates the stages of
reading code from the disk and compiling it on future access. In
addition, it applies a few bytecode optimization patterns that make
code execution faster.

%prep
%setup -qc
mv %{modname}-%{version}/* .

if [ %{php_major_version} -ge 5 -a %{php_minor_version} -ge 5 ]; then
	echo >&2 "pointless to build, PHP >= 5.5 has php-opcache package"
	exit 1
fi

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# NOTE: In case you are going to use Zend OPcache together with Xdebug,
# be sure that Xdebug is loaded after OPcache. "php -v" must show Xdebug
# after OPcache.
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
sed -e 's,@extensiondir@,%{php_extensiondir},' %{SOURCE1} > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/opcache.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README LICENSE
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/opcache.ini
%attr(755,root,root) %{php_extensiondir}/opcache.so
