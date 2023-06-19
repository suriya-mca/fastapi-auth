from decouple import config
import model

# database configuration 
DB_CONFIG = {
                'connections': {
                    # Dict format for connection
                    'default': {
                        "engine": "tortoise.backends.asyncpg",
                        "credentials": {
                            "database": config('DATABASE'),
                            "host": config('HOST'),
                            "password": config('PASSWORD'),
                            "port": config('PORT'),
                            "user": config('USERNAME'),
                          	},
                        'minsize': 1,
                        'maxsize': 200,
                        'max_queries': 50000,
                        'max_inactive_connection_lifetime': 300.0
                    },
                },
                # 'apps': {
                #     'models': {
                #         'models': ["model.models"],
                #          # If no default_connection specified, defaults to 'default'
                #         'default_connection': 'default',
                #     }
                # }
                'apps': {
                    'auth': {
                        'models': ["model.models", "aerich.models"],
                        'default_connection': 'default',
                    }
                }
            }