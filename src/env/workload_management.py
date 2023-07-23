import numpy as np
import math


class workload:
    
    @staticmethod
    def sample_workload(local):
        workload = []
        for i in range(local):
            sample = np.random.uniform()
            if sample < 0.33:
                request_class = 'A'
                mean, std_dev = 5.5, 2.5
                shares = np.clip(np.random.normal(mean, std_dev), 1, 10)  
                dfaas_mb = np.clip(np.random.normal(13, 2.5), 1, 25) 
            elif sample < 0.67:
                request_class = 'B'
                mean, std_dev = 15.5, 2.5 
                shares = np.clip(np.random.normal(mean, std_dev), 11, 20)
                dfaas_mb = np.clip(np.random.normal(38, 2.5), 26, 50) 
            else:
                request_class = 'C'
                mean, std_dev = 25.5, 2.5
                shares = np.clip(np.random.normal(mean, std_dev), 21, 30)
                dfaas_mb = np.clip(np.random.normal(63, 2.5), 51, 75) 
            workload.append({'class': request_class, 'shares': shares, 'dfaas_mb': dfaas_mb, 'position': i})
        return workload

    @staticmethod
    def manage_workload(local ,CPU_capacity, DFAAS_capacity, queue_workload,
                        max_CPU_capacity, max_DFAAS_capacity):
        local_workload = workload.sample_workload(local)
        CPU_workload = []
        CPU_capacity = max_CPU_capacity
        DFAAS_capacity = max_DFAAS_capacity
        for request in queue_workload.copy(): 
            if CPU_capacity >= request['shares'] and DFAAS_capacity >= request['dfaas_mb']:
                CPU_capacity -= request['shares']
                DFAAS_capacity -= request['dfaas_mb']
                CPU_workload.append(request)
                queue_workload.remove(request)
            else:
                break
        print(f"CPU disponibile per le nuove requests: {CPU_capacity}")
        print(f"DFAAS disponibile per le nuove requests: {DFAAS_capacity}") 
         
        for request in local_workload:
            if CPU_capacity >= request['shares'] and DFAAS_capacity >= request['dfaas_mb']:
                CPU_capacity -= request['shares']
                DFAAS_capacity -= request['dfaas_mb']
                CPU_workload.append(request)
            else:
                queue_workload.append(request)
        
        print(f"Num requests in queue: {len(queue_workload)}")
        print(f"Shares in QUEUE: {sum(request['shares'] for request in queue_workload)}")
        print(f"MB in QUEUE: {sum(request['dfaas_mb'] for request in queue_workload)}")

        return CPU_workload, queue_workload

    @staticmethod
    def update_obs_space(queue_workload, queue_capacity, max_queue_capacity, t,
                         forward_capacity, forward_capacity_t, period, congestione):

        print(f"Num requests in queue: {len(queue_workload)}")
        # Update the queue_capacity
        queue_length_requests = len(queue_workload)
        queue_capacity = max(0, max_queue_capacity - queue_length_requests)
        queue_shares = sum(request['shares'] for request in queue_workload)
        
        forward_capacity = int(25 + 75 * (1 + math.sin(2 * math.pi * t / period)) / 2)
        forward_capacity_t = forward_capacity
        congestione = 1 if queue_capacity == 0 else 0
        
        t += 1
        if t == 100:
            done = True
        else:
            done = False

        return queue_capacity, queue_shares, t, done, forward_capacity, forward_capacity_t, congestione