%{?_javapackages_macros:%_javapackages_macros}
%global jarname commons-jexl

Name:           apache-%{jarname}
Version:        2.1.1
Release:        8.1%{?dist}
Summary:        Java Expression Language (JEXL)


License:        ASL 2.0
URL:            https://commons.apache.org/jexl
Source0:        http://www.apache.org/dist/commons/jexl/source/%{jarname}-%{version}-src.tar.gz
# Patch to fix test failure with junit 4.11
Patch0:         001-Fix-tests.patch

BuildRequires:  maven-local
BuildRequires:  javacc-maven-plugin

BuildArch:      noarch

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

Requires:       jpackage-utils
Provides:       %{jarname}-javadoc = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{jarname}-%{version}-src
%patch0 -p1 -b .test
# Java 1.6 contains bsf 3.0, so we don't need the dependency in the pom.xml file
%pom_remove_dep org.apache.bsf:bsf-api
find \( -name '*.jar' -o -name '*.class' \) -delete
# Fix line endings
find -name '*.txt' -exec sed -i 's/\r//' '{}' +


%build
%mvn_build


%install
%mvn_install


%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-7
- Install NOTICE file with javadoc package

* Thu Jun 28 2013 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-6
- Update to current maven spec guidelines to fix build (bug 979497)
- Add patch to fix test with junit 4.11

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.1.1-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-1
- Update to 2.1.1

* Mon Dec 12 2011 Orion Poplawski <orion@cora.nwra.com> - 2.1-1
- Update to 2.1
- Update bsf patch
- Add needed BRs

* Tue Oct 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0.1-4
- Packaging fixes
- New maven macro for depmaps (include a compat depmap) #745118

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 6 2010 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-3
- Use BR apache-commons-parent

* Tue Jul 13 2010 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-2
- Add license to javadoc package

* Wed May 26 2010 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-1
- Update to 2.0.1
- Require Java 1.6 or greater
- Drop language level patch
- Add patch to remove bsf-api 3.0 dependency from pom.xml as this is provided
  by Java 1.6
- Fix depmap group id

* Sat Jan 9 2010 Orion Poplawski <orion@cora.nwra.com> - 1.1-3
- Drop gcj support
- Fix javadoc group
- Bump java levels in pom.xml

* Thu Jan 7 2010 Orion Poplawski <orion@cora.nwra.com> - 1.1-2
- Rename to apache-commons-jexl

* Tue Oct 27 2009 Orion Poplawski <orion@cora.nwra.com> - 1.1-1
- Initial Fedora Package
