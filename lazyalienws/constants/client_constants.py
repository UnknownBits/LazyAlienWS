from lazyalienws.constants.core_constants import NAME, PACKAGE_NAME, VERSION_CLIENT, AUTHOR, GITHUB_URL

PLUGIN_METADATA = {
    'id': f'{PACKAGE_NAME}_client',
    'version': VERSION_CLIENT,
    'name': f'{NAME} Client',
    'description': f'A mcdr plugin for {NAME}',
    'author': AUTHOR,
    'link': GITHUB_URL,
    'dependencies': {
        'mcdreforged': '>=1.0.0',
    }
}

CONFIG = {
    "url":"ws://127.0.0.1:5800/",
    "client_name": None
}