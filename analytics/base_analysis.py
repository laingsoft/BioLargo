# Base analytics object, and a few really basic tools
# All analysis tools will inhert from this object

class Tool:
    def __init__(self):
        pass

    def evaluate(self):
        pass


###############
# Basic tools #
###############


class max_tool(Tool):
    '''
    Accepts a list, returns a maximum value  when eval is called
    '''
    def __init__(self, data):
        self.data = data

    def evaluate(self):
        return max(self.data)
    

class min_tool(Tool):
    '''
    Accepts a list, returns a minimum value when eval is called
    '''
    
    def __init__(self, data):
        self.data = data

    def evaluate(self):
        return min(self.data)

class simple_avg_tool(Tool):
    '''
    Accepts a list, returns a simple average
    '''
    def __init__(self, data):
        self.data = data

    def evaluate(self):
        total_sum = sum(self.data)
        return total_sum/len(self.data)
    
    
