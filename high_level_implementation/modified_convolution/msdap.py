def bin_add(x: str, y: str, op=None) -> str:
    """ 
    adds two stings of binary numbers bit by bit. for subtraction, 2's comp is taken
    Complement -> data_neg = bin_add(40*'0',data_pos, "sub")
    """
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
    padded_data = padding * ['0000'] + data
    return padded_data


def generate_u(n) -> list:
    with open("MSDAP_Coeff1.in", 'r') as MSDAP_coeff_file:
        MSDAP_coeff_str = MSDAP_coeff_file.read()

    MSDAP_coeff = MSDAP_coeff_str.split()

    with open("Rj1.in", 'r') as Rj_file:
        Rj_str = Rj_file.read()

    Rj_str_hex = Rj_str.split()

    with open("data1.in", 'r') as data_file:
        data_str = data_file.read()
    
    data_hex = data_str.split()
    data_hex_slice = data_hex[0:n+1]
    data_hex_slice = pad_data(data_hex_slice)
    u = [40 * '0' for _ in range(16)]

    offset = 0

    for Rj_count, i in enumerate(Rj_str_hex):
        Rj_int_curr = int(i, 16)

        for coeff_counter in range (Rj_int_curr):
            curr_coeff = MSDAP_coeff[coeff_counter + offset]
            curr_data_address = int(curr_coeff[1:], 16)
            curr_data_hex = data_hex_slice[255 - curr_data_address]
            curr_data_bin = sign_extender(curr_data_hex)
            if (curr_data_bin != 40*'0'): 
                if (curr_coeff[0] == '1'): #subtraction
                    u[Rj_count] = bin_add(u[Rj_count], curr_data_bin, 'sub')
                else:
                    u[Rj_count] = bin_add(u[Rj_count], curr_data_bin)

        offset += Rj_int_curr
    
    return u


def right_shift(num: str, step: int) -> str:
    sign = num[0]
    return sign * step + num[:40 - step]


def calculate_y(u):
    acc = 40 * '0'

    for i in range(16):
        acc = bin_add(acc, u[i])
        acc = right_shift(acc, 1)

    return acc

for n in range (0,5):
    u = generate_u(n)
    # print(u)
    y = calculate_y(u)
    y_ = int(y,2)
    print(hex(y_))