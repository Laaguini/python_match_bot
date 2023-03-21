from os.path import join
from cachetools import cached, TTLCache

class FilesystemMessageResolver(): 
    def __init__(self, root):
        self.root = root 

    @cached(TTLCache(16, 3600))
    def get(self, name): 
        filename = f'{name}.md'
        path = join(self.root, filename)

        with open(path, encoding="utf-8") as file: 
            content = file.read()

            if len(content) == 0: 
                return None 
            
            return content