# Base analytics object, and a few really basic tools
# All analysis tools will inhert from this object

from statistics import median, mode, stdev, variance

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

#########################
# Stats Library Wrapper #
#########################
class median_tool(Tool):
    def __init__(self, data):
        self.data = data
    def evaluate(self):
        return median(self.data)
    
class mode_tool(Tool):
    def __init__(self, data):
        self.data = data
    def evaluate(self):
        return mode(self.data)

class stdv_tool(Tool):
    def __init__(self, data):
        self.data = data
    def evaluate(self):
        return mode(self.data)

class variance_tool(Tool):
    def __init__(self, data):
        self.data = data
    def evaluate(self):
        return variance(self.data)


##################
# Genomics Tools #
##################

class nX_score_tool(Tool):
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
        while running_sum < (total_sum * self.x_val) :
            cursor = self.data[i]
            running_sum += cursor
            i+=1
        return cursor

class ngX_score_tool(Tool):
    '''
    calculates the NG[X] score
    Accepts the x_val and genome size
    '''
    def __init__(self, data, x_val, g_size):
        self.data = data.sort(reverse = True)
        self.x_val = x_val / 100
        self.g_size = g_size

    def evalutate(self):)
        i = 0
        running_sum = 0
        while running_sum < (self.g_size * self.x_val):
            cursor = self.data[i]
            running_sum += cursor
            i+=1
        return cursor
    


       
    
            
    
    
