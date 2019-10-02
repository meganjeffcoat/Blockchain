import hashlib
import requests



import sys


# TODO: Implement functionality to search for a proof
def proof_of_work(final_block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """
    # return proof

    proof = 0
    while valid_proof(final_block, proof) is False:
        proof += 1

    return proof 

def valid_proof(final_block, proof):
        guess = f'{final_block}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one

        r = requests.get(url = node + '/last_block')
        data = r.json()
        final_block = data["final_block"]["previous_hash"]

        new_proof = proof_of_work(final_block)

        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        proof_data = {"proof": new_proof}
        r = requests.post(url = node + '/mine', json = proof_data)
        data = r.json()
        
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data.get("message") == "New Block Forged":
            coins_mined += 1
            print(f"You have: {coins_mined} coins")
        print(data.get("message"))
