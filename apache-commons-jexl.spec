%global jarname commons-jexl

Name:           apache-%{jarname}
Version:        2.0.1
Release:        4
Summary:        Java Expression Language (JEXL)

Group:          Development/Java
License:        ASL 2.0
URL:            http://commons.apache.org/jexl
Source0:        http://www.apache.org/dist/commons/jexl/source/%{jarname}-%{version}-src.tar.gz
# Java 1.6 contains bsf 3.0, so we don't need the dependency in the pom.xml file
Patch0:         %{name}-2.0.1-bsf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  jpackage-utils
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  apache-commons-parent
BuildRequires:  maven-release-plugin
BuildRequires:  javacc-maven-plugin

BuildArch:      noarch

Requires:       jpackage-utils
Requires:       java
Provides:       %{jarname} = %{version}-%{release}

%description
Java Expression Language (JEXL) is an expression language engine which can be
embedded in applications and frameworks.  JEXL is inspired by Jakarta Velocity
and the Expression Language defined in the JavaServer Pages Standard Tag
Library version 1.1 (JSTL) and JavaServer Pages version 2.0 (JSP).  While
inspired by JSTL EL, it must be noted that JEXL is not a compatible
implementation of EL as defined in JSTL 1.1 (JSR-052) or JSP 2.0 (JSR-152).
For a compatible implementation of these specifications, see the Commons EL 
project.

JEXL attempts to bring some of the lessons learned by the Velocity community
about expression languages in templating to a wider audience.  Commons Jelly
needed Velocity-ish method access, it just had to have it. 


%package javadoc
Summary:        Javadocs for %{name}
Group:          Development/Java
Requires:       jpackage-utils
Provides:       %{jarname}-javadoc = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{jarname}-%{version}-src
%patch0 -p1 -b .bsf
find \( -name '*.jar' -o -name '*.class' \) -exec rm -f '{}' +
# Fix line endings
find -name '*.txt' -exec sed -i 's/\r//' '{}' +


%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
install javadoc:javadoc


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp target/%{jarname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{jarname}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{jarname}-%{version}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}
cp -rp target/site/apidocs \
$RPM_BUILD_ROOT%{_javadocdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/maven2/poms
cp -p pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap org.apache.commons %{jarname} %{version} JPP %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_datadir}/maven2/poms/JPP-%{name}.pom
%{_mavendepmapfragdir}
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{jarname}-%{version}.jar
%{_javadir}/%{jarname}.jar

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadocdir}/%{name}


