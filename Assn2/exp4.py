import math
import numpy as np
from PIL import Image

img = Image.open("sherlock.png")
img = img.convert('RGB')
img_ar = np.array(img)
rows,cols,color = img_ar.shape 
rgb_size = rows*cols*color
print(rgb_size)

def golomb_encode(N,M):
    q = N//M
    r = N % M 
    quo ='0'*q+'1'
    b = math.floor(math.log2(M))
    k = 2**(b + 1)-M
    if r < k:
        rem = bin(r)[2:]
        l = len(rem)
        if l<b:
            rem = '0'*(b-l)+rem
    else:
        rem = bin(r + k)[2:]
        l = len(rem)
        if l<b + 1:
            rem = '0'*(b + 1-l)+rem
    golomb_code = quo + rem
    return golomb_code

def to_bin(rem,k):
    st = ''
    while(k != 0):
        st = str(rem%2) + st
        rem //= 2 
        k -= 1
    return st

def gpo2(y,k):
    q = y >> k
    quo = '0'*q + '1'
    return quo + to_bin(y & ((1 << k) - 1), k)


def modi_gpo2(Lmax,beta,k,y):
    q = y >> k
    qmax = Lmax - beta - 1
    if(q < qmax):
        return gpo2(y,k)
    else:
        quo = '0'*qmax + '1'
        st = to_bin(y-1,beta)
        return quo+st 

def mapp(residual):
    if(residual < 0):
        return 2*abs(residual) - 1
    else:
        return 2*abs(residual)

def gamma(mapp, k, Lmax, beta):
    return modi_gpo2(Lmax,beta,k,mapp)

for cr in range(color):
    alpha = 256 
    beta = np.max(2,np.ceil(np.log(alpha)))
    Lmax = 2*(beta + np.max(8,beta))
    A,B,C = np.zeros((365,1))
    N = np.ones((365,1))
    tmp = np.max(2,np.floor((alpha+32)/64))
    A += tmp
    Irun = 0
    apre = 0
    T1 = 4
    T2 = 7
    T3 = 21
    g = np.zeros((3,1))
    q = np.zeros((4,1))
    q[3] = 1
    out_seq = np.zeros((rows,cols),dtype=object)
    for i in range(rows):
        for j in range(cols):
            if(i == 0 and j == 0):
                a,b,c,d = 0
            elif(i == 0):
                a = img_ar[i,j-1,cr]
                b,c,d = 0
            elif(j == 0):
                b = img_ar[i-1,j,cr]
                a = b
                c = apre
                d = img_ar[i-1,j+1,cr]
            elif(j == cols-1):
                b = img_ar[i-1,j,cr]
                d = b
                c = apre
                a = img_ar[i,j-1,cr]
            else:
                a = img_ar[i,j-1,cr]
                b = img_ar[i-1,j,cr]
                c = img_ar[i-1,j-1,cr]
                d = img_ar[i-1,j+1,cr]
            x = img_ar[i,j,cr]
            g[0] = d-b
            g[1] = b-c
            g[2] = c-b
            if(g[0] == 0 and g[1] == 0 and g[2] == 0):
                while(img_ar[i,j,cr] == a and j != cols):
                    j += 1
            else:
                for k in range(3):
                    if(g[k] <= -1*T3):
                        q[k] = -4
                    elif(g[k] <= -1*T2):
                        q[k] = -3
                    elif(g[k] <= -1*T1):
                        q[k] = -2    
                    elif(g[k] < 0):
                        q[k] = -1
                    elif(g[k] == 0):
                        q[k] = 0
                    elif(g[k] <= T1):
                        q[k] = 1
                    elif(g[k] <= T2):
                        q[k] = 2
                    elif(g[k] <= T3):
                        q[k] = 3
                    else:
                        q[k] = 4
                for k in range(3):
                    if(q[k] > 0): 
                        break
                    elif(q[k] < 0):
                        q = -1*q
                        break

                context_num = q[0]*81 + q[1]*9 + q[2]

                if(c >= max(a,b)):
                    x_med = min(a,b)
                elif(c <= min(a,b)):
                    x_med = max(a,b)
                else:
                    x_med = a + b - c
                
                if(q[3] == 1):
                    x_hat = x_med + C[context_num]
                else:
                    x_hat = x_med - C[context_num]

                if(x_hat >= alpha):
                    x_hat = alpha - 1
                elif(x_hat < 0):
                    x_hat = 0
                
                residual = x - x_hat
                if(q[3] == -1):
                    residual *= -1
                residual %= alpha
                if(residual < -1*(alpha//2)):
                    residual += alpha
                elif(residual > alpha//2):
                    residual -= alpha

                z = N[context_num]
                k = 0
                while(z < A[context_num]):
                    k += 1
                    z = N[context_num] << k

                if(k > 0):
                    val = mapp(residual)
                elif(k == 0 and 2*B[context_num] <= -1*N[context_num]):
                    val = mapp(-1*residual - 1)
                else:
                    val = mapp(residual)
                
                out_seq[i,j] = gamma(val,k,Lmax,beta)

                B[context_num] += residual
                A[context_num] += abs(residual)
                if(N[context_num] == 64):
                    A[context_num] /= 2
                    if(B[context_num] >= 0):
                        B[context_num] /= 2
                    else:
                        B[context_num] = -(1 - B[context_num]/2)
                    N[context_num] /= 2
                if(B[context_num] < -1*N[context_num]):
                    C[context_num] -= 1
                    B[context_num] += N[context_num]
                    if(B[context_num] <= -1*N[context_num]):
                        B[context_num] = -1*N[context_num] + 1
                elif(B[context_num] > 0):
                    C[context_num] += 1
                    B[context_num] -= N[context_num]
                    if(B[context_num] > 0):
                        B[context_num] = 0

    print(out_seq)
