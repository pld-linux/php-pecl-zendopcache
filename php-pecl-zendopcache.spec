# NOTE:
# This version of Zend OPcache is compatible with PHP 5.2.*, 5.3.*, 5.4.*
# and PHP-5.5 development branch.  PHP 5.2 support may be removed in the future.
%define		php_name	php%{?php_suffix}
%define		modname	zendopcache
Summary:	Zend Optimizer+ - PHP code optimizer
Summary(pl.UTF-8):	Zend Optimizer+ - optymalizator kodu PHP
Name:		%{php_name}-pecl-%{modname}
Version:	7.0.2
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	a175166ac32544051bd3277cc00a7b5d
Source1:	%{modname}.ini
URL:		http://pecl.php.net/package/zendopcache
BuildRequires:	%{php_name}-devel >= 4:5.2
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
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
sed -e 's,@extensiondir@,%{php_extensiondir},' %{SOURCE1} > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/opcache.so
