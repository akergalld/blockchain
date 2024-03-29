# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 19:03:21 2023

@author: Ariel
"""

#Crear cadena de bloques (blockchain)

#improtar librerias
import datetime
import hashlib
import json
from flask import Flask, jsonify

#parte 1 crear cadena de bloques

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block={
                'index':len(self.chain)+1,
                'timestamp':str(datetime.datetime.now()),
                'proof':proof,
                'previous_hash':previous_hash
            }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
        
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if(hash_operation[:4])=='0000':
                check_proof=True
            else:
                new_proof+=1
        
        return new_proof
    
    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block=chain[0]
        block_index = 1
        while block_index <len(chain):
            current_block = chain[block_index]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(str(current_proof**2-previous_proof**2).encode()).hexdigest()
            if(hash_operation[:4])!='0000':
                return False
            previous_block=current_block
            block_index+=1
            return True
        
             
#parte 2 minar un bloque

#Crear una web con Flask
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
#crear una block chain
blockchain = Blockchain()

#minar un bloque
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
            'message':'Haz minado un nuevo bloque!',
            'index':block['index'],
            'timestamp':block['timestamp'],
            'proof':block['proof'],
            'previous_hash':block['previous_hash']
        }
    return jsonify(response),200

#Obtener la cadena de bloques completa
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
            'chain':blockchain.chain,
            'length':len(blockchain.chain)
        }
    return jsonify(response),200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    
    response = {
            'chain':blockchain.chain,
            'is_valid':blockchain.is_chain_valid(blockchain.chain)
        }
    return jsonify(response),200

#Ejecutar la app
app.run(host ='0.0.0.0',port=5000)