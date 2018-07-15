import sys, getopt
import flask
import base64
import pprint
import json
import test_schc
import lns_socket
import _thread

app = flask.Flask(__name__)

app.debug = True

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MzI4ODU5MzQsInVzZXJJbmZvIjp7ImFkbWluIjp0cnVlLCJ1c2VybmFtZSI6Im1hdHRoaWV1In19.ZRA6aUhY7jd_R9u9q6KmNrWmCEEBa895S1auFKJYd7HB-CtRhGI4bsNgdfUdWQTLfaJD7UG0uPvBgz3b7SWr-O_d-B8ybIXsd7JSYD-tBhisr72t3OsrCh8bBGfo5UUcXlShAG0MzYMNXuGe0RWlDAAWJL6PpAJhBTz6-IOQVqeDrjZLLtlHL58HtFEByTixPgqZIOBwtK-xVIjVcmfE7colkE_uID3V1a_9uapxmhWqxuNiU-nTwG-uqHvdGV0y99t3sLx9mzCo8lGUlfRvc77tRiQe7FjOhLPC5LOtksUg08_vm0qJ7LRa5x08SOouYW2-Q6oEzci3IdvlNRBXSw"

socket = lns_socket.LNSSocket(token)
@app.route('/lns', methods=['POST'])
def get_from_LNS():

    fromGW = flask.request.get_json(force=True)
    print ("HTTP POST RECEIVED")
    pprint.pprint(fromGW)
    if "data" in fromGW:
        payload = base64.b64decode(fromGW["data"])
        address = dict()
        address["fPort"] = fromGW["fPort"]
        address["devEUI"] = fromGW["devEUI"]
        socket.from_lns(payload, address)
        print (payload)


        print()
        print ("HTTP POST REPLY")
        resp = flask.Response(status=200)
        return resp

if __name__ == '__main__':
    print (sys.argv)

    defPort=8231
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hp:",["port="])
    except getopt.GetoptError:
        print ("{0} -p <port> -h".format(sys.argv[0]))
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print ("{0} -p <port> -h".format(sys.argv[0]))
            sys.exit()
        elif opt in ("-p", "--port"):
            defPort = int(arg)

    
    _thread.start_new_thread(test_schc.recv, (socket,))
    app.run(host="0.0.0.0", port=defPort)
