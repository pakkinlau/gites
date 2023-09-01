import time

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_spent = end_time - start_time
        print("Start Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
        print("End Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
        print("Time Spent:", "{:.2f} seconds".format(time_spent))
        return result
    return wrapper


### example usage
if __name__ == "__main__":
    @timing
    def your_function():
        # Your function's code here
        pass

    # Call your decorated function
    your_function()