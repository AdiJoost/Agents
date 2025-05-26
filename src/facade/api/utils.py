from flask import Response, make_response, jsonify



def createResponse (body: str, status: int) -> Response:
    response = make_response(jsonify(body), status)
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response