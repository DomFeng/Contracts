# writer by fengjianguang
# time: 2021/9/14 5:25 下午
import time
from web3 import Web3, HTTPProvider

from src.ContractPerformanceTest import contract_abi

contract_address = '0x3D30b722948215D36b17FAD416ad33d2D53735E4'
wallet_private_key = 'd355ce1b91b16a0fc6953cc20ec75e19060487a1a157679819d68595bc1e7ca3'
wallet_address = '0x8B8494cDAF423fAEB446F1a31697663eCA30690e'

w3 = Web3(HTTPProvider('https://dev-evm.dev.findora.org:8545'))

contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)


def burn(amount):
    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = contract.functions.burn(amount).buildTransaction({
        'chainId': 523,
        'gas': 140000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
    print('signed_txn:' + str(signed_txn))
    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print('result:' + str(result))
    tx_receipt = w3.eth.getTransactionReceipt(result)
    print('tx_receipt' + str(tx_receipt))

    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        print(tx_receipt)

    if tx_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    # processed_receipt = contract.events.OpinionBroadcast().processReceipt(tx_receipt)
    #
    # print(processed_receipt)

    # output = "Address {} broadcasted the opinion: {}" \
    #     .format(processed_receipt[0].args._soapboxer, processed_receipt[0].args._opinion)
    # print(output)
    #
    # return {'status': 'added', 'processed_receipt': processed_receipt}


def transfer(address, amount):
    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = contract.functions.transfer(address, amount).buildTransaction({
        'chainId': 523,
        'gas': 140000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
    print('signed_txn:' + str(signed_txn))
    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print('result:' + str(result))
    tx_receipt = w3.eth.getTransactionReceipt(result)
    print('tx_receipt' + str(tx_receipt))

    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        print(tx_receipt)

    if tx_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}


def balance_of(address):
    transact_hash = contract.functions.balanceOf(address)
    return transact_hash


# 调用burn
# burn(2000)
# 执行转账
transfer(0x8B8494cDAF423fAEB446F1a31697663eCA30690e, 2)
