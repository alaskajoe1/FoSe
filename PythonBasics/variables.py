

x = 6

def example():
    z = 5
    global x
    print(x)
    print(x+5)

    # doesn't work
    x += 5

example()