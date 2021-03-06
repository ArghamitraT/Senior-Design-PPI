#this file does the data processing on the vector machine data to corporate with
#HRNN
import numpy as np
import time

#the formation of individual matrix
def convertToMatrix(sqnc):
    sqnc = sqnc+[0]*(1200-len(sqnc))
    matrix_1 = np.array(sqnc).reshape((30,40))
    return matrix_1

#from all protiens it makes matrix
def multiple_matrix(sqnc_num, file_num):
    trimester = time.strftime("_%Y_%m_%d-%H__%M_%S")
    matrices = []
    for sqnc in sqnc_num:
        matrix_1 = convertToMatrix(sqnc)
        matrices.append(matrix_1)
    np.save('TEST_VERY_HARD_negatives'+file_num+trimester, matrices)

#converts sequence to number from the dictionary
def convert_sqnc_to_num(sequence):
    sqnc_num = []
    index_aa = {24: 'X', 1: '_GO', 2: '_EOS', 3: '_UNK', 4: 'A', 5: 'R', 6: 'N', 7: 'D', 8: 'C', 9: 'Q', 10: 'E',
                11: 'G', 12: 'H', 13: 'I', 14: 'L', 15: 'K', 16: 'M', 17: 'F', 18: 'P', 19: 'S', 20: 'T', 21: 'W',
                22: 'Y', 23: 'V'}
    rvrs_index_aa = dict()
    for key,val in index_aa.items():
        rvrs_index_aa[val] = key
    for line in sequence:
        sqnc_1 = []
        for letter in line:
            number = rvrs_index_aa[letter]
            sqnc_1.append(number)
        #sqnc_1 = sqnc_1.ljust(2000, '0')
        sqnc_num.append((sqnc_1))
    return (sqnc_num)

def extract_sequence(str_to_sqnc_dic, data_A, data_B):
    sequenceA = []
    sequenceB = []
    length = []
    for A, B in zip(data_A, data_B):
        sqnc_A = str_to_sqnc_dic[A]
        sqnc_B = str_to_sqnc_dic[B]
        sequenceA.append(sqnc_A)
        sequenceB.append(sqnc_B)
        length.append(len(sqnc_A + sqnc_B))
    return (sequenceA, sequenceB, max(length))


#opens the file where we have all the sequences
def open_sqnc_file(sqnc_filename):
    print("extract sequence")
    str_to_sqnc_dic = {}
    with open(sqnc_filename, "r") as f:
        i = 0
        for line in f:
            if (i % 2) == 0:
                token = line.strip('\n>')
            else:
                sqnc = line.strip('\n>')
                str_to_sqnc_dic[token] = sqnc
                #lines.append([token, line])
            i+=1
    return str_to_sqnc_dic

#extract protein id from text file
def extract_id(lines):
    print("id")
    data_A = []
    data_B = []
    for line in lines:
        split_data = str(line).split()
        data_A.append(split_data[0])
        data_B.append(split_data[1])
    return data_A, data_B

def open_file(filename, sqnc_filename):
    text_file = open(filename, "r")
    lines = text_file.readlines()
    data_A, data_B = extract_id(lines)
    str_to_sqnc_dic = open_sqnc_file(sqnc_filename)
    sequenceA, sequenceB, max_len = extract_sequence(str_to_sqnc_dic, data_A, data_B)
    sqnc_numA = convert_sqnc_to_num(sequenceA)
    sqnc_numB = convert_sqnc_to_num(sequenceB)
    multiple_matrix(sqnc_numA, file_num = 'A')
    multiple_matrix(sqnc_numB, file_num = 'B')


def main():

    #filename = "/home/argha/WORK/extracted_data/extracted_data/positive_list.npy"
    #sqnc_filename = "/home/at/work/dataset/ECEN_404_dataset/vector_machine_data/sequences.fasta"
    filename = "/home/argha/WORK/extracted_data/vector_machine_data/VERY_HARD/TEST_VERY_HARD_negatives.txt"
    sqnc_filename = "/home/argha/WORK/extracted_data/vector_machine_data/sequences.fasta"
    open_file(filename, sqnc_filename )
    print("DONE")


if __name__ == "__main__":
    main()