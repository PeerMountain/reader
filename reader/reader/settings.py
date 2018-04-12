from os import getenv


PORT = int(getenv('PORT'))
if not PORT:
    raise NotImplementedError('PORT must be configured.')

ENVIRONMENT = getenv('ENVIRONMENT', 'PRODUCTION')
