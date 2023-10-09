import boto3
import os
import sys
from getopt import getopt, GetoptError


def usage():
    print(f"Usage: {os.path.basename(sys.argv[0]).rstrip('.py')} [-hv] vault_name job_id outfile", file=sys.stderr)


def main():
    verbose = False

    try:
        opts, args = getopt(sys.argv[1:], 'hv', ['help', 'verbose'])
    except GetoptError as err:
        print(err, file=sys.stderr)
        usage(2)

    for _o, _a in opts:
        if _o in ('-h', '--help'):
            usage()
            exit(0)
        elif _o in ('-v', '--verbose'):
            verbose = True
        else:
            print(f"Invalid option: {_o}", file=sys.stderr)
            usage()
            exit(2)

    if len(args) < 3 or len(args) > 3:
        usage()
        exit(2)

    vault_name = args[0]
    job_id = args[1]
    outfile = args[2]

    glacier = boto3.client('glacier')
    try:
        response = glacier.get_job_output(vaultName=vault_name, jobId=job_id)
    except:
        print(f"Not currently available for download.")
        exit(1)

    if response['Status'] == 200:
        response_body = response['body'].read()
        with open(outfile, 'wb') as f:
            f.write(response_body)
        print(f"Successfully downloaded content and saved to {outfile}")


if __name__ == '__main__':
    main()
