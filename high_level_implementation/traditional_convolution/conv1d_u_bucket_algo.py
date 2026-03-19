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


def pad_data(data: list) -> list:
    """ pads data with zeros for calculation of y(n) for all n <= 254 """
    orig_len = len(data)
    width = 256
    padding = width - orig_len
    padded_data = padding * [40 * '0'] + data
    return padded_data


def bin_add(x: str, y: str, op=None) -> str:
    """ adds two stings of binary numbers bit by bit. for subtraction, 2's comp is taken """
    result = ['0'] * 40
    carry = 0

    if op == 'sub':
        y = list(y)
        for i in range(40):
            y[i] = '0' if y[i] == '1' else '1'
        y = ''.join(y)
        y = bin_add(y, '0' * 39 + '1')

    for i in range(40):
        result[39 - i] = str(int(x[39 - i]) ^ int(y[39 - i]) ^ carry)
        carry = (
            (int(x[39 - i]) & int(y[39 - i])) |
            (carry & int(y[39 - i])) |
            (int(x[39 - i]) & carry)
        )

    return ''.join(result)


def coeff_pad_bin(bin_num: str):
    """ pads string converted coeff to 32 bits """
    width = 32
    padding = max(0, width - len(bin_num))
    return "0" * padding + bin_num


def data_in_formatting(n: int):
    """ selects data from file and pads it to be 256 """
    with open("data1.in", 'r') as data_input:
        data = data_input.read()

    data = data.split()
    data = data[0:n + 1]

    for index, value in enumerate(data):
        data[index] = sign_extender(value)

    data = pad_data(data)

    return data


def generate_pot()-> list:
    """
    Generates list of list for power of twos.
    Each sublist contains an int number, sign gives sign, magnitude gives number of bit shift
    !! Uses multiplication operation.
    
    """
    with open("coeff.in", 'r') as coeff_file:
        coeff_data = coeff_file.read()

    coeff_list = coeff_data.split()
    pot = []

    for index, str_coeff in enumerate(coeff_list):
        coeff_list[index] = int(str_coeff, 16)
        coeff_temp = coeff_pad_bin(format(coeff_list[index], "b"))
        temp_list = []

        for j in range(16):
            temp = 0

            if coeff_temp[31 - j] == '1':
                temp = 16 - j
                temp = temp * (-1) if coeff_temp[15 - j] == "1" else temp
                temp_list.append(temp)

        pot.append(temp_list)

    return pot


def generate_u_list(pot: list, data: list):
    """
    Parameters: pot- list of list of ints that gives 
    """
    u = 16 * [40 * '0']
    Rj = 16 * [0]
    MSDAP_Coeff = [[] for _ in range(16)]

    for i in range(256):
        for j in range(len(pot[i])):
            pot_digit = pot[i][j]
            index = abs(pot_digit) - 1
            k = format(255-i, 'x')
            k = str(k)

            if len(k) < 3:
                k = (2 - len(k)) * '0' + k

            if pot_digit > 0:
                u[index] = bin_add(u[index], data[255 - i])
                entry = '0' + k
                Rj[index] += 1
            else:
                u[index] = bin_add(u[index], data[255 - i], op='sub')
                entry = '1' + k
                Rj[index] += 1

            MSDAP_Coeff[index].append(entry)

    # MSDAP_Coeff = [item for sublist in MSDAP_Coeff for item in sublist]
    return u, Rj, MSDAP_Coeff


def right_shift(num: str, step: int) -> str:
    sign = num[0]
    return sign * step + num[:40 - step]


def calculate_y(u):
    acc = 40 * '0'

    for exp in range(1, 17):
        shifted = right_shift(u[exp - 1], exp)
        acc = bin_add(acc, shifted)

    return acc


pot = generate_pot()
print(pot)
final_Rj = [0] * 16
final_MSDAP = []

for i in range(5):
    data = data_in_formatting(i)
    u, Rj, MSDAP = generate_u_list(pot, data)
    y = calculate_y(u)
    y_ = int(y,2)
    # print(hex(y_))
    # print(u)
    # print(Rj)
    # print(MSDAP)
    # final_MSDAP.extend(MSDAP)
