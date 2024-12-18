'''
A bit of mysticism
I often find myself needing an object which, while storing data, also manipulates
it in one swift go, and returns the result.

But everytime I gotta type something like:
res = Klass( data ).get_res()

Don't know what's a good alternative to that, so I've decided to make this little decorator
which is obviously not production-friendly.

Convention which I adopted is: a 'builder' class in question, named say 'Builder',
must have a method whose name is the class name in lowercase.
This decorator then intercepts class instantiation, produces new instance itself,
calls the init, fetches said method by name, and returns its' result.

'''

def Factory(klass):
    def inner(*args):
        instance = klass.__new__(klass)
        instance.__init__(*args)
        method_name = klass.__name__.lower()
        return getattr( instance, method_name )()
    return inner

