import os



def main():

        with open('kittens.in') as f:

            base_info = f.readline().split()

            # base info input
            num_videos = int(base_info[0])
            num_endpoints = int(base_info[1])
            num_request_description = int(base_info[2])
            num_cache_server = int(base_info[3])
            capacity_each_cache = int(base_info[4])

            # video size per video in list
            video_sizes = f.readline().split()

            # dict key endpoint index, value -> dict [cache_id] key and latency_ms as value
            endpoints = {}

            # list of latency of endpoint to data center
            latency_d = []


            for endpoint_index in range(0, num_endpoints):
                info = f.readline().split()

                print ("Info ", info)
                latency_d.append(int(info[0]))
                K_connections = int(info[1])

                print ("latencty ", latency_d[index]),
                print ("K connectios ", K_connections)


                endpoint_caches = {}
                for cache_index in range(0, K_connections):
                    cache = f.readline().split()

                    endpoint_caches[cache[0]] = cache[1]

                # inner dict to endpoints dict
                endpoints[endpoint_index] = endpoint_caches

                exit(-1)




            exit(-1)




main()
