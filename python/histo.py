#!/usr/bin/env python
'''
plot Gaussian histogram
'''


from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import skew
import struct

def doitboi():
    '''
    read/write binary data
    '''

    def duplicate_file(in_filename):
        out_filename = in_filename + '.dupe'
        byte_string = ''

        with open('data.cfg','rb') as infile:
            with open(out_filename, 'wb') as outfile:
                char = infile.read(1)
                byte = ord(char)
                # print byte
                byte_string += chr(byte)
                while char != "":
                    char = infile.read(1)
                    if char != "":
                        byte = ord(char)
                        # print byte
                        byte_string += chr(byte)
                outfile.write(byte_string)
                outfile.close


    '''
    plot histogram with data from bin file

    N =1000
    #data = np.load('filename')
    data = np.random.randn(N)
    plt.hist(data, bins = 7)

    '''

    '''
    fit histogram with Gaussian function
    '''

    N = 5000
    #data = np.random.randn(N)

    data = np.loadtxt("data.cfg")
    #print(data)
   # print(len(data))

    # Empirical average and variance computed
    avg = np.mean(data)
    #print('The mean of the data: ', avg)
    var = np.var(data)
    #print('The variance of the data: ', var)


    # derive skewness if there is any
    data = np.loadtxt("data.cfg")
    #print('skew value is: ', skew(data))

    # shape of the fitted Gaussian
    pdf_x = np.linspace(np.min(data), np.max(data),100)   # pdf = probability density function
    pdf_y = 1.0 / np.sqrt(2 * np.pi * var) * np.exp(-0.5 * (pdf_x - avg) ** 2/ var)

    # plotting
    # plt.figure()
    # plt.style.use('ggplot')
    # plt.hist(data, 100, normed = True)
    # plt.plot(pdf_x,pdf_y,'k--')
    # plt.legend(("Fit", "Data"), "best")
    # plt.savefig("test.png")
    # plt.show()



    '''
    about 95 % of the values lie within two standard deviation
    remove outlier using normal distribution and standard deviation
    remove outliers points by eleminating any points that were above (mean + 2 * sd) and any point below (mean - 2 * sd)
    '''
    elements = np.array(data)
    mean = np.mean(elements, axis = 0)
    sd = np.std(elements, axis = 0)
    final_list = [x for x in data if (x > mean - 2 * sd)]
    final_list = [x for x in data if (x < mean + 2 * sd)]
    # print(final_list)
    # print(len(final_list))

    # Emperical average and variance computed
    avg1 = np.mean(final_list)
    #print('Mean without outliers: ', avg1)
    var1 = np.var(final_list)
    #print('Variance without outliers: ', var)

    # Derive skewness if there is any
    #print('Skew value without outliers:', skew(final_list))

    # shape of the fitted Gaussian
    pdf_x_1 = np.linspace(np.min(final_list), np.max(final_list), 30)
    pdf_y_1 = 1.0 / np.sqrt(2 * np.pi * var1) * np.exp(-0.5 * (pdf_x_1 - avg1) ** 2 / var1)

    # plotting without outliers
    # plt.figure()
    # plt.style.use('ggplot')
    # plt.hist(final_list, 30, normed = True)
    # plt.plot(pdf_x_1, pdf_y_1, 'k--')
    # plt.legend(("Fit", "Data"), "best")
    # plt.savefig("test without outliers.png")
    # plt.show()


    return avg1



    '''
    probability density function (pdf)
    a pdf is used to specify the probability of the random variable falling within a particular range of values, as opposed to taking on any one value

    '''

    # from scipy.integrate import quad
    # import matplotlib.pyplot as plt
    # import numpy as np
    #
    # x = np.linspace(-90,90, num=1000)
    #
    # constant = 1.0 / np.sqrt(2 * np.pi)
    # pdf_normal_distribution = constant * np.exp((-x**2) / 2.0)
    #
    # fig, ax = plt.subplots(figsize = (10,5))
    # ax.plot(x, pdf_normal_distribution)
    # ax.set_ylim(0)
    # ax.set_title('Normal Distribution', size = 20)
    # ax.set_ylabel('Probability Density', size = 20)
    # plt.show()
    #
    #
    #
    # # make a pdf for the normal distribution a function
    # def normalProbabilityDensity(x):
    #     constant = 1.0 / np.sqrt(2 * np.pi)
    #     return (constant * np.exp((-x**2) / 2.0))
    #
    # test = normalProbabilityDensity(x)
    # print(test)
    #
    #
    # #integrate pdf from -2 to 2
    # result = quad(normalProbabilityDensity(x), -90, 90, limit= 1000)
    # print(result)







    # from scipy.integrate import quad
    # import matplotlib.pyplot as plt
    # import scipy.stats
    # import numpy as np
    #
    #
    # # normal distribution
    # xMin = 0.0
    # xMax = 16.0
    #
    # mean = np.average(data)
    # std = np.std(data)
    #
    # x = np.linspace(xMin, xMax,100)
    # y = scipy.stats.norm.pdf(x, mean, std)
    # plt.plot(x,y, color = 'black')
    #
    # # integration between x1 and x1
    # def normal_distribution_function(x):
    #     value = scipy.stats.norm.pdf(x, mean, std)
    #     return value
    #
    # x1 = mean + std
    # x2 = mean+ 2.0 * std
    #
    # res, err = quad(normal_distribution_function, x1, x2)
    #
    # print('Normal Distribution (mean, std): ', mean, std)
    # print('Integration between {} and {} -->'.format(x1,x2), res)
    #
    # #plot integration surface
    # ptx = np.linspace(x1, x2, 10)
    # pty = scipy.stats.norm.pdf(ptx, mean, std)
    #
    # plt.fill_between(ptx, pty, color = '#0b559f', alpha = '1.0')
    #
    # plt.grid()
    # plt.xlim(xMin, xMax)
    # plt.ylim(0, 0.25)
    #
    # plt.title('How to integrate a normal distribution in python? ', fontsize = 10)
    # plt.xlabel('x')
    # plt.ylabel('Normal Distribution')
    # plt.savefig("integrate_normal_distribution.png")
    # plt.show()

    
def intersect(p0,a0):
       
    """
    :param p0 : Nx2 (x,y) position coordinates
    :param a0 : angles in degrees for each point in p0
    :return: least squares intersection point of N lines
    """

    ang = a0 # create list of angles

    # create direction vectors with magnitude = 1
    n = []
    for a in ang:
        n.append([np.cos(np.radians(a)), np.sin(np.radians(a))])
    
    print(n)

    pos = p0 # create list of points
    n = np.array(n)

    # generate the array of all projectors
    nnT = np.array([np.outer(nn,nn) for nn in n ])
    ImnnT = np.eye(len(pos[0]))-nnT # orthocomplement projectors to n

    # now generate R matrix and q vector
    R = np.sum(ImnnT,axis=0)
    q = np.sum(np.array([np.dot(m,x) for m,x in zip(ImnnT,pos)]),axis=0)

    p = np.linalg.lstsq(R,q,rcond=None)[0]

    # and solve the least squares problem for the intersection point p
    return p
