import os


num_videos = None
num_endpoints = None
num_request_description = None
num_cache_server = None
capacity_each_cache = None
video_sizes = None
endpoints = {}
latency_d = []
requests = []
example_name = "kittens"

class Request(object):

    def __init__(self, v, e, n):
        self.v = v
        self.e = e
        self.n = n


def main():
    global num_videos, num_endpoints, num_request_description, num_cache_server, capacity_each_cache, video_sizes, endpoints, requests, latency_d, example_name

    with open(example_name + '.in') as f:

        base_info = f.readline().split()

        # base info input
        num_videos = int(base_info[0])
        num_endpoints = int(base_info[1])
        num_request_description = int(base_info[2])
        num_cache_server = int(base_info[3])
        capacity_each_cache = int(base_info[4])

        # video size per video in list
        video_sizes = f.readline().split()
        video_sizes = [int(x) for x in video_sizes]

        # dict key endpoint index, value -> dict [cache_id] key and latency_ms as value
        endpoints = {}

        # list of latency of endpoint to data center
        latency_d = []


        for endpoint_index in range(0, num_endpoints):
            info = f.readline().split()

            print ("Info ", info)
            latency_d.append(int(info[0]))
            K_connections = int(info[1])

            #print ("latencty ", latency_d[endpoint_index]),
            #print ("K connectios ", K_connections)


            endpoint_caches = {}
            for cache_index in range(0, K_connections):
                cache = f.readline().split()

                endpoint_caches[int(cache[0])] = int(cache[1])

            # inner dict to endpoints dict
            endpoints[endpoint_index] = endpoint_caches

        requests = []
        for request_index in range(num_request_description):
            v, e, n = f.readline().split()
            requests.append(Request(int(v), int(e), int(n)))


main()
print (len(latency_d))
