import glob
import os
import random
import time
from multiprocessing import Process, Manager, Lock


def clear():
    files = glob.glob('*.txt')
    for file in files:
        os.remove(file)


def create():
    start_time = time.time()
    for j in range(20):
        p = Process(target=file_creator, args=(j,))
        p.start()
    end_time = time.time()
    print(end_time - start_time)


def calc():
    manager = Manager()
    files = glob.glob('*.txt')
    lock = Lock()
    total_sum = manager.Value('sum', 0)
    process_list = []

    for file in files:
        process = Process(target=calculator(total_sum, lock, file), args=(total_sum, lock))
        process.start()
        process_list.append(process)

    for i in process_list:
        i.join()
    print(total_sum.value)


def calculator(total_sum, lock, file):
    row_file = open(file, "r")
    row_file = row_file.read()
    nums = row_file.replace("\n", " ")
    array_nums = nums.split(" ")
    sum_in_file = 0
    for num in array_nums:
        if num != "":
            sum_in_file = sum_in_file + int(num)
    lock.acquire()
    total_sum.value = total_sum.value + sum_in_file
    lock.release()


def file_creator(j):
    for creator in range(50):
        info(j, creator)


def info(j, creator):
    line = ""
    randfile = open("Random{}_{}.txt".format(str(j), str(creator)), "w")

    for i in range(random.randint(20, 100)):
        for k in range(random.randint(5, 40)):
            line = line + str(random.randint(0, 9)) + " "

        randfile.write(line)
        randfile.write("\n")
        line = ""

    randfile.close()


if __name__ == '__main__':
    clear()
    #create()
    calc()
