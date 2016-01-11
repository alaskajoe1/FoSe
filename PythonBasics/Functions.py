
#paremeters go in ()
def example():
    print('Basic Function')
    z = 3+9
    print(z)

def simple_addition(num1, num2):
    answer = num1 + num2
    print(num1, " + ", num2, " = ", answer)

def simple(num1, num2):
    pass

# gives num2 the default value of 5
# but it can be overwritten
def simple(num1, num2=5):
    pass

example()

#same order
simple_addition(3,5)

#or can define them explicitly
simple_addition(num2=5, num1=7)