Summary:	Jakarta Commons Daemon - controlling of Java daemons
Summary(pl.UTF-8):	Jakarta Commons Daemon - kontrolowanie demonów w Javie
Name:		jakarta-commons-daemon
Version:	1.0.1
Release:	1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/daemon/source/daemon-%{version}.tar.gz
# Source0-md5:	df3eb5aafa53ca530843a09d40b8a1c0
Patch0:		%{name}-link.patch
URL:		http://jakarta.apache.org/commons/daemon/
BuildRequires:	ant >= 1.4.1
BuildRequires:	automake
BuildRequires:	jdk >= 1.2
BuildRequires:	jpackage-utils
BuildRequires:	junit >= 3.7
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jakarta-commons-collections >= 2.0
Requires:	jakarta-commons-logging >= 1.0
Requires:	jre >= 1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Daemon Component contains a set of Java and native code, including
a set of Java interfaces applications must implement and Unix native
code to control a Java daemon from a Unix operating system.

%description -l pl.UTF-8
Komponent Daemon zawiera zbiór kodu w Javie i natywnego, zawierającego
zbiór interfejsów w Javie, które muszą być zaimplementowane w
aplikacjach oraz natywny kod uniksowy kontrolujący demony w Javie w
systemie Unix.

%package javadoc
Summary:	Jakarta Commons Daemon documentation
Summary(pl.UTF-8):	Dokumentacja do Jakarta Commons Daemon
Group:		Documentation
Obsoletes:	jakarta-commons-daemon-doc

%description javadoc
Jakarta Commons Daemon documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do Jakarta Commons Daemon.

%prep
%setup -q -n daemon-%{version}
%patch0 -p1

%build
# Java part
required_jars="junit"
export CLASSPATH=$(/usr/bin/build-classpath $required_jars)
%ant dist

# native part
cd src/native/unix
cp -f /usr/share/automake/config.sub support
%configure \
	--with-java=%{_libdir}/java
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
for a in dist/*.jar; do
	jar=${a##*/}
	cp -a dist/$jar $RPM_BUILD_ROOT%{_javadir}/${jar%%.jar}-%{version}.jar
	ln -s ${jar%%.jar}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$jar
done

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_bindir}
install src/native/unix/jsvc $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc dist/LICENSE
%attr(755,root,root) %{_bindir}/jsvc
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
