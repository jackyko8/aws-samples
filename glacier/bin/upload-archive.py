import boto3
import os
import sys
from getopt import getopt, GetoptError
import json
from magico import MagicO


def usage():
    print(f"Usage: {os.path.basename(sys.argv[0]).rstrip('.py')} [-hv] vault_name file_path [archive_description]", file=sys.stderr)


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

    if len(args) < 2:
        usage()
        exit(2)

    vault_name = args[0]
    file_path = args[1]

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            body = f.read()
    else:
        raise Exception(f"{file_path} is not a file.")

    params = {
        'vaultName': vault_name,
        'body': body,
    }

    params['archiveDescription'] = \
        os.path.basename(file_path) if len(args) == 2 \
        else ' '.join(args[2:])

    glacier = boto3.client('glacier')
    response = glacier.upload_archive(**params)

    if verbose:
        print(json.dumps(response, indent=2))
    else:
        print(f"ArchiveId: {MagicO(response).archiveId}")


if __name__ == "__main__":
    main()
