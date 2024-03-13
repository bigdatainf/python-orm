class MetaModel(type):
    manager_class = BaseManager
 
    def _get_manager(cls):
        return cls.manager_class(model_class=cls)
 
    @property
    def objects(cls):
        return cls._get_manager()