# we create a global list that will store the results of the minors
List_res = []
# this procedure outputs matrices in a beautiful way
def output_matrix(mat):
    for i in mat:
        for j in i:
            print(j, end=' ')
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
    global r_z, c_z
    global const_len
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
        else:
            # if minor > 0 => we don't put brackets and output this expressions
            print(f'= {elem[0]} * {next_step} = {elem[0] * next_step}')
            List_res.append(elem[0] * next_step)
    # when we have reached the last step, we output a message with the result of recursion
    if r[0] == r_z[0] and c[0] == c_z[0] and k == len(mat) - 1 and len(new_mat) == const_len - 1:
        print('The determinant of the matrix by the recursive formula:', end=' ')
        if len(List_res) == 1:
            print(List_res[0])
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
    global r_z, c_z
    # condition for exiting recursion
    if (len(mat) == 1):
        return mat[0][0]
    else:
        ans = 0
        # select the row or column by which we will decompose the recursion
        r, c = zero_row(mat), zero_column(mat)
        # if quantity 0 in row >= quantity 0 in column
        if (r[1] > c[1] or r[1] == c[1]):
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

        # if quantity 0 in row < quantity 0 in column
        elif (r[1] < c[1]):
            for k in range(len(mat)):
                new_mat = [[mat[i][j] for j in range(len(mat)) if i != k and j != c[0]] for i in range(0, len(mat))]
                new_mat = [q for q in new_mat if len(q) != 0]
                elem = [mat[k][c[0]] if (c[0] + k) % 2 == 0 else -mat[k][c[0]]]
                beautiful_output(k, r, c, mat, new_mat, elem)

                if mat[k][c[0]] != 0:
                    ans += elem[0] * rec_laplace(new_mat)
                else:
                    ans += 0
        return ans
# <<<<<<<<<-----------------the ending of the code associated with the recursive Laplace formula----------->>>>>>>>>>>>>

ans = []
counter = 0
def combin_form_leibn(mat):
    global ans, counter
    if len(mat) == 1:
        ans.append(mat[0][0])
        print(ans)
        counter += 1
    else:
        for i in range(len(mat)):
            ans.append(mat[0][i])
            metk = len(ans)
            new_mat = [[mat[j][k] for k in range(len(mat[j])) if j != 0 and k != i] for j in range(len(mat))]
            new_mat = [new_mat[j] for j in range(len(new_mat)) if len(new_mat[j]) != 0]
            combin_form_leibn(new_mat)
            ans = ans[:metk - 1]



# entering the name of a text file
name_file = input("Enter name your test file: ")
print()
# reading data from file
with open(name_file) as file:
    size_m = int(file.readline()) # reading first string
    matrix = [[int (j) for j in file.readline().split()] for i in range(size_m)] # reading matrix from file
    const_len = len(matrix)
    # r_z, c_z = zero_row(matrix), zero_column(matrix) # need to definitions of the first step of entering recursion
    # print("<<Your matrix from file>>")
    # output_matrix(matrix)
    # # if the matrix consists of only one element the result will be this element
    # if len(matrix) == 1:
    #     print(f'The determinant of the matrix by the recursive formula: {matrix[0][0]}')
    # else:
    #     rec_laplace(matrix)
    combin_form_leibn(matrix)
    print(counter)