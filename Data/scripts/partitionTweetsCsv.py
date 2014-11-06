NUM_TWEETS_PER_FILE = 10000

all_tweets_filename = "tweets.csv"

f = open(all_tweets_filename)

num_tweets_in_file = 0

num_partition_files = 0

header_str = None
curr_partition_file = None

def getPartitionFilename(partition_num):
    return "%dk-tweets.csv" % (partition_num)

for line in f.readlines():
    if header_str == None:
        header_str = line
    else:
        if curr_partition_file == None:
            num_partition_files += 1
            curr_partition_file = open(getPartitionFilename(num_partition_files), "wb+")
            # write header to the top of the file
            curr_partition_file.write(header_str)
        elif (num_tweets_in_file > NUM_TWEETS_PER_FILE):
            # close the old partition file
            curr_partition_file.close()
            num_partition_files += 1

            # open the new partition file
            curr_partition_file = open(getPartitionFilename(num_partition_files), "wb+")
            num_tweets_in_file = 0
            # write header to top of the file
            curr_partition_file.write(header_str)

        # write this tweet to the current partition file
        curr_partition_file.write(line)
            
        num_tweets_in_file += 1

curr_partition_file.close()
