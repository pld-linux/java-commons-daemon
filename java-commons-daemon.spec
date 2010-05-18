# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%include	/usr/lib/rpm/macros.java

%define		srcname	commons-daemon
Summary:	Commons Daemon - controlling of Java daemons
Summary(pl.UTF-8):	Commons Daemon - kontrolowanie demonów w Javie
Name:		java-commons-daemon
Version:	1.0.2
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.net.pl/commons/daemon/source/commons-daemon-%{version}-src.tar.gz
# Source0-md5:	a6c68eed204bc9f1ef3b77488edfcfeb
Patch0:		jakarta-commons-daemon-link.patch
URL:		http://commons.apache.org/daemon/
BuildRequires:	ant >= 1.4.1
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	java-junit >= 3.7
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	xmlto >= 0:0.0.18-1
Requires:	java-commons-collections >= 2.0
Requires:	java-commons-logging >= 1.0
Requires:	jpackage-utils
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

%package -n jsvc
Summary:	Commons Daemon jsvc utility
Summary(pl.UTF-8):	Narzędzie jsvc Commons Daemon
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description -n jsvc
Jsvc is a set of libraries and applications for making Java
applications run on UNIX more easily.

%description -n jsvc -l pl.UTF-8
Jsvc jest zestawem bibliotek i aplikacji które ułatwiają uruchamianie
aplikacji Javy.

%package javadoc
Summary:	Commons Daemon documentation
Summary(pl.UTF-8):	Dokumentacja do Commons Daemon
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	jakarta-commons-daemon-doc
Obsoletes:	jakarta-commons-daemon-javadoc

%description javadoc
Commons Daemon documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do Commons Daemon.

%prep
%setup -q -n %{srcname}-%{version}-src

find -name '*.o' -o -name '*.a' | xargs rm

%patch0 -p1

%build
# Java part
required_jars="junit"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH
%ant jar %{?with_javadoc:javadoc}

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
cp -a dist/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install src/native/unix/jsvc $RPM_BUILD_ROOT%{_bindir}
cp -a src/native/unix/man/jsvc.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc PROPOSAL.html RELEASE-NOTES.txt README
%{_javadir}/*.jar

%files -n jsvc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jsvc
%{_mandir}/man1/jsvc.1*

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
