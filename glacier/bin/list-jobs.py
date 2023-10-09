import boto3
import os
import sys
from getopt import getopt, GetoptError
import json
from magico import MagicO


def usage():
    print(f"Usage: {os.path.basename(sys.argv[0]).rstrip('.py')} [-hv] vault_name", file=sys.stderr)


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

    if len(args) < 1 or len(args) > 1:
        usage()
        exit(2)

    vault_name = args[0]

    glacier = boto3.client('glacier')
    response = glacier.list_jobs(vaultName=vault_name)

    if verbose:
        print(json.dumps(response, indent=2))
    else:
        magic_response = MagicO(response)
        for job_item in magic_response.JobList:
            print(f"{job_item.CreationDate}: ", end='')
            print(f"{(job_item.Action + ' ' * 18)[:18]} ", end='')
            print(f"{(job_item.StatusCode + ' ' * 10)[:10]}; ", end='')
            print(f"JobId: {job_item.JobId}")


if __name__ == '__main__':
    main()
