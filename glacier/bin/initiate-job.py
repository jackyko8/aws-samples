import boto3
import os
import sys
from getopt import getopt, GetoptError
import json
from magico import MagicO


def usage():
    print(f"Usage: {os.path.basename(sys.argv[0]).rstrip('.py')} [-hv] vault_name (inventory-retrieval | archive-retrieval archive_id)", file=sys.stderr)


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
    job_type = args[1]

    job_params = {'Type': job_type}

    if job_type == 'inventory-retrieval':
        if len(args) > 2:
            usage()
            exit(2)
    elif job_type == 'archive-retrieval':
        if len(args) < 3 or len(args) > 3:
            usage()
            exit(2)
        else:
            archive_id = args[2]
            job_params['ArchiveId'] = archive_id

    glacier = boto3.client('glacier')
    response = glacier.initiate_job(vaultName=vault_name, jobParameters=job_params)

    if verbose:
        print(json.dumps(response, indent=2))
    else:
        print("Job Parameters:")
        print(json.dumps(job_params, indent=2))
        print(f"Job created with JobId: {MagicO(response).jobId}")


if __name__ == '__main__':
    main()
