import json
import requests
import sha3

bytecode = "0x60606040526040516040806107228339810160405280805190602001909190805190602001909190505081600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055504260028190555080600360006101000a81548160ff021916908360ff1602179055505050610645806100dd6000396000f300606060405260043610610078576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680630b97bc861461007d578063109e94cf146100a6578063231fd9d4146100fb5780632ef2d55e1461015157806370dea79a14610180578063fd922a4214610195575b600080fd5b341561008857600080fd5b6100906101ea565b6040518082815260200191505060405180910390f35b34156100b157600080fd5b6100b96101f0565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b341561010657600080fd5b61014f60048080356000191690602001909190803560ff169060200190919080356000191690602001909190803560001916906020019091908035906020019091905050610215565b005b341561015c57600080fd5b610164610517565b604051808260ff1660ff16815260200191505060405180910390f35b341561018b57600080fd5b61019361052a565b005b34156101a057600080fd5b6101a86105df565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b60025481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b61021d610605565b600080600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561027c57600080fd5b87600019168430604051808381526020018273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166c01000000000000000000000000028152601401925050506040518091039020600019161415156102ea57600080fd5b6040805190810160405280601c81526020017f19457468657265756d205369676e6564204d6573736167653a0a333200000000815250925082886040518083805190602001908083835b6020831015156103595780518252602082019150602081019050602083039250610334565b6001836020036101000a03801982511681845116808217855250505050505090500182600019166000191681526020019250505060405180910390209150600182888888604051600081526020016040526000604051602001526040518085600019166000191681526020018460ff1660ff16815260200183600019166000191681526020018260001916600019168152602001945050505050602060405160208103908084039060008661646e5a03f1151561041557600080fd5b50506020604051035190506000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614151561047b57600080fd5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc859081150290604051600060405180830381858888f1935050505015156104dd57600080fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b600360009054906101000a900460ff1681565b42600360009054906101000a900460ff1660ff1660025401118061059b57506000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614155b156105a557600080fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6020604051908101604052806000815250905600a165627a7a72305820e6ffc6597070f8051b4469dda7a372fad38da4b679834df53e308fbc0f9648ee0029"

def hit(command, params):
	return requests.post('http://localhost:7545', data='{"jsonrpc":"2.0","method":"' + command + '","params":' + json.dumps(params) + ',"id":1}')

def printBalances(client, server):
	clientBalance = hit('eth_getBalance', [client,"latest"]).json()['result']
	serverBalance = hit('eth_getBalance', [server,"latest"]).json()['result']
	print "Client Balance: " + clientBalance
	print "Server Balance: " + serverBalance

accounts = hit('eth_accounts', []).json()['result']
client = accounts[0]
server = accounts[1]

timeout = "0000000000000000000000000000000000000000000000000100000000000000"
down_payment = '005000000000000000'

gasEstimate = hit('eth_estimateGas', [{"from": client,"data":bytecode + "000000000000000000000000" + server[2:] + timeout}]).json()['result']
transaction = hit('eth_sendTransaction', [{"from": client,"gas":gasEstimate,"value":"0x" + down_payment,"data":bytecode + "000000000000000000000000" + server[2:] + timeout}]).json()['result']
contractAddress = hit('eth_getTransactionReceipt', [transaction]).json()['result']['contractAddress']

msg = '0000000000000000000000000000000000000000000000002000000000000000'

k = sha3.keccak_256()
k.update((msg + contractAddress[2:]).decode('hex'))
h = k.hexdigest()

signedMessage = hit('eth_sign', [client, "0x" + h]).json()['result']

signature = signedMessage[2:]
r = signature[:64]
s = signature[64:128]
if signature[128:130] == "01":
	v = "000000000000000000000000000000000000000000000000000000000000001c"
else:
	v = "000000000000000000000000000000000000000000000000000000000000001b"

gasEstimate = hit('eth_estimateGas', [{"from": server,"to":contractAddress,"data":"0x231fd9d4" + h + v + r + s + msg}]).json()['result']
result = hit('eth_sendTransaction', [{"from": server,"gas":gasEstimate + "0","to":contractAddress,"data":"0x231fd9d4" + h + v + r + s + msg}]).json()['result']
result = hit('eth_getTransactionReceipt', [result]).json()
print json.dumps(result)

#transaction = hit('eth_call', [{"from": client,"to":contractAddress,"data":"0x1c6f6e8a"}]).json()
#print json.dumps(transaction)

#printBalances(client,server)
#result = hit('eth_getTransactionReceipt', [transaction]).json()
#print json.dumps(result)

#printBalances(client, server)