import numpy as np

class Batcher:
    def __init__(self, x):
        self.x = x
        self.n = int(len(x))
        
    def sorter_base(self, x):
        if x[0] >= x[1]:
            return x[::-1]
        else:
            return x

    def sorter(self, x):
        n = int(len(x))
        n2 = int(n/2)
        if n == 2:
            return self.sorter_base(x)  
        else:
            x1 = np.zeros(n)

            for i in range(n2): 
                x1[2*i:2*i+2] = self.sorter_base(x[2*i:2*i+2]) 
            
            x2 = np.zeros(n)

            for i in range(n):
                if i<n2 and i%2 == 1:
                    x2[i] = x1[n2+i-1]
                elif i>=n2 and i%2 == 0:
                    x2[i] = x1[i-n2+1]
                else:
                    x2[i] = x1[i]
            
            x3 = np.zeros(n)

            x3[:n2] = self.sorter(x2[:n2])
            x3[n2:] = self.sorter(x2[n2:])
            return x3

    # n batcher network
  
    def run(self):
        data = self.x
        k = 2 

        # bitnic sorter
        while k <= self.n:
            p = int(self.n/k) 
            
            data1 = np.zeros(self.n)

            for i in range(p): 
                for j in range(k):
                    if j<k/2:
                        data1[2*j+i*k] = data[j+i*k]
                    else:
                        data1[2*j-k+1+i*k] = data[j+i*k]                
            
            data2 = np.zeros(self.n)

            for i in range(p):
                s = self.sorter(data1[k*i:k*i+k])
                if i%2 == 1:
                    s = s[::-1] 
                data2[k*i:k*i+k] = s
                
            k = k*2
            data = data2
            
        return data


class Banyan:
    def __init__(self, x):
        self.x = x

    def banyan_base(self, x, n_time):
        if x[0] is not None:
            if x[0][n_time] == '1':
                return x[::-1]
        elif x[1] is not None:
            if x[1][n_time] == '0':
                return x[::-1]
        
        return x

    def banyan(self, x, n_time):
        n = int(len(x))
        n2 = int(n/2)
        
        if n == 2:  
            return self.banyan_base(x,n_time)
        else:

            x1 = [''] * n
            for i in range(n2): 
                x1[2*i:2*i+2] = self.banyan_base(x[2*i:2*i+2],n_time)

            x2 = [''] * n
            for i in range(n): 
                if i<n2 and i%2 == 1:
                    x2[i] = x1[n2+i-1]
                elif i>=n2 and i%2 == 0:
                    x2[i] = x1[i-n2+1]
                else:
                    x2[i] = x1[i]

            x3 = [''] * n
            x3[:n2] = self.banyan(x2[:n2],n_time+1)  
            x3[n2:] = self.banyan(x2[n2:],n_time+1)

            return x3

    def run(self):
        return self.banyan(self.x, 0)

def main():
    #x = np.array([1,0,3,2,5,4,7,6])  # 8 input
    x = np.array([1,0,3,2,5,4,7,6,9,8,11,10,13,12,15,14])  # 16 input

    print('---input--- \n', x)

    n = int(len(x))
    n_time = int(np.log2(n))
    print('---x size--- \n', n)

    batcher = Batcher(x)
    x1 = batcher.run()
    print('---batcher output--- \n', x1)

    x2 = np.zeros(n)
    for i in range(n):
        if i<n/2:
            x2[2*i] = x1[i]
        else:
            x2[2*i-n+1] = x1[i]

    x3 = [None]*n
    for i in range(n):
        if x2[i] < n:
            x3[i] = format(int(x2[i]), '0{}b'.format(n_time))  
    print('---banyan input--- \n', x3)

    banyan = Banyan(x3)
    x4 = banyan.run()
    print('---banyan output--- \n', x4)

    x5 = [None] * n
    for i in range(n):
        if x4[i] != None:
            x5[i] = int(x4[i], 2)
    print('---final output--- \n', x5)


if __name__ == '__main__':
    main()