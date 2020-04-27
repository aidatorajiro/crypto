import urllib.request, json, base64
import zclib

class RPCException(Exception):
    pass

class JSONRPC:
    def __init__(self, addr, user, password):
        self.addr = addr
        self.user = user
        self.password = password
    
    def __getattr__(self, attrname):
        def callrpc(arg):
            obj = {"jsonrpc": "2.0", "method": attrname, "params": arg, "id": "jsonrpc"}
            method = "POST"
            data = json.dumps(obj).encode("utf-8")
            basic = base64.b64encode('{}:{}'.format(self.user, self.password).encode('utf-8'))
            headers = {"Content-Type" : "application/json", "Authorization": "Basic " + basic.decode('utf-8')}
            request = urllib.request.Request(self.addr, data=data, method=method, headers=headers)
            with urllib.request.urlopen(request) as response:
                ret = json.loads(response.read().decode("utf-8"))
                if ret['error'] == None:
                    return ret['result']
                else:
                    raise RPCException(ret['error'])
        
        return callrpc

rpc = JSONRPC("http://127.0.0.1:8080/", 'user', 'password')

if __name__ == '__main__':
    tx = rpc.gettransaction([rpc.listunspent([])[0]['txid']])
    txraw = tx['hex']
    txparsed = zclib.getTransaction(bytes.fromhex(txraw))
    tx_z = rpc.gettransaction([rpc.z_listunspent([])[0]['txid']])
    txraw_z = tx_z['hex']
    txparsed_z = zclib.getTransaction(bytes.fromhex(txraw_z))
    print(txparsed)
    print(txparsed_z)
