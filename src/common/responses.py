from flask import jsonify
from graphql.error import format_error as format_graphql_error
from graphql.error import GraphQLError


def generate_empty_response(status_code):
    return {"statusCode": status_code}


def generate_response(body, status_code):
    response = generate_empty_response(status_code)
    response["msg"] = body
    return response


def internal_error_response(err):
    output = {"error": "500 error: Internal Server Error occurred."}
    resp = jsonify(output)
    resp.status_code = 500
    return resp


def unauthorized_response():
    output = {"error": "401 error: Unauthorized."}
    resp = jsonify(output)
    resp.status_code = 401
    return resp


def method_not_allowed_response():
    output = {"error": "405 error: Method Not Allowed."}
    resp = jsonify(output)
    resp.status_code = 405
    return resp


def connection_establish():
    output = {"msg": "Application has access to the DB", "statuscode": 200}
    resp = jsonify(output)
    resp.status_code = 200
    return resp


def service_unavailable():
    output = {"error": "503 error: Service Unavailable."}
    resp = jsonify(output)
    resp.status_code = 503
    return resp


def rec_not_found_response():
    output = {"errors": "No record exists in database", "statuscode": 200}
    return jsonify(output)


def method_not_found_response():
    output = {
        "msg": "404 error: This route is currently not supported.\
            See API documentation.",
        "statuscode": 404,
    }
    resp = jsonify(output)
    resp.status_code = 404
    return resp


def no_data():
    output = {"errors": "No data found in the request body", "statuscode": 400}
    resp = jsonify(output)
    resp.status_code = 400
    return resp


def bad_request(result):
    errors_list = []
    if result:
        for error in result.errors:
            errors_list.append(format_graphql_error(error))
    if not errors_list:
        errors_list.append({"errors": "Bad request"})
    output = {"errors": errors_list}
    resp = jsonify(output)
    resp.status_code = 400
    return resp


def generate_error_response(err, status_code):
    return generate_response({"msg": err}, status_code)
