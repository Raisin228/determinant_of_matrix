# I connected the intertules module in order to determine the indices of elements in a combinatorial formula
from itertools import *
geese_flag = False

# we create a global list that will store the results of the minors
List_res = []
# this procedure outputs matrices in a beautiful way
def output_matrix(mat):
    max_len = 0
    for q in range(len(mat)):
        for h in range(len(mat)):
            max_len = max(max_len, len(str(mat[q][h])))

    for i in mat:
        for j in i:
            print(str(j).ljust(max_len), end=' ')
        print()

# function for search for the row with the largest number of 0 elements and memorize this index_row
# this function returns the index of the row with the largest quantity of 0s and the quantity of zeros in this row
def zero_row(mat):
    counter, max_counter, ind_row = 0, 0, 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 0:
                counter += 1
            if max_counter < counter:
                max_counter = counter
                ind_row = i
        counter = 0
    return ind_row, max_counter

# function for search for the column with the largest number of 0 elements and memorize this index_column
# this function returns the index of the column with the largest quantity of 0s and the quantity of zeros in this column
def zero_column(mat):
    counter, max_counter, ind_column = 0, 0, 0
    for k in range(len(mat)):
        for q in range(len(mat[k])):
            if mat[q][k] == 0:
                counter += 1
            if max_counter < counter:
                max_counter = counter
                ind_column = k
        counter = 0
    return ind_column, max_counter

# this function is needed in order to beautifully output 1 recursive decomposition action
def beautiful_output(k, r, c, mat, new_mat, elem):
    global List_res
    global r_z, c_z, geese_flag, const_len
    # if there has not been more than one decomposition, then you need to output a message
    # which says by rows or columns there will be decomposition
    if k == 0 and r[0] == r_z[0] and c[0] == c_z[0] and const_len == len(mat):
        print(f'Decomposition of the determinant by {r[0] + 1} lines' if r[1] > c[1] or r[1] == c[1] else f'Decomposition of the determinant into {c[0] + 1} columns')
    # if element is not equal to 0 then we output this element and an additional minor to it
    if r[0] == r_z[0] and c[0] == c_z[0] and elem[0] != 0 and len(new_mat) == const_len - 1:
        print(elem[0])
        output_matrix(new_mat)
        # I think we need to put the result of the recursion in a variable so as not to count the same thing many times
        next_step = rec_laplace(new_mat)
        if next_step < 0:
            # if minor < 0 => we put brackets and output this expression
            print(f'= {elem[0]} * ({next_step}) = {elem[0] * next_step}')
            List_res.append(elem[0] * next_step)
        elif next_step > 0:
            # if minor > 0 => we don't put brackets and output this expressions
            print(f'= {elem[0]} * {next_step} = {elem[0] * next_step}')
            List_res.append(elem[0] * next_step)
    # when we have reached the last step, we output a message with the result of recursion
    if r[0] == r_z[0] and c[0] == c_z[0] and k == len(mat) - 1 and len(new_mat) == const_len - 1 and geese_flag == False:
        print('The determinant of the matrix by the RECURSIVE formula:', end=' ')
        geese_flag = True
        if len(List_res) == 1:
            print(List_res[0])
        elif len(List_res) == 0:
            print(0)
        else:
            for i in range(len(List_res)):
                # put brackets if we need to it
                if List_res[i] < 0 and i != 0:
                    L_r = '(' + str(List_res[i]) + ')'
                else:
                    L_r = List_res[i]
                print(f'{L_r} + ' if i != len(List_res) - 1 else f'{L_r} = {sum(List_res)}', end='')
# <<<<<<<<<-----------------the beginning of the code associated with the recursive Laplace formula----------->>>>>>>>>>>>>
# function with BY THE RECURSIVE LAPLACE FORMULA
def rec_laplace(mat):
    global r_z, c_z, geese_flag
    # condition for exiting recursion
    if (len(mat) == 1):
        return mat[0][0]
    else:
        ans = 0
        # select the row or column by which we will decompose the recursion
        r, c = zero_row(mat), zero_column(mat)
        if ((r[1] == len(mat) or c[1] == len(mat)) and geese_flag == False):
            print('The determinant of the matrix by the RECURSIVE formula = 0', end='')
            geese_flag = True
            return 0
        # if quantity 0 in row >= quantity 0 in column
        elif (r[1] > c[1] or r[1] == c[1]):
            flag = False
            for i in range(len(mat[r[0]])):
                if mat[r[0]][i] != 0:
                    flag = True
                    break
            if flag:
                for k in range(len(mat[r[0]])):
                    new_mat = [[mat[i][j] for j in range(len(mat)) if i != r[0] and j != k] for i in range(0, len(mat))]
                    new_mat = [q for q in new_mat if len(q) != 0]
                    # chose sign element
                    elem = [mat[r[0]][k] if (r[0] + k) % 2 == 0 else -mat[r[0]][k]]
                    beautiful_output(k, r, c, mat, new_mat, elem)

                    # if el = 0 then we can don't call recursion
                    if mat[r[0]][k] != 0:
                        ans += elem[0] * rec_laplace(new_mat)
                    else:
                        ans += 0
            else:
                return 0

        # if quantity 0 in row < quantity 0 in column
        elif (r[1] < c[1]):
            flag = False
            for i in range(len(mat[c[0]])):
                if mat[i][c[0]] != 0:
                    flag = True
                    break
            if flag:
                for k in range(len(mat)):
                    new_mat = [[mat[i][j] for j in range(len(mat)) if i != k and j != c[0]] for i in range(0, len(mat))]
                    new_mat = [q for q in new_mat if len(q) != 0]
                    elem = [mat[k][c[0]] if (c[0] + k) % 2 == 0 else -mat[k][c[0]]]
                    beautiful_output(k, r, c, mat, new_mat, elem)

                    if mat[k][c[0]] != 0:
                        ans += elem[0] * rec_laplace(new_mat)
                    else:
                        ans += 0
            else:
                return 0
        return ans
# <<<<<<<<<-----------------the ending of the code associated with the recursive Laplace formula----------->>>>>>>>>>>>>

#<<<<<<<<<<-----------------the beginning of a function related to the combinatorial Leibniz formula----------->>>>>>>>>>>>>
# this function is needed in order to find the product of elements
# of one of the combinations in a combinatorial formula
# As an argument, the function takes a list that contains a combination of numbers from the matrix.
# This function returns the product of the list items
def multiplication_list(L):
    output = 1
    for t in L:
        output *= t
    return output

# the function takes a list of indexes of one of the combinations and finds the number of inversions in it.
# If inversion %2 == 0 => sign '+' otherwise '-'
def sign_combin(List):
    counter = 0
    for i in range(len(List) - 1):
        for j in range(i, len(List)):
            if List[i] > List[j]: # if element on the right less then we consider this as 1 inversion
                counter += 1
    if counter % 2 == 0:
        return True # true == '+'
    else:
        return False # false == '-'


ans = [] # 1 combination is stored
Num, res, counter = 0, 0, 0
# the number of the list with indexes obtained from permutations from intertuls
# in res stored answer from received from the combinatorial formula
# counter in order to output 10 combinations per line and moves the cursor to the next line
# combination formula
def combin_form_leibn(mat):
    global ans, ind, Num, res, counter # we make global variables so as not to lose the data obtained in recursion
    if len(mat) == 1: # condition for exiting recursion and output to the screen
        ans.append(mat[0][0])

        # beautiful output
        if Num != 0:
            # definition of the sign between the terms
            if sign_combin(ind[Num]):
                print(' +', end=' ')
                counter += 1
                if counter % 10 == 0 and counter != 0:
                    print()
            else:
                print(' -', end=' ')
                counter += 1
                # line wrapping
                if counter % 10 == 0 and counter != 0:
                    print()
        # the output of the element itself from the combination and, if necessary,
        # put it in brackets
        for q in range(len(ans)):
            if q != len(ans) - 1:
                if ans[q] < 0:
                    print(f'({ans[q]})', '*', sep='', end='')
                else:
                    print(ans[q], '*', sep='', end='')
            else:
                if ans[q] < 0:
                    print(f'({ans[q]})', sep='', end='')
                else:
                    print(ans[q], sep='', end='')

        # adding or subtracting the product of a given combination to res
        if sign_combin(ind[Num]):
            res += multiplication_list(ans)
        else:
            res -= multiplication_list(ans)
        # output at the very end of res
        Num += 1
        if Num == len(ind):
            print(f' = {res}')
    else:
        for i in range(len(mat)):
            ans.append(mat[0][i]) # adding one of the numbers to the combination
            metk = len(ans) # it is needed to slice the ans list at another recursion entry
            new_mat = [[mat[j][k] for k in range(len(mat[j])) if j != 0 and k != i] for j in range(len(mat))]
            new_mat = [new_mat[j] for j in range(len(new_mat)) if len(new_mat[j]) != 0] # a new matrix from which the element will be selected
            combin_form_leibn(new_mat)
            ans = ans[:metk - 1]
# <<<<<<<<<-----------------the ending of the code associated with the Leibniz combinatorial formula----------->>>>>>>>>>>>>

#<<<<<<<<<<-----------------the beginning of a function related to the Gauss method ----------->>>>>>>>>>>>>
# Greatest Common Divisor
def gcd(x, y):
    if (y == 0):
        return x
    else:
        return gcd(y, x % y)

# the Smallest Common Multiple (NOK)
# 2 scm numbers are passed to the function to be counted
# at the output we get their scm
def s_c_m(x, y):
    return (x * y) // gcd(x , y)

# in this function we are looking for the smallest first
# element with which we will reset the entire column
def min_el_col(mat, x):
    min_str = [x, mat[x][x]]
    for j in range(x + 1, len(mat)):
        if (abs(mat[j][x]) < abs(min_str[1]) and mat[j][x] != 0) or min_str[1] == 0:
            min_str[0] = j
            min_str[1] = mat[j][x]

    # we output a message that we are now rearranging the rows in places
    if x != min_str[0]:
        print(f'Permutation of {x + 1} lines and {min_str[0] + 1}', sep='\n')
    # changing the necessary lines in places
        for i in range(len(mat)):
            mat[min_str[0]][i], mat[x][i] = mat[x][i], mat[min_str[0]][i]
        return 1 # the signal is that the determinant of the original matrix get a minus
    return 0

# METHOD GAUSS
def gauss_method(mat):
    minus_counter = 0 # from rearranging strings in places
    answer = 1
    list_res = [] # it is needed in order to store the multipliers by which we multiply the strings
    # and at the end divide the answer by the product of the elements of this list
    k = 0 # to select a leading element
    while k != len(mat) - 1:
        indik = 0
        # calling a string permutation
        m_c = minus_counter
        minus_counter += min_el_col(mat, k)
        if minus_counter - m_c == 1:
            output_matrix(mat)
            print()
        # selecting an element to reset
        for i in range(k + 1, len(mat)):
            if mat[i][k] != 0:
                scm = s_c_m(abs(mat[k][k]), abs(mat[i][k])) # the total multiplier of the leading and selected
                mnoj2 = scm // mat[i][k]
                if mat[k][k] != 0:
                    mnoj1 = scm // mat[k][k]

                    # + -
                    if mat[i][k] * mnoj2 > 0 and mat[k][k] * mnoj1 < 0:
                        if mnoj2 != 1:
                            # output action
                            print(f'{mnoj2} * ({i + 1}) + {mnoj1} * ({k + 1})', end='\n')
                            indik += 1
                            # we add a multiplier that changed our matrix in order to divide it by it at the end
                            list_res.append(mnoj2)
                        else:
                            print(f'({i + 1}) + {mnoj1} * ({k + 1})', end='\n')
                            indik += 1
                        # subtraction or addition of two lines
                        for q in range(len(mat)):
                            mat[i][q] = mat[i][q] * mnoj2 + mat[k][q] * mnoj1
                    # - +
                    if mat[i][k] * mnoj2 < 0 and mat[k][k] * mnoj1 > 0:
                        if mnoj2 != 1:
                            print(f'{mnoj2} * ({i + 1}) + {mnoj1} * ({k + 1})', end='\n')
                            indik += 1
                            list_res.append(mnoj2)
                        else:
                            print(f'({i + 1}) + {mnoj1} * ({k + 1})', end='\n')
                            indik += 1
                        for q in range(len(mat)):
                            mat[i][q] = mat[i][q] * mnoj2 + mat[k][q] * mnoj1
                    # + +
                    if mat[i][k] * mnoj2 > 0 and mat[k][k] * mnoj1 > 0:
                        if mnoj2 != 1:
                            print(f'{mnoj2} * ({i + 1}) - {mnoj1} * ({k + 1})', end='\n')
                            indik += 1
                            list_res.append(mnoj2)
                        else:
                            print(f'({i + 1}) - {mnoj1} * ({k + 1})', end='\n')
                            indik += 1
                        for q in range(len(mat)):
                            mat[i][q] = mat[i][q] * mnoj2 - mat[k][q] * mnoj1
                    # - -
                    if mat[i][k] * mnoj2 < 0 and mat[k][k] * mnoj1 < 0:
                        if mnoj2 != 1:
                            print(f'{mnoj2} * ({i + 1}) + {mnoj1} * ({k + 1})', end='\n')
                            indik += 1
                            list_res.append(mnoj2)
                        else:
                            print(f'({i + 1}) + {mnoj1} * ({k + 1})', end='\n')
                            indik += 1
                        for q in range(len(mat)):
                            mat[i][q] = mat[i][q] * mnoj2 + mat[k][q] * mnoj1
        # output of a matrix with a zeroes column
        if indik != 0:
            output_matrix(mat)
            indik = 0
            print()

        # the next leading element
        k += 1

    # beautiful output
    print('The determinant of the matrix by the GAUSS METHOD:', end=' ')
    for i in range(len(mat)):
        if mat[i][i] < 0:
            print(f'({mat[i][i]}) *', end=' ')
        elif mat[i][i] >= 0:
            print(f'{mat[i][i]} *', end=' ')
        answer *= mat[i][i]
    div = multiplication_list(list_res)
    if div > 0:
        print(f'1/{div} =', end=' ')
    else:
        print(f'(-1/{abs(div)}) =', end=' ')

    # we divide the answer by those elements that increased our determinant
    # and adding a minus from the string permutation
    if minus_counter % 2 == 0:
        print(answer // multiplication_list(list_res))
    else:
        print(-answer // multiplication_list(list_res))
# <<<<<<<<<-----------------the ending of the code associated with the Gauss method----------->>>>>>>>>>>>>

# entering the name of a text file
name_file = input("Enter name your test file: ")
print()
# reading data from file
with open(name_file) as file:
    size_m = int(file.readline()) # reading first string
    if size_m == 0:
        print('В файле нет данных!!!')
        exit()
    matrix = [[int (j) for j in file.readline().split()] for i in range(size_m)] # reading matrix from file
    const_len = len(matrix)
    r_z, c_z = zero_row(matrix), zero_column(matrix) # need to definitions of the first step of entering recursion
    print("<<Your matrix from file>>")
    output_matrix(matrix)
    #if the matrix consists of only one element the result will be this element
    if len(matrix) == 1:
        print(f'The determinant of the matrix by the RECURSIVE formula: {matrix[0][0]}')
    else:
        rec_laplace(matrix)
    print('\n')

    # list column indexes are needed for permutations and sign determination
    valid_indexes = list(range(len(matrix)))
    # all kinds of permutations by columns
    ind = list(permutations(valid_indexes, len(valid_indexes)))
    # calling the Leibniz combinatorial formula
    print('<<The determinant of the matrix by the COMBINATORIAL formula>>')
    combin_form_leibn(matrix)
    print()

    # calling the method Gauss
    print('<<GAUSS METHOD>>')
    gauss_method(matrix)