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

class nx_score_tool(Tool):
    '''
    Calculates the N[x] score
    Accepts x_val, where x_val is the percentage of the entire assembly
    you want to see
    '''

    def __init__(self, data, x_val):
        self.data = data.sort(reverse=True)
        self.x_val = x_val / 100

    def evaluate(self):
        total_sum = sum(self.data)
        i = 0
        running_sum = 0
        while running_sum < (total_sum * x_val) :
            cursor = self.data[i]
            running_sum += cursor
            i+=1
        return cursor
    

            
       
    
            
    
    
