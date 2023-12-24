import argparse
import concurrent.futures
import time
import requests

def print_ascii_art():
    # Add your ASCII art here
    print("""

 +--^----------,--------,-----,--------^-,
 | |||||||||   `--------'     |          O
 `+---------------------------^----------|
   `\_,---------,---------,--------------'
     / XXXXXX /'|       /'
    / XXXXXX /  `\    /'
   / XXXXXX /`-------'
  / XXXXXX /
 / XXXXXX /
(________(                
 `------'    

SAY HELLO TO MY LITTLE FRIEND

    """)

def print_banner():
    print(f"\n{'*' * 40} HTTP(S) Load Tester : By D3ndr1t30x {'*' * 40}")

class LoadTester:
    def __init__(self, url, num_requests, num_concurrent):
        self.url = url
        self.num_requests = num_requests
        self.num_concurrent = num_concurrent
        self.stats = {'successes': 0, 'failures': 0, 'total_time': [], 'first_byte_time': [], 'last_byte_time': []}

    def make_request(self):
        start_time = time.time()
        try:
            response = requests.get(self.url)
            response_time = time.time() - start_time

            self.stats['total_time'].append(response_time)
            self.stats['first_byte_time'].append(response.elapsed.total_seconds())
            self.stats['last_byte_time'].append(response.elapsed.total_seconds())

            if response.ok:
                self.stats['successes'] += 1
            else:
                self.stats['failures'] += 1
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            self.stats['failures'] += 1

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_concurrent) as executor:
            executor.map(self.make_request, range(self.num_requests))

    def print_summary(self):
        print(f"\n{'*' * 40} Results {'*' * 40}")
        print(f"Successes: {self.stats['successes']}\nFailures: {self.stats['failures']}")
        print("Total Request Time (s) (Min, Max, Mean): {:.2f}, {:.2f}, {:.2f}".format(
            min(self.stats['total_time']), max(self.stats['total_time']), sum(self.stats['total_time']) / len(self.stats['total_time'])
        ))
        print("Time to First Byte (s) (Min, Max, Mean): {:.2f}, {:.2f}, {:.2f}".format(
            min(self.stats['first_byte_time']), max(self.stats['first_byte_time']), sum(self.stats['first_byte_time']) / len(self.stats['first_byte_time'])
        ))
        print("Time to Last Byte (s) (Min, Max, Mean): {:.2f}, {:.2f}, {:.2f}".format(
            min(self.stats['last_byte_time']), max(self.stats['last_byte_time']), sum(self.stats['last_byte_time']) / len(self.stats['last_byte_time'])
        ))

def main():
    print_ascii_art()
    print_banner()

    parser = argparse.ArgumentParser(
        description='HTTP(S) Load Tester',
        epilog='Happy Holidays!\nVisit https://github.com/yourusername/load-tester for more information and updates.'
    )
    parser.add_argument('-u', '--url', required=True, help='URL to test (include http:// or https://)')
    parser.add_argument('-n', '--num-requests', type=int, default=10, help='Number of requests to make')
    parser.add_argument('-c', '--num-concurrent', type=int, default=1, help='Number of concurrent requests')

    args = parser.parse_args()

    load_tester = LoadTester(args.url, args.num_requests, args.num_concurrent)
    load_tester.run()
    load_tester.print_summary()

if __name__ == "__main__":
    main()
