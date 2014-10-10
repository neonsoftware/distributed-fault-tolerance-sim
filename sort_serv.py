import sys, datetime, time, threading, pickle, random

import thread

class Checkpoint(object):

    def __init__( self, input_list, running, remaining_time ):

        self.input_list     = input_list
        self.running        = running 
        self.remaining_time = remaining_time 



class Sort_serv_interface(object) :

    def __init__ ( self, ident , file_name, period, failure_rate, sort_time ):


        self.f_out          = './tmp/' + file_name + '.out'
        self.f_log          = './tmp/' + file_name + '.log'
        self.f_pickle       = './tmp/' + file_name + '.pickle'

        self.file_name = file_name
        self.id = ident
        self.period = period
        self.sort_time = sort_time
        
        self.state = None

        # Failure Rate (in failures/minute )
        # mttf is expressed in seconds between failure   60/
        self.mttf = int( 60/failure_rate )

        self.running = False

    def set_master( self, master) :
        self.master = master

    def continue_from_checkpoint( self, checkpoint_file_name ):
        ''' This method is the bare copy of run with the continue '''
        ''' '''
   
        print 'I m coninouting form checkpoint !'

        self.load_checkpoint( checkpoint_file_name )

        threading.Timer( self.period , self.print_status ).start()
        threading.Timer( self.period , self.save_checkpoint ).start()
        
        self.initial_time = datetime.datetime.now()
       
        # Standard deviation
        sigma = int( self.mttf / 3 )
        alive_time = self.mttf + random.randint( - sigma , sigma ) 

        # print 'Alive time : ' + str( alive_time )  
        threading.Timer( alive_time , self.kill ).start()
        
        self.running = True
        
        sorted_list = self.sort( self.checkpoint.input_list )

        self.return_result( sorted_list )
        
        self.running = False

    
    def run( self, inp ):

        self.checkpoint = Checkpoint( inp, True, self.sort_time )

        threading.Timer( self.period , self.print_status ).start()
        threading.Timer( self.period , self.save_checkpoint ).start()
        
        self.initial_time = datetime.datetime.now()
       
        # Standard deviation
        sigma = int( self.mttf / 3 )
        alive_time = self.mttf + random.randint( - sigma , sigma ) 

        # print 'Alive time : ' + str( alive_time )  
        threading.Timer( alive_time , self.kill ).start()
        
        self.running = True
        
        sorted_list = self.sort( self.checkpoint.input_list )

        self.return_result( sorted_list )
        
        self.running = False

    def sort( self, inp ):

        raise NotImplementedError( "This is an abstract method" ) 
        
    def get_status( self ):

        raise NotImplementedError( "This is an abstract method" ) 


    def print_status( self ):

        if self.running :
            time_struct = time.localtime()

            f = open ( self.f_log , 'a' )
            f.write( self.get_status( ) )
            f.flush()
            f.close()

            threading.Timer( self.period , self.print_status ).start()

    def save_checkpoint( self ):

        if self.running :
            pickle.dump( self.checkpoint, open( self.f_pickle , "wb" ) )
            print 'I am checkpointing myself !'
    
    def load_checkpoint( self, pickle_file ):

        self.checkpoint = pickle.load(open( pickle_file , "rb" ) )
        print 'I am loading my checkpoint !'


    def kill(self):
        print ">>>>> Died " + str(self.id)
        thread.exit()
    
    def __repr__(self):

        return 'Id : ' + str(self.id) + ' Period : ' + str(self.period) + ' Files : ' + self.file_name + '.{out,log,pickle}' 
    
class local_server(Sort_serv_interface) :

    def return_result( self, sorted_list  ):

        print 'Server ' + str(self.id) + ': notifying result to master ' + repr ( self.master )

        self.master.finished( self.id, datetime.datetime.now() - self.initial_time, sorted_list )


class dist_server(Sort_serv_interface) :

    def return_result( self, sorted_list  ):

        f = open ( self.f_out , 'w' )
        f.write( sorted_list )
        f.flush()
        f.close()

        print 'Server ' + self.id + ': writing result to file.'

        print 'Server ' + self.id + ': notifying to master ' + repr ( self.master )

        self.master.finished( self.id, datetime.datetime.now() - self.initial_time, None  )


