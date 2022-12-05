import numpy as np
import os

def valid_resolvent(c1, c2, res):
    if ((res > 1) | (res < -1)).sum(): return False

    duality = 0
    for i in range(len(res)):
        if (c1[i] * c2[i] == -1): duality += 1
    if duality != 1: return False

    return True

def new(clauses, res):
    return not(res == clauses).all(1).any()

def alpha_encoder(alpha):
    return np.array([clause_encoder(c) for c in alpha.split(' OR ')]) * -1

def clause_encoder(clause):
    literals = [x.strip() for x in clause.split('OR')]
    encoded = np.zeros(len(encode_table)).astype(int)

    for l in literals:
        if l[0] == '-':
            encoded[encode_table[l[-1]]] = -1
        else:
            encoded[encode_table[l]] = 1
        
    return encoded

def clause_decoder(encoded):
    if not encoded.any(): return '{}'
    
    temp = (encoded + 1)
    return ' OR '.join([decode_table[i][temp[i]] for i in range(len(temp)) if temp[i] != 1])

def print_clauses(clauses, start, end):
    output = ''
    output += str(end - start) + '\n'

    for i in range(start, end):
        output += clause_decoder(clauses[i]) + '\n'
    return output

def read_input(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        alpha = lines[0].strip()
        clauses = [x.strip() for x in lines[2:]]
        return alpha, clauses

def write_output(file_name, output):
    with open(file_name, 'w') as f:
        f.write(output)

def PL_RESOLUTION(encoded_clauses):
    output = ''

    old_end_index = len(encoded_clauses)
    new_start_index = 0
    new_end_index = len(encoded_clauses) 

    while True:
        for i in range(0, old_end_index):
            for j in range(new_start_index, new_end_index):
                c1 = encoded_clauses[i]
                c2 = encoded_clauses[j]
                res = c1 + c2
                if valid_resolvent(c1, c2, res) and new(encoded_clauses, res):
                    encoded_clauses = np.append(encoded_clauses, res.reshape(1, -1), axis=0)

        output += print_clauses(encoded_clauses, new_end_index, len(encoded_clauses))

        if new_end_index == len(encoded_clauses): return output + 'NO'
        if (encoded_clauses.any(axis = 1) == False).sum() == 1: return output + 'YES'

        new_start_index = new_end_index
        old_end_index = new_end_index
        new_end_index = len(encoded_clauses)

cwd = os.getcwd()
input_folder = os.path.join(cwd, 'INPUT')

for input_file in os.listdir(input_folder):
    file_name = os.path.join(input_folder, input_file)
    alpha, clauses = read_input(file_name)

    keys = []
    for c in clauses + [alpha]:
        ls = c.split('OR')
        for k in ls:
            k = k.strip().strip('-')
            if k not in keys:
                keys.append(k)

    encode_table = dict(zip(keys, range(len(keys))))
    decode_table = np.array([[f'-{c}', '', c] for c in keys])

    alpha_break = alpha.split(' OR ')
    clauses += alpha_break
    encoded_clauses = np.array([clause_encoder(c) for c in clauses])

    output_file = os.path.join(cwd, 'OUTPUT', 'output' + file_name[-5] + '.txt')
    write_output(output_file, PL_RESOLUTION(encoded_clauses))
