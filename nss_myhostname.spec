Summary:	glibc plugin for local system host name resolution
Name:		nss_myhostname
Version:	0.3
Release:	1
License:	LGPL v2+
Group:		Libraries
URL:		http://0pointer.de/lennart/projects/nss-myhostname/
Source0:	http://0pointer.de/lennart/projects/nss-myhostname/nss-myhostname-%{version}.tar.gz
# Source0-md5:	d4ab9ac36c053ab8fb836db1cbd4a48f
Requires:	/sbin/ldconfig
Requires:	sed >= 4.0
Obsoletes:		nss-myhostname
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2).

%prep
%setup -q -n nss-myhostname-%{version}

%build
%configure \
	--libdir=/%{_lib} \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/nss-myhostname

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig -X
# sed-fu to add myhostname to the hosts line of %{_sysconfdir}/nsswitch.conf
if [ -f %{_sysconfdir}/nsswitch.conf ]; then
	%{__sed} -i -e '
		/^hosts:/ !b
		/\<myhostname\>/ b
		s/[[:blank:]]*$/ myhostname/
	' %{_sysconfdir}/nsswitch.conf
fi

%preun
# sed-fu to remove myhostname from the hosts line of %{_sysconfdir}/nsswitch.conf
if [ "$1" -eq 0 -a -f %{_sysconfdir}/nsswitch.conf ] ; then
	%{__sed} -i -e '
		/^hosts:/ !b
		s/[[:blank:]]\+myhostname\>//
	' %{_sysconfdir}/nsswitch.conf
fi

%postun -p /sbin/postshell
/sbin/ldconfig -X

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) /%{_lib}/libnss_myhostname.so.2
