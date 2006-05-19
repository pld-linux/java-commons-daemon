Summary:	Jakarta Commons Daemon - controlling of Java daemons
Summary(pl):	Jakarta Commons Daemon - kontrolowanie demonów w Javie
Name:		jakarta-commons-daemon
Version:	1.0.1
Release:	1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/daemon/source/daemon-%{version}.tar.gz
# Source0-md5:	df3eb5aafa53ca530843a09d40b8a1c0
URL:		http://jakarta.apache.org/commons/daemon/
BuildRequires:	automake
BuildRequires:	ant >= 1.4.1
BuildRequires:	jdk >= 1.2
BuildRequires:	junit >= 3.7
Requires:	jre >= 1.2
Requires:	jakarta-commons-collections >= 2.0
Requires:	jakarta-commons-logging >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -n daemon-%{version}

%build
# Java part
cat > build.properties << EOF
junit.home = %{_javadir}
junit.jar = \${junit.home}
EOF
ant dist

# native part
cd src/native/unix
cp -f /usr/share/automake/config.sub support
%configure \
	--with-java=%{_libdir}/java
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_bindir}}

install dist/*.jar $RPM_BUILD_ROOT%{_javadir}

install src/native/unix/jsvc $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc dist/LICENSE
%attr(755,root,root) %{_bindir}/jsvc
%{_javadir}/*.jar

%files doc
%defattr(644,root,root,755)
%doc dist/docs
