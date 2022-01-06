from nsetools import Nse


def print_hi(name):
    nse = Nse()
    print(nse.get_fno_lot_sizes())
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
