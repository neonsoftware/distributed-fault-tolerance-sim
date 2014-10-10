import sys
import datetime
import time
import threading

import sort_serv
import example


class Master(object) :

    def __init__(self, is_internal):

        self.is_internal = is_internal
        
        self.state = []
        self.input_list = None
        self.checkpoint = None
        self.all_finished = False
        self.result = None

    def run ( self, input_list  ):
        
        raise NotImplementedError( "This is an abstract method" ) 

    # Acceptance test
    # Check whether list is sorted
    def isSorted(self, list):

        for i in range(len(list)-1):
            if list[i] > list[i+1]:
                return False
        return True
       
    def update ( self ):

        temp_state = self.state

        self.state = []

        return ( temp_state, self.all_finished, self.result ) 
            

    def notify() :

        raise NotImplementedError( "This is an abstract method" ) 


class MasterRedundant(Master) :
    
    def __init__(self, is_internal, number_of_workers, period, failure_rate, sort_time ):
 
        self.servers = []
        self.results = []
        self.number_of_workers = number_of_workers
                
        self.number_finished = 0

        self.period = period
        self.failure_rate = failure_rate
        self.sort_time = sort_time


        Master.__init__(self, is_internal)

        for index in range( number_of_workers ):
            self.add_server( example.example_serv( index, 'worker_' + str( index ), self.period, self.failure_rate, self.sort_time ) )


    def add_server( self, newServer ):

        newServer.set_master( self )

        self.servers.append( newServer )
        
        self.state.append( 'Master-Redundant : Created a redundant server : ' + repr( newServer) ) 
    

    def run ( self, input_list ):
        
        for s in self.servers :

            print 'Starting a thread ! '
            self.input_list = input_list 
            thread = threading.Thread(target = s.run, args = ( self.input_list , ))
            thread.start()

        self.state.append( 'Master-Redundant : Threads running. '  )

    def finished( self, ide, dat, result ):

        self.state.append( 'Master-Redundant : Server ' + str(ide) + ' has finished in ' + str( dat ) + ' sec' + ' and result ' + repr(result) ) 

        self.number_finished = self.number_finished + 1

        self.results.append(result)

        if self.number_finished == len ( self.servers ) :
            self.vote()


    def vote( self ):

        votes = [] 

        for index in range( self.number_of_workers ): 
            votes.append( 1 )

        print 'Voting between :'

        for index in range ( self.number_of_workers ): 

            print self.results[index]

            for other in range ( self.number_of_workers ) :

                if other != index :

                    if self.results[other] == self.results[index] :

                        votes[index] += 1

        max_votes = max(votes)

        if max_votes > len(votes)/2 :
            self.result = self.results[votes.index(max_votes)]
        else:
            self.result = None

            print 'Voting NEGATIVE : Just ' + str(max_votes) + ' out of ' + str(len(votes)) + ' worker nodes agreed on the result'
            print 'Please repeat the calculation.'


        self.all_finished = True



class MasterRecoverySw(Master) :
    
    def __init__(self, is_internal, timeout ,  period, failure_time, sort_time):
 
        self.results = []
        self.period = period
        self.timeout = timeout
        self.started_primary_at  = None 
        self.started_recovery_at  = None
        self.failure_rate = failure_time
        self.sort_time = sort_time

        self.period = period

        self.add_servers()

        self.primary_has_finished = False 
        
        self.recovery_has_finished = True

        Master.__init__(self, is_internal)

        
    def add_servers( self ):

        self.primary_server = example.example_insertion_serv( 1, 'primary_1', self.period, self.failure_rate, self.sort_time  ) 
        self.primary_server.set_master(self)
        self.recovery_server = example.example_bubble_serv( 2, 'recovery_1', self.period , self.failure_rate, self.sort_time ) 
        self.recovery_server.set_master(self)


    def run ( self, input_list ):
            
        self.input_list = input_list 
        
        print 'Starting primary thread ! '
        self.primary_thread = threading.Thread(target = self.primary_server.run, args = ( input_list , ))
        self.primary_thread.start()
        
        self.started_primary_at  = datetime.datetime.now()
        
        threading.Timer( self.period , self.check_primary ).start()

        self.state.append( 'Master-Recovery-Sw : Threads running. '  )

    def check_primary( self ):

        if not self.primary_has_finished :

            time_passed = datetime.datetime.now() - self.started_primary_at 
            
            if self.primary_thread.isAlive() :

                if ( time_passed > datetime.timedelta ( seconds = self.timeout ) ) :
                
                    self.state.append( 'Master-Recovery-Sw : Primary has *Timeout* ' + str( self.timeout ) )
                    self.state.append( 'Master-Recovery-Sw : Starting recovery thread ! ')
                    
                    self.primary_has_finished = True
                    
                    self.started_recovery_at  = datetime.datetime.now()

                    self.recovery_thread = threading.Thread( target = self.recovery_server.continue_from_checkpoint , args = ( self.recovery_server.f_pickle , ) )
                    self.recovery_thread.start()
        
                    threading.Timer( self.period , self.check_primary ).start()

                
                else :

                    self.state.append( 'Master-Recovery-Sw : Primary server is actively running after ' + str(time_passed)  )
        
                    threading.Timer( self.period , self.check_primary ).start()

                
            else :
                
                print 'Primary has failed ! '
                print 'Starting recovery thread ! '
            
                self.primary_has_finished = True
                
                self.started_recovery_at  = datetime.datetime.now()

                self.recovery_thread = threading.Thread(target = self.recovery_server.run, args = ( self.input_list , ))
                self.recovery_thread.start()
                    
                threading.Timer( self.period , self.check_primary ).start()
        
        else :
            
            if not self.all_finished :

                time_passed = datetime.datetime.now() - self.started_recovery_at 
                
                if self.recovery_thread.isAlive() :

                    if ( time_passed > datetime.timedelta ( seconds = self.timeout ) ) :
                    
                        self.state.append( 'ERROR : Also Recovery has *Timeout* ' + str( self.timeout ) )
                        self.state.append( 'Both primary and recovery servers have failed, please retry the operation ! ')
                   
                        self.all_finished = True
                        self.result = None

                    
                    else :

                        self.state.append( 'Master-Recovery-Sw : Recovery server is actively running after ' + str(time_passed)  )
                        
                        threading.Timer( self.period , self.check_primary ).start()

                    
                else :
                    
                    self.state.append( 'ERROR : Recovery server has failed ! ')
                    self.state.append( 'Both primary and recovery servers have failed, please retry the operation ! ')
               
                    self.all_finished = True
                    self.result = None
        



    def finished( self, ide, dat, result ):

        if ide == 1 :
            
            self.state.append( 'Master-Recovery-Sw : Primary Server ' + str( ide ) + ' has finished in ' + str( dat ) + ' sec' + ' and result ' + repr( result) ) 
            self.primary_has_finished = True
        
        else :

            self.state.append( 'Master-Recovery-Sw : Recovery Server ' + str( ide ) + ' has finished in ' + str( dat ) + ' sec' + ' and result ' + repr( result) ) 
            self.recovery_has_finished = True


        self.all_finished = True
        self.result = result

class MasterRecoveryHw(MasterRecoverySw) :


    def add_servers(self) :

        self.primary_server = example.example_insertion_serv( 1, 'primary_1', self.period, self.failure_rate, self.sort_time  ) 
        self.primary_server.set_master(self)
        self.recovery_server = example.example_insertion_serv( 2, 'recovery_1', self.period , self.failure_rate, self.sort_time ) 
        self.recovery_server.set_master(self)


