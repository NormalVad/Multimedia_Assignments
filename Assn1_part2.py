from matplotlib.image import imread
import numpy as np
import os
import pywt
import matplotlib.pyplot as plt
import copy
plt.rcParams['figure.figsize'] = [8,8]
plt.rcParams["figure.autolayout"] = True
plt.rcParams.update({'font.size' : 15})

im = imread('test4.png')
inp_im = np.mean(im,-1)

print(inp_im.shape)

k = 2
w = 'db35'
coeffs = pywt.wavedec2(inp_im,wavelet=w,level=k)

coeff_arr, coeff_slices = pywt.coeffs_to_array(coeffs)

# thresh1 = np.sqrt(np.mean(np.square(coeff1_arr[coeff_slice1[0]])))
# ind1 = np.abs(coeff1_arr[coeff_slice1[0]]) > thresh1
# coeff1_arr[coeff_slice1[0]] = coeff1_arr[coeff_slice1[0]]*ind1

### Pruning coefficents on the basis of average energy of each sub band 

thresh = {}

for i in range(k):
    for j in {'ad','da','dd'}:
        thresh[str(i+1) + j] = np.sqrt(np.mean(np.square(coeff_arr[coeff_slices[i+1][j]])))

t = 1        
fig1 = plt.figure()
for s in (1,2,4,8):
    coeff_arr1 = copy.deepcopy(coeff_arr)
    for i in range(k):
        for j in {'ad','da','dd'}: 
            ind1 = np.abs(coeff_arr1[coeff_slices[i+1][j]]) > thresh[str(i+1)+j]*s
            coeff_arr1[coeff_slices[i+1][j]] = coeff_arr1[coeff_slices[i+1][j]]*ind1 

    coeffs_filt = pywt.array_to_coeffs(coeff_arr1,coeff_slices,output_format='wavedec2')
    Ar = pywt.waverec2(coeffs_filt,wavelet=w)
    fig1.add_subplot(2,2,t)
    plt.imshow(Ar,cmap='gray_r')
    plt.axis('off')
    plt.rcParams['figure.figsize'] = [12,12] 
    plt.rcParams.update({'font.size' : 7})
    plt.title('Energy Threshold = ' + str(s) + '*average energy')
    t += 1
plt.show()

### Varying the number of coefficents retained

i = 1
rows = 3
columns = 2
fig = plt.figure()

Csort = np.sort(np.abs(coeff_arr.reshape(-1)))
print(Csort)

for keep in (0.5,0.2,0.1,0.09,0.07,0.05):
    threshold = Csort[int(np.floor((1-keep)*len(Csort)))]
    print(threshold)
    ind = np.abs(coeff_arr) > threshold
    Cfilt =  coeff_arr*ind

    coeffs_filt = pywt.array_to_coeffs(Cfilt,coeff_slices,output_format='wavedec2')

    Arecon = pywt.waverec2(coeffs_filt,wavelet=w)
    fig.add_subplot(rows,columns,i)
    plt.imshow(Arecon,cmap='gray_r')
    plt.axis('off')
    plt.rcParams['figure.figsize'] = [8,8]
    plt.title('keep = ' + str(keep))
    i += 1
plt.show()
