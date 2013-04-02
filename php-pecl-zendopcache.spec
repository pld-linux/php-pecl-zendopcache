# NOTE:
# This version of Zend OPcache is compatible with PHP 5.2.*, 5.3.*, 5.4.*
# and PHP-5.5 development branch.  PHP 5.2 support may be removed in the future.
%define		modname	zendopcache
Summary:	Zend Optimizer+ - PHP code optimizer
Summary(pl.UTF-8):	Zend Optimizer+ - optymalizator kodu PHP
Name:		php-pecl-%{modname}
Version:	7.0.1
Release:	0.1
License:	PHP 3.01
Group:		Libraries
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	3a0a43a4819c72763bc35ecf5689221e
URL:		http://pecl.php.net/package/zendopcache
BuildRequires:	php-devel >= 4:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.519
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

# TODO:
# NOTE: In case you are going to use Zend OPcache together with Xdebug,
# be sure that Xdebug is loaded after OPcache. "php -v" must show Xdebug
# after OPcache.
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} zend extension module
zend_extension=opcache.so
EOF

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
%attr(755,root,root) %{php_extensiondir}/opcache.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php/conf.d/%{modname}.ini
