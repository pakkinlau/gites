import time

start_time = time.time()
# Print the results
end_time = time.time()
time_spent = end_time - start_time
print("Start Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
print("End Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
print("Time Spent:", "{:.2f} seconds".format(time_spent))