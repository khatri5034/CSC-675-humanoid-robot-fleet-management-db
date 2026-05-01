class Relationship:
    def __init__(self,model_name, foreign_key,backreference=None, lazy_load=True):
        self.model_name = model_name
        self.fk = foreign_key
        self.lazy_load = lazy_load
        self.attribute_name = None 
        self.backreference = backreference
    def __set_name__(self, owner, name):
        self.attribute_name = name
    def __get__(self, instance, owner):
        """

        """
        if instance is None:
            return self
        
        cache = Cache(self.attribute_name)
        if self.lazy:
            if cache.has(instance):
                return cache.get(instance)

        model  = owner.resolve_model(self.model_name)

        fk_value = getattr(instance, self.fk)
        if model is None or fk_value is None:
            return None
        model_object = model.get(id=fk_value)
        if self.lazy and cache is not None:
            cache.add(instance, model_object)
        
        setattr(model_object, self.backreference, instance)
            
        
class Cache:
    def __init_(self,attribute_name):
        self.cache_name = f"_{attribute_name}_cache"
    @property
    def name(self):
        return self.cache_name
    def add(self, instance, model_object):
        setattr(instance, self.cache_name, model_object)

    def get(self, instance):
        return getattr(instance, self.cache_name)

    def has(self, instance):
        return hasattr(instance, self.cache_name)