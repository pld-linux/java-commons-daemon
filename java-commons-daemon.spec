# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%include	/usr/lib/rpm/macros.java
Summary:	Commons Daemon - controlling of Java daemons
Summary(pl.UTF-8):	Commons Daemon - kontrolowanie demonów w Javie
Name:		java-commons-daemon
Version:	1.0.1
Release:	4
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/jakarta/commons/daemon/source/daemon-%{version}.tar.gz
# Source0-md5:	df3eb5aafa53ca530843a09d40b8a1c0
Patch0:		jakarta-commons-daemon-link.patch
URL:		http://commons.apache.org/daemon/
BuildRequires:	ant >= 1.4.1
BuildRequires:	automake
BuildRequires:	jdk >= 1.2
BuildRequires:	jpackage-utils
BuildRequires:	junit >= 3.7
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	xmlto >= 0:0.0.18-1
Requires:	java-commons-collections >= 2.0
Requires:	java-commons-logging >= 1.0
Requires:	jpackage-utils
Requires:	jre >= 1.2
Provides:	jakarta-commons-daemon
Obsoletes:	jakarta-commons-daemon
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
Summary:	Commons Daemon documentation
Summary(pl.UTF-8):	Dokumentacja do Commons Daemon
Group:		Documentation
Requires:	jpackage-utils
Provides:	jakarta-commons-daemon-javadoc
Obsoletes:	jakarta-commons-daemon-doc
Obsoletes:	jakarta-commons-daemon-javadoc

%description javadoc
Commons Daemon documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do Commons Daemon.

%prep
%setup -qc
mv daemon-%{version}/* .
%patch0 -p1

%build
# Java part
required_jars="junit"
export CLASSPATH=$(build-classpath $required_jars)
%ant dist

# native part
cd src/native/unix
cp -f /usr/share/automake/config.sub support
%configure \
	--with-java=%{java_home}
%{__make}
refentry2man < man/jsvc.1.xml > man/jsvc.1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a dist/commons-daemon.jar $RPM_BUILD_ROOT%{_javadir}/commons-daemon-%{version}.jar
ln -s commons-daemon-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/commons-daemon.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install src/native/unix/jsvc $RPM_BUILD_ROOT%{_bindir}
cp -a src/native/unix/man/jsvc.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc dist/LICENSE
%attr(755,root,root) %{_bindir}/jsvc
%{_mandir}/man1/jsvc.1*
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
