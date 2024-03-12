import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.datetime.now()} - function {old_function.__name__} was called with arguments {args, kwargs}. Returned value: {result}\n")
            return result
        return new_function
    return __logger
