#main.py
import web
import json, time, socket, sys

import master, sort_serv, example

#
#  Here is our little server. 
#  



# little example function
def make_text(string):
	return string

# This line maps the requests (server world) with the procedures that are defined under (python world)
# It is vary good to separate the functionalities
urls = ('/', 'index','/request', 'request', '/update', 'update')

# Here I tell which HTML template to load
render = web.template.render('templates/')


application = web.application(urls, globals())

my_form = web.form.Form(
                web.form.Textbox('', class_='textfield', id='textfield')
                )
                
		
un_bel_json = { }

sort_master = None


class request:

    def POST(self):
        
        global sort_master 
        
        # Here I answer to POST 
        form = my_form()
        form.validates()

        # Getting the Input
        input_list = map ( int , form.value['inputList'].split(' ') )
        method = form.value['method']


        n_of_servers = int( form.value['number_of_servers'] )
        availability = int( form.value['availability'] )
        failure_rate = int( form.value['lambda'] )
        analysis     = bool(form.value['calculate_analysis'])
        sort_time    = int( form.value['sort_time'] )
        print form.value

        period = 4 
        timeout = 10

        print 'Method is ' + method

        if method == "Redundancy":
            sort_master = master.MasterRedundant( True , n_of_servers, period, failure_rate, sort_time )
            un_bel_json['Update'] = ['Start : Started sorting on ' + str ( n_of_servers ) + ' redundant servers']
        else :
            if method == "Recovery Algorithm":
                sort_master = master.MasterRecoverySw( True , timeout, period, failure_rate, sort_time )
                un_bel_json['Update'] = ['Start : Started Recovery Sw']
            else :
                if method == "Recovery Hardware":
                    sort_master = master.MasterRecoveryHw( True , timeout, period, failure_rate, sort_time )
                    un_bel_json['Update'] = ['Start : Started Recovery Hw']
                else:
                    raise 

        if analysis : 
            try :
                import analysis
                
                if ( method == "Redundancy" ) :
                    un_bel_json['Analysis'] = analysis.analysis_redu( failure_rate, n_of_servers, sort_time )
                else : 
                    un_bel_json['Analysis'] = analysis.analysis_block( failure_rate, n_of_servers, sort_time )

            except:
                un_bel_json['Analysis'] = 'No_Library'

        print 'result ', un_bel_json

        sort_master.run( input_list )

        # I add the info to the json (data collection)

        # I return the json (data calculated)
        return json.dumps(un_bel_json)

class update:

    def POST(self):

        global sort_master

        data_output = {}
       
        state, has_finished, result = sort_master.update() 
        
        data_output['Update'] = state
    
        if has_finished :
            data_output['Result'] = result

        # I return the json (data calculated)
        return json.dumps(data_output)

# Here is where the index (main) page is loaded
class index:
    def GET(self):
	# I get the localhost name to print it in the main page, giusto per fare un po di Python
        hname = socket.gethostname()
        # I prepare the index page
	return render.List(hname, "   Waiting for Commands")

# serve        
if __name__ == '__main__':
        application.run()
