def coeff_pad_bin(bin_num: str):
    """ pads string converted coeff to 32 bits """
    width = 32
    padding = max(0, width - len(bin_num))
    return "0" * padding + bin_num


def bin_add(x: str, y: str, op=None) -> str:
    """ adds two stings of binary numbers bit by bit. for subtraction, 2's comp is taken """
    result = ['0'] * 40
    carry = 0

    if op == 'sub':
        y = list(y)
        # complement bits
        for i in range(40):
            y[i] = '0' if y[i] == '1' else '1'
        y = ''.join(y)
        # add 1 to compelete 2's comp
        y = bin_add(y, '0' * 39 + '1')

    for i in range(40):
        result[39 - i] = str(int(x[39 - i]) ^ int(y[39 - i]) ^ carry)
        carry = (
            (int(x[39 - i]) & int(y[39 - i])) |
            (carry & int(y[39 - i])) |
            (int(x[39 - i]) & carry)
        )

    return ''.join(result)


def coeff_formatting()->list:
    """
    generates list of list of coeff converted to binary and padded with zeros to make it 32bit
    """

    with open("coeff.in", 'r') as coeff_file:
        coeff_data = coeff_file.read()

    coeff_list = coeff_data.split()

    for index, str_coeff in enumerate(coeff_list):
        coeff_list[index] = int(str_coeff, 16)
        coeff_list[index] = coeff_pad_bin(format(coeff_list[index], "b"))

    return coeff_list


def sign_extender(hex_str: str) -> str:
    """
    Sign extends 16bit data to 40bits.

    Parameters:
    hex_str: 4 letter string of hex number 

    Returns: 
    num: sign extended 40bit string
    """
    num = int(hex_str, 16)
    num = format(num, '016b')
    num = ("0" * 8 if num[0] == '0' else "1" * 8) + num + "0" * 16
    return num


def data_formatting()->list:
    """
    generate a list of positive and negative data converted to binary
    for direct add/sub
    """
    with open("data1.in", 'r') as data_input:
        data = data_input.read()

    data = data.split()
    bin_formatted_data = []
    for index, value in enumerate(data):
        temp_list = []
        data_pos = sign_extender(value)
        data_neg = bin_add(40*'0',data_pos, "sub")
        temp_list.append(data_pos)
        temp_list.append(data_neg)
        bin_formatted_data.append(temp_list)
    
    return bin_formatted_data


def pad_data(data: list) -> list:
    """ pads data with zeros for calculation of y(n) for all n <= 254 """
    orig_len = len(data)
    width = 256
    padding = width - orig_len
    padded_data = [[40 * '0', 40 * '0'] for _ in range(padding)] + data

    return padded_data


def data_slice(n:int,bin_formatted_data:list)->list:
    """ selects data from file and pads it to be 256 """

    data = bin_formatted_data[0:n + 1]
    data = pad_data(data)

    return data


def right_shift(num: str, step: int) -> str:
    sign = num[0]
    return sign * step + num[:40 - step]


def left_shift(num: str, step: int) -> str:
    return num[step:40] + '0' * step


def calculate_yn(data_slice:list, coeff_list:list, n:int) -> int:
    """
    implementation of ATS- add then shift
    y(n) = summ(k = 0->N) h(k) * x(n-k)
    """
    accum = 40 *'0'
    for k in range(256):
        curr_coeff = coeff_list[k]
        curr_data = data_slice[255 - k]

        temp = 40 * '0'

        for i in range(16):
            curr_POTdig = curr_coeff[31 - i]

            if curr_POTdig == '1':
                if curr_coeff[31 - i - 16] == '0':
                    temp = bin_add(temp, curr_data[0])
                else:
                    temp = bin_add(temp, curr_data[1])

            temp = right_shift(temp, 1)

        accum = bin_add(accum, temp)
    # for k in range(256):

    #     curr_coeff = coeff_list[k]
    #     curr_data = data_slice[255-k]
    #     if (curr_data[0] != 40 * '0'):
    #         accum = left_shift(accum, 16)
    #         for i in range(16):
    #             curr_POTdig = curr_coeff[31-i]
    #             if (curr_POTdig == '1'):
    #                 if (curr_coeff[31-i-16] == '0'):
    #                     accum = bin_add(accum, curr_data[0])
    #             else:
    #                 if (curr_coeff[31-i-16] == '1'):
    #                     accum = bin_add(accum, curr_data[1])
    #             accum = right_shift(accum, 1)
            

    accum = hex(int(accum,2))
    return accum


coeff_list = coeff_formatting()
bin_formatted_data = data_formatting()
for n in range(10):
    data_window = data_slice(n, bin_formatted_data)
    y_n = calculate_yn(data_window, coeff_list, n)
    print(y_n)

