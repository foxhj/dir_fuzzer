#!/usr/bin/env python

import argparse
import requests
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Fuzzing tool for fuzzing directories',
                                     epilog='Displays responses to status codes 200,204,301,302,307,401,403 by default',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--url', type=str, required=True, help='url to fuzz')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='wordlist to load')
    parser.add_argument('-a', '--all', action='store_true', help='display all error codes (usually WAY too verbose)')
    parser.add_argument('-x', '--extension', type=str, default=None, help='extension to append to payload (e.g., .php,.aspx,.pdf)')
    args = parser.parse_args()
    return args

def load_payloads(wordlist_file, extension):
    payloads = []
    try:
        with open(wordlist_file, 'r') as f:
            wordlist = f.read()
            payloads = wordlist.split('\n')
    except Exception as e:
        sys.exit(f'[-] Error loading wordlist: {e}')
    if extension:
        payloads = [payload + extension for payload in payloads]
    return payloads

def fuzz(url, payloads, display_all_codes, extension):
    display_codes = (200, 204, 301, 302, 307, 401, 403)
    print(f'[+] Fuzzing with {len(payloads)} payloads...\n\n')
    count = 1
    try:
        for payload in payloads:
            try:
                resp = requests.get(f'{url}/{payload}')
                if not display_all_codes:
                    if resp.status_code in display_codes:
                        print(f'[+] Payload: {payload} -- Status Code: {resp.status_code} -- Content-Length: {resp.headers["Content-Length"]}')
                else:
                    print(f'[+] Payload: {payload} -- Status Code: {resp.status_code} -- Content-Length: {resp.headers["Content-Length"]}')
                progress_percentage = count / len(payloads) * 100
                print(f'Progress: {count}/{len(payloads)} ({progress_percentage:.2f}%)', end='\r', flush=True)
                count += 1
            except Exception as e:
                print(f'[-] Error encountered: {e}')
                break
    except KeyboardInterrupt:
        print('[+] Stopping...')
    finally:
        return
    
def main():
    args = parse_arguments()
    payloads = load_payloads(args.wordlist, args.extension)
    try:
        requests.get(args.url)
    except Exception as e:
        sys.exit(f'[-] Error requesting url: {e}')
    fuzz(args.url, payloads, args.all, args.extension)

if __name__ == '__main__':
    main()