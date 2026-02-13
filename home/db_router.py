

#####################################################################################



class UserRouter:
    def db_for_read(self, model, **hints):
        if model.__name__ == 'CustomUser':   
            return 'users'
        return 'default'

    def db_for_write(self, model, **hints):
        if model.__name__ == 'CustomUser':
            return 'users'
        return 'default'

