import speedtest
from random import randint,random
import datetime

class speedtest_class:
    def get_data_online(self):
        servers = []
        # If you want to test against a specific server
        # servers = [1234]

        threads = None
        # If you want to use a single threaded test
        # threads = 1

        s = speedtest.Speedtest()
        print('getting data from speedtest...',flush=True,end='')
        s.get_servers(servers)
        s.get_best_server()
        s.download(threads=threads)
        s.upload(threads=threads)
        #s.results.share()

        results_dict = s.results.dict()
        print('done')
        return results_dict

    def get_st_fields(self):
        mock = {'download': 14269205.120757429, 'upload': 1597528.7789401715, 'ping': 40.966,
                'server': {'url': 'http://speedtest.hynetwifi.it:8080/speedtest/upload.php', 'lat': '45.5500',
                           'lon': '11.5500', 'name': 'Vicenza', 'country': 'Italy', 'cc': 'IT', 'sponsor': 'Hynet s r l',
                           'id': '3679', 'host': 'speedtest.hynetwifi.it:8080', 'd': 142.808631163175, 'latency': 40.966},
                'timestamp': '2020-11-21T07:25:20.441456Z', 'bytes_sent': 2433024, 'bytes_received': 18175472,
                'share': None,
                'client': {'ip': '151.95.140.16', 'lat': '46.0674', 'lon': '13.2364', 'isp': 'Wind Tre', 'isprating': '3.7',
                           'rating': '0', 'ispdlavg': '0', 'ispulavg': '0', 'loggedin': '0', 'country': 'IT'}}
        return mock

    def get_data(self, real=False):
        data = {'download': 14269205.120757429+random()*100,
                'upload': 1597528.7789401715+random()*100,
                'ping': 40.966+random()*10,
                'server': {'url': 'MOCK_DATA', 'lat': '45.5500',
                           'lon': '11.5500', 'name': 'MOCK', 'country': 'Italy', 'cc': 'IT', 'sponsor': 'MOCK',
                           'id': '3679', 'host': 'MOCK', 'd': 142.808631163175, 'latency': 40.966},
                'timestamp': datetime.datetime.now(), #'2020-11-21T07:25:20.441456Z',
                'bytes_sent': randint(2433024-100,2433024+100),
                'bytes_received': randint(18175472-100,18175472+100),
                'share': None,
                'client': {'ip': '151.95.140.999', 'lat': '46.0674', 'lon': '13.2364', 'isp': 'MOCK_DATA', 'isprating': '3.7',
                           'rating': '0', 'ispdlavg': '0', 'ispulavg': '0', 'loggedin': '0', 'country': 'IT'}}
        if real:
            data = self.get_data_online()
        return data

