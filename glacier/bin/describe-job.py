import boto3
import os
import sys
from getopt import getopt, GetoptError
import json
from magico import MagicO


def usage():
    print(f"Usage: {os.path.basename(sys.argv[0]).rstrip('.py')} [-hv] vault_name job_id", file=sys.stderr)


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

    if len(args) < 2 or len(args) > 2:
        usage()
        exit(2)

    vault_name = args[0]
    job_id = args[1]

    glacier = boto3.client('glacier')
    response = glacier.describe_job(vaultName=vault_name, jobId=job_id)

    if verbose:
        print(json.dumps(response, indent=2))
    else:
        magic_response = MagicO(response)
        print(f"JobId: {magic_response.JobId}")
        print(f"Action: {magic_response.Action}", end='')
        print(f"{' ' + magic_response.ArchiveId if 'ArchiveId' in magic_response else ''}")
        print(f"StatusCode: {magic_response.StatusCode}")
        print(f"{'Not ' if not magic_response.Completed else ''}Completed")


if __name__ == '__main__':
    main()
