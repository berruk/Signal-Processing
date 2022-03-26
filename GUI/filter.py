#
#   FILTER LIBRARY
#   Method:
#     BandPassFilter
#

# @author Berru Karakaş
#             150190733
#               13.6.21


import numpy as np

def BandPassFilter(X,J,fcL,fcH,sample_rate):

    #Calculated K coeff
    K = ((fcL**2 + fcH**2)**(3/2))/(2.82842712475*((fcL*fcH*np.pi)**3))
    T = 1/sample_rate #given

    #First set of coefficients
    A = np.pi*T*fcL
    B = np.pi*T*fcH

    #Second set of coefficients
    C = 8*K*(A**3)*(B**3)/(T**3)
    D = A*B + A + B + 1
    E = 2*A*B -2
    F = A*B - A - B + 1

    #bn coefficients for pseudo
    b = [C, 0, -3*C, 0, 3*C, 0, -C]

    #an coefficients for pseudo
    a = [D**3,       3*E*(D**2),
        3*(D**2)*F + 3*D*(E**2),
        6*D*E*F + (E**3),
        3*(E**2)*F + 3*D*(F**2),
        3*E*(F**2),        F**3]


    #Transfer Function
    J[1] = X/a[0] - J[2]*(a[1]/a[0]) - J[3]*(a[2]/a[0]) - J[4]*(a[3]/a[0]) - J[5]*(a[4]/a[0]) - J[6]*(a[5]/a[0]) - J[7]*(a[6]/a[0])
    
    Y = (b[0]/a[0])*( J[1] + -3*J[3] + 3*J[5] - J[7])
  
    #Unit Delay
    for i in range(7,1,-1): # 7 6 5 4 3 2 
        J[i] = J[i-1]


    return Y,J



