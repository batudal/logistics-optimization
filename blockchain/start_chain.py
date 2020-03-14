import json
import os
import hashlib
from random import randrange

blockchain_dir = "dir/"
filter = True

def get_hash(blockname):
    file = open(blockchain_dir + blockname, 'rb').read()
    return hashlib.sha256(file).hexdigest()

def verify():
    blocks = get_blocks()
    results = []
    global filter

    for file in blocks[1:]:
        prev_h = json.load(open(blockchain_dir + str(file)))['hash']
        prev_b = str(file -1)
        true_h = get_hash(prev_b)

        if prev_h == true_h:
            res = 'genuine'
        else:
            res = 'fake'
        results.append({'block':prev_b, 'result': res})

        if res == 'fake':
            filter = False

    return results

def hack_something():
    blocks = os.listdir(blockchain_dir)
    blocks = sorted([int(i) for i in blocks])
    rnd = randrange(len(blocks)-1)
    print('Hacking block[{}]...'.format(rnd))
    print('Increasing transaction value by tenfold. :]')
    data = json.load(open(blockchain_dir + str(blocks[rnd])))
    data['amount'] = str(int(data['amount']) * 10)

    with open(blockchain_dir + str(blocks[rnd]), 'w') as file:
        json.dump(data,file, indent=4)

def create_block(payer, amount, payee, p_hash=''):
    verify()
    if filter:
        blocks = get_blocks()
        last_block = blocks[-1]
        blockname = str(last_block + 1)
        p_hash = get_hash(str(last_block))

        data = {'payer': payer,
                'amount': amount,
                'payee': payee,
                'hash': p_hash}

        with open(blockchain_dir + blockname, 'w') as file:
            json.dump(data,file, indent=4)
    else:
        print("This blockchain is corrupt. \nSelf-destruction in progress. \nGood bye.")
        exit()

def get_blocks():
    blocks = os.listdir(blockchain_dir)
    return sorted([int(i) for i in blocks])

def reset():
    blocks = os.listdir(blockchain_dir)
    for i in blocks:
        os.remove("dir/" + i)

    genesis = {'payer': 'Miyamoto',
            'amount': 1,
            'payee': 'Satoshi',
            'hash': ''}

    with open(blockchain_dir + '0', 'w') as file:
        json.dump(genesis,file, indent=4)

def main():
    global filter
    verify()
    if filter:
        create_block('Satoshi', 1, 'Miyamoto')
    else:
        print("This blockchain is corrupt. \nRestarting blockchain.")
        reset()
        filter = True
        main()

if __name__ == '__main__':
    main()

while True:
    command = str(input('create/reset/hack: '))
    if command == 'create':
        payer = str(input('From: '))
        payee = str(input('To: '))
        amount = str(input('Amount: '))
        create_block(payer,amount,payee)
    elif command == 'reset':
        reset()
        break
    elif command == 'hack':
        #create_block('Hackers',0, 'Placeholder')
        hack_something()
        print(verify())
    else:
        print('Wrong command. Try "create" or "reset"')
