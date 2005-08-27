Summary:	Mozilla LDAP schema
Summary(pl):	Schemat LDAP dla Mozilli
Name:		openldap-schema-mozillaorgperson
Version:	0.6.3
Release:	0.2
Epoch:		0
License:	?
Group:		Networking/Daemons
Source0:	mozillaOrgPerson.schema
URL:		https://bugzilla.mozilla.org/show_bug.cgi?id=116692
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		schemadir	/usr/share/openldap/schema

%description
This package contains LDAPv3 schema for use with the Mozilla Address
Book.

%description -l pl
Ten pakiet zawiera schemat LDAPv3 do u¿ywania z ksi±¿k± adresow±
Mozilli.

%prep
%setup -q -c -T
cp %{SOURCE0} .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{schemadir}

install *.schema $RPM_BUILD_ROOT%{schemadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q %{schemadir}/mozillaOrgPerson.schema /etc/openldap/slapd.conf; then
	sed -i -e '
		/^include.*local.schema/{
			i\
include		%{schemadir}/mozillaOrgPerson.schema
		}

		# enable dependant schemas: cosine, inetorgperson and core
		/^#include.*\(cosine\|inetorgperson\|core\)\.schema/{
			s/^#//
		}
	' /etc/openldap/slapd.conf
fi

if [ -f /var/lock/subsys/ldap ]; then
	/etc/rc.d/init.d/ldap restart >&2 || :
fi

%postun
if [ "$1" = "0" ]; then
	if grep -q %{schemadir}/mozillaOrgPerson.schema /etc/openldap/slapd.conf; then
		sed -i -e '
		/^include.*\/usr\/share\/openldap\/schema\/mozillaOrgPerson\.schema/d

		# for symmetry it would be nice if we disable enabled schemas in post,
		# but we really can not do that, it would break something else.
		' /etc/openldap/slapd.conf
	fi

	if [ -f /var/lock/subsys/ldap ]; then
		/etc/rc.d/init.d/ldap restart >&2 || :
	fi
fi

%files
%defattr(644,root,root,755)
%{schemadir}/*.schema
