import boto3
import os
import sys
from getopt import getopt, GetoptError
import json


def usage():
    print(f"Usage: {os.path.basename(sys.argv[0]).rstrip('.py')} [-hv] vault_name archive_id", file=sys.stderr)


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
    archive_id = args[1]

    glacier = boto3.client('glacier')
    try:
        response = glacier.delete_archive(vaultName=vault_name, archiveId=archive_id)
    except:
        print("The archive ID was not found.")
        exit(1)

    if verbose:
        print(json.dumps(response, indent=2))
    else:
        print(f"Archive deleted: {archive_id}")
        # print(f"HTTPStatusCode: {MagicO(response).ResponseMetadata.HTTPStatusCode}")


if __name__ == '__main__':
    main()
