class TraceDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_change = lambda x:x
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.on_change(self)

    def __delitem__(self, key):
        super().__delitem__(key)
        self.on_change(self)

    def clear(self):
        super().clear()
        self.on_change(self)

    def pop(self, *args):
        result = super().pop(*args)
        self.on_change(self)
        return result

    def popitem(self):
        result = super().popitem()
        self.on_change(self)
        return result

    def setdefault(self, key, default=None):
        result = super().setdefault(key, default)
        self.on_change(self)
        return result

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.on_change(self)
        
class TraceList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = None
    
    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        if self.callback:
            self.callback(self)
    
    def __delitem__(self, index):
        super().__delitem__(index)
        if self.callback:
            self.callback(self)
    
    def append(self, value):
        super().append(value)
        if self.callback:
            self.callback(self)
    
    def extend(self, values):
        super().extend(values)
        if self.callback:
            self.callback(self)
    
    def insert(self, index, value):
        super().insert(index, value)
        if self.callback:
            self.callback(self)
    
    def pop(self, index=-1):
        value = super().pop(index)
        if self.callback:
            self.callback(self)
        return value
    
    def remove(self, value):
        super().remove(value)
        if self.callback:
            self.callback(self)
    
    def clear(self):
        super().clear()
        if self.callback:
            self.callback(self)
    
    def reverse(self):
        super().reverse()
        if self.callback:
            self.callback(self)
    
    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs)
        if self.callback:
            self.callback(self)
            
def search_and_replace(regex_pattern, replacement, text):
    # Use the re.MULTILINE flag to search and replace across multiple lines
    pattern = re.compile(regex_pattern, flags=re.MULTILINE)
    result = pattern.sub(replacement, text)
    return result            