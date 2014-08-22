#!/usr/bin/python
import ldif
import os


def get_user_data():
    uidNumberFilePath = '/tmp/uidNumber '

    #apass = raw_input('Enter LDAP auth password: ')
    filename = raw_input('Enter filename: ')
    givenName = raw_input('Enter first name: ')
    sn = raw_input('Enter last name: ')
    cn = raw_input('Enter username: ')
    mail = raw_input('Enter email: ')
    title = raw_input('Enter title: ')
    userpass = raw_input('Enter user password: ')
    uidNumber = os.popen("ldapsearch -x -LLL -H ldap://ldap-utility-e1a-001.caffeine.io -b dc=caffeine,dc=io 'uidNumber=*' -S uidNumber | awk '/uidNumber/ {print $2}' | tail -n1")

    return {'first': givenName,
            'last': sn,
            'username': cn,
            'email': mail,
            'title': title,
            'filename': filename,
            'userpass': userpass,
            'uidNumber': uidNumber}


def main():
    data = get_user_data()

    entry = {'objectClass': ['top',
                             'person',
                             'organizationalPerson',
                             'inetOrgPerson',
                             'posixAccount'],
             'cn': [data['username']],
             'givenName': [data['first']],
             'uid': [data['username']],
             'mail': [data['email']],
             'title': [data['title']],
             'gecos': [data['username']],
             'homeDirectory': ['/home/' + data['username']],
             'loginShell': ['/bin/bash'],
             'userPassword': [data['userpass']],
             'uidNumber': [data['uidNumber']]}

    dn = 'cn=' + data['username'] + ',ou=chartboost' + ',dc=caffeine,dc=io'
    with open('/tmp/' + data['filename'] + '.ldif', 'w') as fd:
        ldif_writer = ldif.LDIFWriter(fd)
        ldif_writer.unparse(dn, entry)


if __name__ == '__main__':
    main()
