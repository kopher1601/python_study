# python decorator

def copyright(func):
    def new_func():
        print("Hello from new_func")
        func()

    return new_func


@copyright
def smile():
    print(":-)")

smile()