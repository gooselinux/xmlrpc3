# Copyright (c) 2000-2005, JPackage roject
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global mainname xmlrpc
%global     with_maven 0

Name:       xmlrpc3
Version:    3.0
Release:    4.15%{?dist}
Summary:    Java XML-RPC implementation
License:    ASL 2.0
Group:      Development/Libraries
Url:        http://ws.apache.org/xmlrpc/
Source0:    http://archive.apache.org/dist/ws/xmlrpc/sources/xmlrpc-%{version}-src.tar.gz
Source1:    %{name}-jpp-depmap.xml
%if ! %{with_maven}
# These build files were generated with mvn ant:ant
Source2:    %{name}-buildfiles.tar.bz2
Source3:    %{name}-ant-osgimanifests.tar.bz2
%endif
# FIXME:  file this upstream
# The tests pom.xml doesn't include necessary dependencies on junit and
# servletapi
Patch0:     %{name}-addjunitandservletapitotestpom.patch
%if %{with_maven}
# Add OSGi MANIFEST information
Patch1:     %{name}-client-addosgimanifest.patch
Patch2:     %{name}-common-addosgimanifest.patch
%else
Patch3:     %{name}-ant-osgimanifests.patch
%endif

BuildRequires:  dos2unix
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-eclipse
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-release
BuildRequires:  maven2-plugin-source
BuildRequires:	tomcat5
%endif
BuildRequires:  ant
BuildRequires:  ws-jaxme
BuildRequires:  ws-commons-util
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  apache-tomcat-apis
BuildRequires:  junit
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jakarta-commons-codec >= 1.3
BuildRequires:  jsse
BuildRequires:  java-devel >= 1:1.6.0
Requires:       jpackage-utils >= 0:1.6
Requires:       apache-tomcat-apis
Requires:       junit
Requires:       jakarta-commons-httpclient
Requires:       jakarta-commons-codec >= 1.3
Requires:       jsse
Requires:       ws-jaxme
Requires:       ws-commons-util

BuildArch:    noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:    Javadoc for %{name}
Group:      Development/Libraries

%description javadoc
Javadoc for %{name}.

%package common
Summary:    Common classes for XML-RPC client and server implementations
Group:      Development/Libraries

%description common
%{summary}.

%package common-devel
Summary:    Source for common classes of XML-RPC
Group:      Development/Libraries
Requires:   %{name}-common

%description common-devel
%{summary} client and server implementations.

%package client
Summary:    XML-RPC client implementation
Group:      Development/Libraries
Requires:   %{name}-common

%description client
%{summary}.

%package client-devel
Summary:    Source for XML-RPC client implementation
Group:      Development/Libraries
Requires:   %{name}-client

%description client-devel
%{summary}.

%package server
Summary:    XML-RPC server implementation
Group:      Development/Libraries
Requires:   %{name}-common

%description server
%{summary}.

%package server-devel
Summary:    Source for XML-RPC server implementation
Group:      Development/Libraries
Requires:   %{name}-server

%description server-devel
%{summary}.

%prep
%setup -q -n %{mainname}-%{version}
%patch0
%if %{with_maven}
cp %{SOURCE1} .
pushd client
%patch1
popd
pushd common
%patch2
popd
%else
tar jxf %{SOURCE2}
tar jxf %{SOURCE3}
%patch3
%endif

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
rm -rf $MAVEN_REPO_LOCAL
mkdir -p $MAVEN_REPO_LOCAL

%if ! %{with_maven}
mkdir -p $MAVEN_REPO_LOCAL/org/apache/ws/commons/ws-commons-util/1.0.1
ln -s %{_javadir}/ws-commons-util-1.0.1.jar \
  $MAVEN_REPO_LOCAL/org/apache/ws/commons/ws-commons-util/1.0.1

mkdir -p $MAVEN_REPO_LOCAL/junit/junit/3.8.1
ln -s %{_javadir}/junit-3.8.2.jar \
  $MAVEN_REPO_LOCAL/junit/junit/3.8.1/junit-3.8.1.jar

mkdir -p $MAVEN_REPO_LOCAL/xml-apis/xml-apis/1.0.b2/xml-apis-1.0.b2.jar
ln -s %{_javadir}/xml-commons-apis-1.3.04.jar \
  $MAVEN_REPO_LOCAL/xml-apis/xml-apis/1.0.b2/xml-apis-1.0.b2.jar

mkdir -p $MAVEN_REPO_LOCAL/jaxme/jaxmeapi/0.5.1/jaxmeapi-0.5.1.jar
ln -s %{_javadir}/jaxme/ws-jaxmeapi-0.5.1.jar \
  $MAVEN_REPO_LOCAL/jaxme/jaxmeapi/0.5.1

mkdir -p $MAVEN_REPO_LOCAL/commons-httpclient/commons-httpclient/3.0.1
ln -s %{_javadir}/commons-httpclient.jar \
  $MAVEN_REPO_LOCAL/commons-httpclient/commons-httpclient/3.0.1/commons-httpclient-3.0.1.jar

mkdir -p $MAVEN_REPO_LOCAL/commons-logging/commons-logging/1.1
ln -s %{_javadir}/commons-logging.jar \
  $MAVEN_REPO_LOCAL/commons-logging/commons-logging/1.1/commons-logging-1.1.jar

mkdir -p $MAVEN_REPO_LOCAL/log4j/log4j/1.2.12
ln -s %{_javadir}/log4j.jar \
  $MAVEN_REPO_LOCAL/log4j/log4j/1.2.12/log4j-1.2.12.jar

mkdir -p $MAVEN_REPO_LOCAL/logkit/logkit/1.0.1
ln -s %{_javadir}/avalon-logkit.jar \
  $MAVEN_REPO_LOCAL/logkit/logkit/1.0.1/logkit-1.0.1.jar

mkdir -p $MAVEN_REPO_LOCAL/avalon-framework/avalon-framework/4.1.3
ln -s %{_javadir}/avalon-framework.jar \
  $MAVEN_REPO_LOCAL/avalon-framework/avalon-framework/4.1.3/avalon-framework-4.1.3.jar

mkdir -p $MAVEN_REPO_LOCAL/javax/servlet/servlet-api/2.4
ln -s %{_javadir}/apache-tomcat-apis/tomcat-servlet2.4-api.jar \
  $MAVEN_REPO_LOCAL/javax/servlet/servlet-api/2.4/servlet-api-2.4.jar

mkdir -p $MAVEN_REPO_LOCAL/commons-codec/commons-codec/1.2
ln -s %{_javadir}/commons-codec.jar \
  $MAVEN_REPO_LOCAL/commons-codec/commons-codec/1.2/commons-codec-1.2.jar

# These next three will appear broken but become un-broken during the build
mkdir -p $MAVEN_REPO_LOCAL/org/apache/xmlrpc/xmlrpc-common/3.0
ln -s ../../../../../../../common/target/xmlrpc-common-3.0.jar \
  $MAVEN_REPO_LOCAL/org/apache/xmlrpc/xmlrpc-common/3.0/xmlrpc-common-3.0.jar

mkdir -p $MAVEN_REPO_LOCAL/org/apache/xmlrpc/xmlrpc-client/3.0
ln -s ../../../../../../../client/target/xmlrpc-client-3.0.jar \
  $MAVEN_REPO_LOCAL/org/apache/xmlrpc/xmlrpc-client/3.0/xmlrpc-client-3.0.jar

mkdir -p $MAVEN_REPO_LOCAL/org/apache/xmlrpc/xmlrpc-server/3.0
ln -s ../../../../../../../server/target/xmlrpc-server-3.0.jar \
  $MAVEN_REPO_LOCAL/org/apache/xmlrpc/xmlrpc-server/3.0/xmlrpc-server-3.0.jar
%endif

%build
dos2unix LICENSE.txt
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
%if %{with_maven}
# The java.home is due to java-gcj and libgcj weirdness on 64-bit
# systems
mvn-jpp \
  -e \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  -Djava.home=%{_jvmdir}/java/jre \
  -Dmaven2.jpp.depmap.file=%{SOURCE1} \
  -Dmaven.test.failure.ignore=true \
  install javadoc:javadoc
%else
ant -Dmaven.mode.offline=true -Dmaven.test.skip=true -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  javadoc package
find -name \.svn | xargs rm -rf
jar cf common/target/%{mainname}-common-%{version}-sources.jar \
  common/src/main/java/META-INF/MANIFEST.MF \
  -C common/src/main/java .
jar cf client/target/%{mainname}-client-%{version}-sources.jar \
  client/src/main/java/META-INF/MANIFEST.MF \
  -C client/src/main/java .
jar cf server/target/%{mainname}-server-%{version}-sources.jar \
  server/src/main/java/META-INF/MANIFEST.MF \
  -C server/src/main/java .
%endif

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 client/target/%{mainname}-client-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-client-%{version}.jar
install -m 644 server/target/%{mainname}-server-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-server-%{version}.jar
install -m 644 common/target/%{mainname}-common-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-common-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# sources jars
install -m 644 client/target/%{mainname}-client-%{version}-sources.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-client-%{version}-sources.jar
install -m 644 server/target/%{mainname}-server-%{version}-sources.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-server-%{version}-sources.jar
install -m 644 common/target/%{mainname}-common-%{version}-sources.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-common-%{version}-sources.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
cp -pr common/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr client/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr server/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/*

%files common
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadir}/%{name}-common.jar
%{_javadir}/%{name}-common-%{version}.jar

%files common-devel
%defattr(-,root,root,-)
%{_javadir}/%{name}-common-%{version}-sources.jar

%files client
%defattr(-,root,root,-)
%{_javadir}/%{name}-client.jar
%{_javadir}/%{name}-client-%{version}.jar

%files client-devel
%defattr(-,root,root,-)
%{_javadir}/%{name}-client-%{version}-sources.jar

%files server
%defattr(-,root,root,-)
%{_javadir}/%{name}-server.jar
%{_javadir}/%{name}-server-%{version}.jar

%files server-devel
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-server-%{version}-sources.jar

%changelog
* Fri Feb 19 2010 Andrew Overholt <overholt@redhat.com> 3.0-4.15
- Use archive.apache.org.

* Tue Feb 9 2010 Alexander Kurtakov <akurtako@redhat.com> 3.0-4.14
- BR java-devel >= 1:1.6.0.

* Tue Feb 9 2010 Alexander Kurtakov <akurtako@redhat.com> 3.0-4.13
- Make it use apache-tomcat-apis instead of tomcat5.

* Fri Dec 11 2009 Andrew Overholt <overholt@redhat.com> 3.0-4.12
- Disable building with maven due to missing -release plugin.
- Provide ability to build with ant.

* Mon Aug 17 2009 Andrew Overholt <overholt@redhat.com> 3.0-4.10
- Fixed URL (bug #354031)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-4.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 31 2008 Alexander Kurtakov <akurtako@redhat.com> 3.0-2.9
- Fix client osgi manifest - client should require common bundle.

* Wed Oct 22 2008 Alexander Kurtakov <akurtako@redhat.com> 3.0-2.8
- Drop gcj_support.
- Fix commons osgi manifest.
- BR tomcat5.

* Fri Sep 12 2008 Andrew Overholt <overholt@redhat.com> 3.0-2.7
- Add ppc64.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-2.6
- drop repotag
- fix license tag

* Wed Mar 19 2008 Andrew Overholt <overholt@redhat.com> 3.0-2jpp.5
- Fix server description (rhbz#433699)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0-2jpp.4
- Autorebuild for GCC 4.3

* Fri Sep 07 2007 Andrew Overholt <overholt@redhat.com> 3.0-1jpp.4
- Disable ppc64 (rh#239123).

* Fri Sep 07 2007 Andrew Overholt <overholt@redhat.com> 3.0-1jpp.3
- Add OSGi manifests.

* Fri Aug 24 2007 Andrew Overholt <overholt@redhat.com> 3.0-1jpp.2
- Rebuild.

* Fri Mar 16 2007 Andrew Overholt <overholt@redhat.com> 3.0-1jpp.1
- Create new xmlrpc3 package
- Use maven to build
- Shuffle to common, server, and client sub-packages
- Add -devel sub-packages for -sources jars

* Thu Mar 08 2007 Deepak Bhole <dbhole@redhat.com> 2.0.1-3jpp.2
- Add javax.net.ssl support to build org.apache.xmlrpc.secure.*
- Minor spec file cleanup

* Fri Aug 04 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:2.0.1-3jpp.1
- Merge with latest from JPP.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:2.0.1-1jpp_8.2fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.1-1jpp_8.1fc
- rebuild

* Wed Mar  8 2006 Rafael Schloming <rafaels@redhat.com> - 0:2.0.1-1jpp_7fc
- excluded s390 due to eclipse

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:2.0.1-1jpp_6fc
- stop scriptlet spew

* Fri Feb 24 2006 Igor Foox <ifoox@redhat.com> - 0:2.0.1-1jpp_5fc
- Added post/postun dependency on coreutils.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.1-1jpp_4fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.1-1jpp_3fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 25 2006 Igor Foox <ifoox@redhat.com>  0:2.0.1-1jpp_2fc
- ExcludeArch s390x and ppc64

* Wed Jan 18 2006 Andrew Overholt <overholt@redhat.com> 0:2.0.1-1jpp_2fc
- Comment out JPackage Distribution and Vendor tags

* Wed Jan 18 2006 Jesse Keating <jkeating@redhat.com> 0:2.0.1-1jpp_2fc
- bump for test

* Wed Jan 18 2006 Igor Foox <ifoox@redhat.com> 0:2.0.1-1jpp_1fc
- Update to version 2.0.1
- Natively compile

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> 0:1.2-0.b1.3jpp
- Build with ant-1.6.2

* Thu Apr 29 2004 David Walluck <david@jpackage.org> 0:1.2-0.b1.2jpp
- add jar symlinks
- remove %%buildroot in %%install

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.2-0.b1.1jpp
- 1.2-b1
- update for JPackage 1.5

* Mon Mar 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-1jpp 
- 1.1
- generic servlet support
- used source release
- dropped patch
- added applet jar

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-3jpp 
- versioned dir for javadoc
- no dependencies for javadoc package
- dropped jsse package
- adaptation to new servlet3 package
- adaptation to new jsse package
- section macro

* Fri Dec 7 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-2jpp
- javadoc into javadoc package

* Sat Nov 3 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-1jpp
- first JPackage release
