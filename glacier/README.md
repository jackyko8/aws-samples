# Amazon S3 Glacier

## Installation

```bash
git clone https://github.com/jackyko8/aws-samples.git
cd aws-samples/glacier
pip install -r requirements.txt
```

Optional installations:

- Install [jq](https://jqlang.github.io/jq/download/).
- Use the "jq filter suggestion" items in the User Guide as a trial:
  - Example: `../bin/list-vaults -v | jq -r ".VaultList[] | {VaultName, CreationDate, SizeInBytes}"`
- If the `-v` option is specified, the Python script in `./aws-samples/glacier/bin` will output a JSON document, which can be parsed by `jq`.


## User Guide

- List vaults: `bin/list-values`
  - jq filter suggestion: `.VaultList[] | {VaultName, CreationDate, SizeInBytes}`
- Upload archive: `bin/upload-archive value_name file_name`
  - jq filter suggestion: `.archiveId`
- Inventory retrieval: `bin/initiate-job accsoft-archive inventory-retrieval`
  - jq filter suggestion: `.jobId`
- Archive retrieval: `bin/initiate-job-archive-retrieval vault_name archive_id`
  - jq filter suggestion: `.jobId`
- List jobs: `bin/list-jobs vault_name`
  - jq filter suggestion: `.JobList[] | {Action, CreationDate, StatusCode, JobId}`
- Describe job: `bin/describe-job vault_name job_id`
  - jq filter suggestion: `{Action, ArchiveId, StatusCode, JobId}`
- Get job output: `bin/get-job-output vault_name job_id outfile`
  - jq filter suggestion: `.status` being 200
- Delete archive: `bin/delete-archive vault_name archive_id`
  - jq filter suggestion: `.ResponseMetadata.HTTPStatusCode` being 204
