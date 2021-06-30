# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 11:54:15 2020

@author: AF47245
This is the entry point for python recommendation engine.
"""

from flask import request, make_response, Flask, jsonify
from starwars_app import create_app


app = create_app() 

@app.route('/ping', methods=['GET'])
def ping():
    """
    Check if API Alive
    ---
    tags:
      - Check Alive
    consumes:
      - application/json
    produces:
      - application/json
      - text/xml
      - text/html
    responses:
        200:
            description: Success
            schema:
            id: return_test
            properties:
        500:
            description: Error
    """
    
    return jsonify({"status": "Alive"}),200


'''
This is the entry method
This method calls mongoReader method, 
which reads documents from DB and process
'''
if __name__ == '__main__':
    try:
        # before_first_request()
        HOSTNAME = '0.0.0.0'
        PORT = 8080
        app.run(host=HOSTNAME, port=PORT, debug=False)
        
    except Exception as e:
       print(e)
  
