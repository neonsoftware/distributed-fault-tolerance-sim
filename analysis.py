from scipy import integrate
import numpy, math
# For the par it is 4 R(t) + 4 R(t)^2
#

def r_block (my_lambda, x):

    return 2 * math.exp( - my_lambda * x ) -  math.exp( - my_lambda * x ) *  math.exp( - my_lambda * x )

def mttf_par ( my_lambda ):

    return integrate.quad ( lambda x : 4 * math.exp( - my_lambda * x ) + 4 * math.exp( - my_lambda * x ) * math.exp( - my_lambda *x ), 0, numpy.inf )

def mttf_block ( my_lambda ):
    
    return integrate.quad ( lambda x : 2 * math.exp( - my_lambda * x ) -  math.exp( - my_lambda * x ) *  math.exp( - my_lambda * x ) , 0, numpy.inf )


def analysis_redu (  my_lambda , machines , sort_time ):
    return { "MTTF of single machine" : float(1)/my_lambda , "MTTF of the System" : str (mttf_par(my_lambda)[0]) + 's' , "Clients served" : machines/3 , "Average Response Time of the system" :  str(sort_time) + 's'  } 

def analysis_block (  my_lambda , machines , sort_time ):
    return { "MTTF of single machine" : float(1)/my_lambda , "MTTF of the System" : str (mttf_block( my_lambda)[0] ) + 's' , "Clients served" : machines/2 ,  "Average Response Time of the system" : float(2 *  sort_time) - ( r_block(my_lambda, sort_time) *  sort_time  ) } 

print "\nLAMBDA\tMachines\tMTTF_comp\tMTTF_redu\tClients\t\tAvg_Resp_time\tMTTF_block\tClients\tAvg_Resp_time"
print "(fail/h)\t\t(hours)\t\t(hours)\t\tredu\t\tredu\t\t(hours)\t\tblock\tblock"
print "________________________________________________________________________________________________________________________"
my_lambda = 0.7
machines= 30
sort_time = 15
print my_lambda, "\t%d" % (machines), "\t\t%.3f" % ( float(1)/my_lambda ) , "\t\t%.3f" % ( mttf_par(my_lambda)[0] ), "\t\t%d" % (machines/3), "\t\t%d" % sort_time  , "\t\t%.3f" % ( mttf_block(my_lambda)[0] ), "\t\t%d" % ( machines/2 ),  "\t%d" % ( float(2 *  sort_time) - ( r_block(my_lambda, sort_time) *  sort_time  ) )

my_lambda = 10
machines= 30
print my_lambda, "\t%d" % (machines), "\t\t%.3f" % ( float(1)/my_lambda ) , "\t\t%.3f" % ( mttf_par(my_lambda)[0] ), "\t\t%d" % (machines/3), "\t\t%d" % sort_time  , "\t\t%.3f" % ( mttf_block(my_lambda)[0] ), "\t\t%d" % ( machines/2 ),  "\t%d" % ( float(2 *  sort_time) - ( r_block(my_lambda, sort_time) *  sort_time  ) )

my_lambda = 30
machines= 30
print my_lambda, "\t%d" % (machines), "\t\t%.3f" % ( float(1)/my_lambda ) , "\t\t%.3f" % ( mttf_par(my_lambda)[0] ), "\t\t%d" % (machines/3), "\t\t%d" % sort_time  , "\t\t%.3f" % ( mttf_block(my_lambda)[0] ), "\t\t%d" % ( machines/2 ),  "\t%d" % ( float(2 *  sort_time) - ( r_block(my_lambda, sort_time) *  sort_time  ) )


print ""

def bin_coeff(n, k):
    from math import factorial
    return factorial(n) // (factorial(k) * factorial(n - k))
