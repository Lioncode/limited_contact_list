{
    'name': 'Company Contacts',
    'version': '12.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Contacts limited',
    'sequence': '10',
    'license': 'AGPL-3',
    'author': 'Lioncode',
    'maintainer': 'Lioncode',
    'website': 'https://lioncode.gr',
    'depends': ['base','crm','contacts','project'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'view/employee.xml',
    ],
    'images': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}