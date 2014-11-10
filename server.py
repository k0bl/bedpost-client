import logging
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from os import system
from jsonrpc import JSONRPCResponseManager, dispatcher



@dispatcher.add_method

def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]

#Create a method "xfer" that takes the username parameter and logs that the user 
#started bedpost
@dispatcher.add_method

def xfer(**kwargs):
	print "starting bedpost transfer"
	print kwargs," started transfers"
	system('python bedpostmock.py')


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s 
    dispatcher["add"] = lambda a, b: a + b

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

	
if __name__ == '__main__':
    run_simple('localhost', 4000, application)
