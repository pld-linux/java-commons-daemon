Summary:	Jakarta Commons Daemon
Name:		jakarta-commons-daemon
Version:	0.1
Release:	1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://jakarta.apache.org/~jfclere/commons-daemon/commons-daemon-src.tar.gz
URL:		http://jakarta.apache.org/
Requires:	jre
BuildRequires:	jakarta-ant
BuildRequires:	junit
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	/usr/share/java

%description
Jakarta Commons Daemon.

%package doc
Summary:	Jakarta Commons Daemon
Group:		Development/Languages/Java

%description doc
Jakarta Commons Daemon.

%prep
%setup -q -n commons-daemon-src

%build
touch LICENSE
mkdir srcdir
cat > build.properties << EOF
junit.home = %{_javalibdir}
junit.jar = \${junit.home}
EOF
#hack
ant dist || true

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javalibdir}
install dist/*.jar $RPM_BUILD_ROOT%{_javalibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc dist/LICENSE
%{_javalibdir}/*.jar

%files doc
%defattr(644,root,root,755)
%doc dist/docs
