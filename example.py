import sort_serv, time


class example_serv( sort_serv.local_server ):


    def sort ( self, inp ) :    
        '''
        This is the main function you will have to implement. Its purpose is to implement the sort.

        This method returns a list that is the input list, sorted.
        '''

        inp.sort()

        return inp 


    def get_status( self ):
        '''
        In this funcion you return a string that represents your internal state.
        This is possible by using your inernal data members.

        NOTE : In general, in order to keep the state persisten it is needed that you use 
        internal data members to your class, as an example the 'self.temp' list that I use above
        '''

        return_string = 'I am ID ' + str(self.id) + ' and until now my result is' + repr (self.temp) + '\n' 

        return return_string

class example_insertion_serv( sort_serv.local_server ):

    # Find where to start the shifting.
    # Help method to insertion sort
    def setInOrder(self, m,input_list):
        e_m = input_list[m]
        for j in range(m):
            e_j = input_list[j]
            if (e_m < e_j):
                input_list = self.shift(j,m,input_list) 
                return input_list;

    # Help method to insertion sort
    def shift(self, j,m,input_list):
        e_in = input_list[j]
        input_list[j]=input_list[m]

        for k in range(j,m):
            e_out = input_list[k+1]
            input_list[k+1] = e_in
            e_in = e_out
        return input_list


    def sort ( self, input_list ) :    
        '''
        This is the main function you will have to implement. Its purpose is to implement the sort.

        This method returns a list that is the input list, sorted.
        '''

        self.checkpoint.running = True 

        print 'Insertion : Still ', self.checkpoint.remaining_time, ' to be slept.'

        while self.checkpoint.remaining_time > 0 :

            self.checkpoint.remaining_time = max ( 0, self.checkpoint.remaining_time - 3 )
            
            print 'I am about sleeping for ', self.checkpoint.remaining_time
            time.sleep( self.sort_time )

        # Insertion sort

        for i in range(len(input_list)-1):
            e0 = input_list[i]
            e1 = input_list[i+1]
            if (e0 > e1):
                input_list = self.setInOrder(i+1,input_list)

        return input_list



    def get_status( self ):
        '''
        In this funcion you return a string that represents your internal state.
        This is possible by using your inernal data members.

        NOTE : In general, in order to keep the state persisten it is needed that you use 
        internal data members to your class, as an example the 'self.temp' list that I use above
        '''

        return_string = 'I am ID ' + str(self.id) + ' and until now my result is blablaba \n' 

        return return_string

class example_bubble_serv( sort_serv.local_server ):


    def sort ( self, input_list ) :    
        '''
        This is the main function you will have to implement. Its purpose is to implement the sort.

        This method returns a list that is the input list, sorted.
        '''
        
        self.checkpoint.running = True 

        print 'Bubble : still ', self.checkpoint.remaining_time, ' to be slept.'

        while self.checkpoint.remaining_time > 0 :

            self.checkpoint.remaining_time = max ( 0, self.checkpoint.remaining_time - 3 )
            
            print 'I am about sleeping for ', self.checkpoint.remaining_time
            time.sleep( self.sort_time )

        
        # Bubble sort
        sortedness = 0
        self.temp = input_list

        for i in range(len(input_list)-1):
            e0 = input_list[i]
            e1 = input_list[i+1]
            if (e0 > e1):
                input_list[i] = e1
                input_list[i+1] = e0
                sortedness = 0
            else:
                sortedness += 1

        if (sortedness < (len(input_list)-1)):
            self.sort(input_list)
        else: 
            print self.get_status()
            return input_list


    def get_status( self ):
        '''
        In this funcion you return a string that represents your internal state.
        This is possible by using your inernal data members.

        NOTE : In general, in order to keep the state persisten it is needed that you use 
        internal data members to your class, as an example the 'self.temp' list that I use above
        '''

        return_string = 'I am ID ' + str(self.id) + ' and until now my result is temporary.\n' 

        return return_string
