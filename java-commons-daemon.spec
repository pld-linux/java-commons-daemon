Summary:	Jakarta Commons Daemon - controlling of Java daemons
Summary(pl):	Jakarta Commons Daemon - kontrolowanie demonów w Javie
Name:		jakarta-commons-daemon
Version:	0.1
Release:	1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://jakarta.apache.org/~jfclere/commons-daemon/commons-daemon-src.tar.gz
# Source0-md5:	01aad1d93e62c019e666d9d088a1560d
Patch0:		%{name}-nobat.patch
URL:		http://jakarta.apache.org/
BuildRequires:	automake
BuildRequires:	jakarta-ant >= 1.4.1
BuildRequires:	jdk >= 1.2
BuildRequires:	junit >= 3.7
Requires:	jre >= 1.2
Requires:	jakarta-commons-collections >= 2.0
Requires:	jakarta-commons-logging >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	/usr/share/java

%description
The Daemon Component contains a set of Java and native code,
including a set of Java interfaces applications must implement and
Unix native code to control a Java daemon from a Unix operating
system.

%description -l pl
Komponent Daemon zawiera zbiór kodu w Javie i natywnego,
zawieraj±cego zbiór interfejsów w Javie, które musz± byæ
zaimplementowane w aplikacjach oraz natywny kod uniksowy kontroluj±cy
demony w Javie w systemie Unix.

%package doc
Summary:	Jakarta Commons Daemon documentation
Summary(pl):	Dokumentacja do Jakarta Commons Daemon
Group:		Development/Languages/Java

%description doc
Jakarta Commons Daemon documentation.

%description doc -l pl
Dokumentacja do Jakarta Commons Daemon.

%prep
%setup -q -n commons-daemon-src
%patch -p1

%build
# Java part
touch LICENSE
mkdir srcdir
cat > build.properties << EOF
junit.home = %{_javalibdir}
junit.jar = \${junit.home}
EOF
ant dist

# native part
cd src/native/unix
%configure \
	--with-java=/usr/lib/java
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javalibdir},%{_bindir}}

install dist/*.jar $RPM_BUILD_ROOT%{_javalibdir}

install dist/jsvc $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc dist/LICENSE
%attr(755,root,root) %{_bindir}/jsvc
%{_javalibdir}/*.jar

%files doc
%defattr(644,root,root,755)
%doc dist/docs
