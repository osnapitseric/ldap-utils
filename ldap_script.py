import ldif
import os


def get_user_data():
    return {'filename': raw_input('Filename: '),
            'cn': raw_input('First name: '),
            'sn': raw_input('Last name: '),
            'mail': raw_input('Email: '),
            'title': raw_input('Title: '),
            'username': raw_input('Username: '),
            'pw': raw_input('Password: '),
            'uid': os.popen("ldapsearch -x -LLL -H ldap://ldap-utility-e1a-001.caffeine.io -b dc=caffeine,dc=io 'uidNumber=*' -S uidNumber | awk '/uidNumber/ {print $2}' | tail -n1").read().strip()+1}


def main():
    data = get_user_data()

    with open('/tmp/' + data['filename'] + '.ldif', 'w') as fd:
        lw = ldif.LDIFWriter(fd)

        lw.unparse('cn=' + data['username'] + ',ou=chartboost,dc=caffeine,dc=io',
                   {'objectClass': ['top',
                                    'person',
                                    'organizationalPerson',
                                    'inetOrgPerson',
                                    'posixAccount'],
                    'cn': [data['username']],
                    'givenname': [data['cn']],
                    'uid': [data['uid']],
                    'mail': [data['mail']],
                    'title': [data['title']],
                    'gecos': [data['username']],
                    'homeDirectory': ['/home/' + data['username']],
                    'loginShell': ['/bin/bash'],
                    'userPassword': [data['pw']],
                    'uidNumber': [data['uid']],
                    'gidNumber': ['1001']})

if __name__ == '__main__':
    main()