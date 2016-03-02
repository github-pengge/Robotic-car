# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

import math

class matrix(object):
    def __init__(self, value): # init matrix
        self.value = value
        self.dimx = len(value)
        self.dimy = len(value[0])
        if(value == [[]]): # here, len(value) = 1
            self.dimx = 0
        # self.size = self.dimx * self.dimy

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        if(self.dimx == 0):
            return '[[]]'
        matrix_string = ''
        for i in range(self.dimx):
            matrix_string += '%s\n' % self.value[i]
        return matrix_string

    def show(self): # display matrix
        print(str(self))

    @staticmethod
    def zeros(dimx, dimy):
        if(dimx == 0):
            mat = [[]]
        else:
            mat = [[0 for _ in range(dimy)] for _ in range(dimx)]
        return matrix(mat)

    @staticmethod
    def ones(dimx, dimy):
        res = matrix.zeros(dimx,dimy)
        res += 1
        return res

    @staticmethod
    def eye(dim):
        mat = matrix.zeros(dim, dim)
        for i in range(dim):
            mat.value[i][i] = 1
        return mat

    def __add__(self, other):
        if(isinstance(other,matrix)):
            assert self.dimx == other.dimx and self.dimy == other.dimy
            mat_add = []
            for row in range(self.dimx):
                one_row = []
                for col in range(self.dimy):
                    one_row.append(self.value[row][col] + other.value[row][col])
                mat_add.append(one_row)
        elif(isinstance(other,list) or isinstance(other,tuple)): # support broadcasting
            assert self.dimx == len(other)
            assert isinstance(other[0],int) or isinstance(other[0],float)
            mat_add = []
            for row in range(self.dimx):
                one_row = []
                for col in range(self.dimy):
                    one_row.append(self.value[row][col] + other[row])
                mat_add.append(one_row)
        elif(isinstance(other,int) or isinstance(other,float)): # support element-wise addition
            mat_add = []
            for row in range(self.dimx):
                one_row = []
                for col in range(self.dimy):
                    one_row.append(self.value[row][col] + other)
                mat_add.append(one_row)
        else:
            raise TypeError('matrix addition: unsupported type of %s.' % type(other))

        return matrix(mat_add)

    def __sub__(self, other):
        if(isinstance(other,matrix)):
            assert self.dimx == other.dimx and self.dimy == other.dimy
            mat_sub = []
            for row in range(self.dimx):
                one_row = []
                for col in range(self.dimy):
                    one_row.append(self.value[row][col] - other.value[row][col])
                mat_sub.append(one_row)
        elif(isinstance(other,list) or isinstance(other,tuple)): # support broadcasting
            assert self.dimx == len(other)
            assert isinstance(other[0],int) or isinstance(other[0],float)
            mat_sub = []
            for row in range(self.dimx):
                one_row = []
                for col in range(self.dimy):
                    one_row.append(self.value[row][col] - other[row])
                mat_sub.append(one_row)
        elif(isinstance(other,int) or isinstance(other,float)): # support element-wise subtraction
            mat_sub = []
            for row in range(self.dimx):
                one_row = []
                for col in range(self.dimy):
                    one_row.append(self.value[row][col] - other)
                mat_sub.append(one_row)
        else:
            raise TypeError('matrix subtraction: unsupported type of %s.' % type(other))

        return matrix(mat_sub)

    def __abs__(self):
        mat_abs = []
        for row in range(self.dimx):
            one_row = []
            for col in range(self.dimy):
                one_row.append(abs(self.value[row][col]))
            mat_abs.append(one_row)

        return matrix(mat_abs)

    def __mul__(self, other):
        if(isinstance(other, matrix)):
            assert self.dimy == other.dimx
            mat_mul = []
            for row in range(self.dimx):
                one_row = []
                for col in range(other.dimy):
                    s = 0
                    for c in range(self.dimy):
                        s += self.value[row][c] * other.value[c][col]
                    one_row.append(s)
                mat_mul.append(one_row)
        elif(isinstance(other, list) or isinstance(other, tuple)):
            assert self.dimy == len(other)
            assert isinstance(other[0],int) or isinstance(other[0],float)
            mat_mul = []
            for row in range(self.dimx):
                one_row = []
                for col in range(1):
                    s = 0
                    for c in range(self.dimy):
                        s += self.value[row][c] * other.value[c]
                    one_row.append(s)
                mat_mul.append(one_row)
        elif(isinstance(other, int) or isinstance(other, float)):
            mat_mul = []
            for row in range(self.dimx):
                one_row = []
                for col in range(self.dimy):
                    one_row.append(self.value[row][col] * other)
                mat_mul.append(one_row)
        else:
            raise TypeError('matrix multiplication: unsupported type of %s.' % type(other))

        return matrix(mat_mul)

    def __neg__(self):
        return self * (-1)

    def transpose(self):
        mat_trans = []
        for col in range(self.dimy):
            one_col = []
            for row in range(self.dimx):
                one_col.append(self.value[row][col])
            mat_trans.append(one_col)
        return matrix(mat_trans)

    def Cholesky(self, ztol=1.0e-5):
        res = matrix.zeros(self.dimx, self.dimx)

        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError("Matrix not positive-definite")
                res.value[i][i] = math.sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(self.dimx)])
                if abs(S) < ztol:
                    S = 0.0
                res.value[i][j] = (self.value[i][j] - S)/res.value[i][i]
        return res

    def Cholesky_inverse(self):
        res = matrix.zeros(self.dimx, self.dimy)

        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k] * res.value[j][k] for k in range(j+1, self.dimx)])
            res.value[j][j] = 1.0/tjj**2 - S/tjj
        for i in reversed(range(j)):
            res.value[j][i] = res.value[i][j] = \
                        -sum(
                            [self.value[i][k]*res.value[k][j]
                                    for k in range(i+1, self.dimx)
                             ]
                        )/self.value[i][i]

        return res

    def inverse(self): # matrix inverse (only for symmetry matrix)
        aux = self.Cholesky()
        res = aux.Cholesky_inverse()
        return res


if __name__ == '__main__':
    x = matrix([[1.5,0], [0.,1.5]])
    x.show() # print(x)
    print(x.inverse())

    y = matrix([[10.], [10.]])
    print(y.transpose())

    print(matrix.eye(3))

    print(x + matrix([[3.,0], [0.5, 2.]]))

    print(x * matrix([[1,2],[2,1]]))