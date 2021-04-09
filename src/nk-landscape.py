import numpy as np

class NKLandscape:
    '''
    Summary: 
        NKLandscape is a class used to define an NK Landscape. The solutions of this model
        are binary strings which are represented as length N numpy arrays of binary numbers.
    
    Required Parameters: 
        N is the length of NK landscape binary solution strings.
        
        K is the number of dependencies at each bit position.
        
    Optional Parameters:
        dependency_matrix must be a shape (N, N) 2d numpy array consisting of zeros and ones 
        which will be interpreted as a matrix defining the dependency of each bit position 
        on every other bit position in the calculation of fitness. The sum of each row must 
        be equal to K + 1 and the diagonal of the matrix must always consist of ones. 
        The identity matrix is the only valid dependency matrix for K = 0. Each row will be mapped
        to a substring as if the array index of the one on the diagonal were the index into the solution string,
        mapping that value to the first element of the substring. Following ones along the row will be mapped 
        similarly to sequential elements of the substring, wrapping around at the end of the row. 
        If dependency_matrix is not provided, wrapped sequential dependency will be assumed.
        
        fitness_mapping is a length 2^K array where the indices map to binary substrings of 
        length K and the values are the fitness of each substring. If fitness_mapping is not 
        provided, the fitness values will be drawn from a normal distribution.
        
    
    To Do:
     - calculate_fitness method could probably be optimized when dependency matrix is the default
     - fix getters and setters
    '''
    
    def __init__(self, N=None, K=None, dependency_matrix=None, fitness_mapping=None):
        if (N is None):
            raise ValueError('N must be provided')
        self.N = N
        
        if (K is None):
            raise ValueError('K must be provided')
        if (K >= self.N):
            raise ValueError('K must be less than N = {}'.format(self.N))    
        self.K = K
        
        if (dependency_matrix is None):
            self.dependency_matrix = self._construct_sequential_dependency_matrix()
        else:
            self.dependency_matrix = dependency_matrix.astype(int)
            self._check_dependency_matrix()
            
        if (fitness_mapping is None):
            #fitness_mapping = np.random.normal(0, 1, (self.N, 2**self.K+1))
            self.fitness_mapping = np.random.uniform(-1, 1, (self.N, 2**(self.K+1)))
        else:
            self.fitness_mapping = fitness_mapping
        
    def _construct_sequential_dependency_matrix(self):
        dependency_matrix = np.identity(self.N)
        
        if (self.K > 0):
            for offset in range(self.K):
                dependency_matrix += np.eye(self.N, k=offset+1) + np.eye(self.N, k=-(self.N-(offset+1)))
        
        return dependency_matrix.astype(int)
    
    def _binary_to_decimal(self, binary):
        decimal = 0
        for i in range(len(binary)):
            decimal += binary[len(binary) - i - 1]*2**i
            
        return decimal
    
    def _check_dependency_matrix(self):
        if (self.dependency_matrix.shape != (self.N, self.N)):
            raise ValueError('The dependency matrix must be of shape (N, N) = ({}, {})'.format(self.N, self.N))
        
        if (not np.array_equal(self.dependency_matrix, self.dependency_matrix.astype(bool))):
            raise ValueError('The dependency matrix must only contain binary values')
            
        if (np.trace(self.dependency_matrix) != self.N):
            raise ValueError('The diagonal of the dependency matrix must be all ones')
            
        if ((K == 0) and (self.dependency_matrix.sum() != self.N)):
            raise ValueError('When K = 0 the dependency matrix can only be the identity matrix')
        
        if (not np.array_equal(self.dependency_matrix.sum(axis=1), np.full((1, self.N), self.K + 1)[0])):
            raise ValueError('The rows of the dependency matrix must each sum up to K={}'.format(self.K))   
    
    def generate_solutions(self, num=None):
        if num is None:
            raise ValueError('The number of solutions must be specified')
        return np.random.randint(2, size=(num, self.N))
    
    def calculate_fitness(self, solution):
        fitness = 0
        for i in range(self.N):
            dependency_indicies = np.argwhere(self.dependency_matrix[i, :] == 1).T[0]
            rolled_dependency_indicies = np.roll(dependency_indicies, -np.argwhere(dependency_indicies == i)[0])

            rolled_dependency_indicies = rolled_dependency_indicies
            substring = solution[rolled_dependency_indicies]
            decimal = self._binary_to_decimal(substring)
            
            fitness += self.fitness_mapping[i, decimal]
            
        return fitness
    
    def set_dependency_matrix(self, dependency_matrix):
        self.dependency_matrix = dependency_matrix
        self._check_dependency_matrix()
    
    def get_dependency_matrix(self):
        return self.dependency_matrix
    
    def set_fitness_mapping(self, fitness_mapping):
        self.fitness_mapping = fitness_mapping
        
    def get_fitness_mapping(self):
        return self.fitness_mapping
/newcommand(
/newcommand(
/newcommand(

/newcommand(
/newcommand(
/newcommand(


