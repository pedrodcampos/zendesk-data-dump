# zendesk-data-dump
Utility for Zendesk data extraction to csv file.
Currently supported endpoints: 
- `search`
- `articles` --_sections and categories are injected automaticaly_

## Usage

`python export.py [-h] [--instance INSTANCE] [--helpcenter HELPCENTER] [--username USERNAME] [--password PASSWORD] {search,articles}`

#### Optional Arguments

Argument | Name | Description
---|---|---
-h, --help| HELP|show this help message and exit
--instance |INSTANCE   |Zendesk instance url
--helpcenter| HELPCENTER|Zendesk helpcenter url
--username| USERNAME |  Admin account user email
--password |PASSWORD|   Admin account password

>_Alternatively, make a copy of the `.env.example` in this repo, rename it to `.env`. If you have access to multiple instances or helpcenters, you can keep your credentials in the `.env` file and define instance/helpcenter parameter when running the application._


#### Subcommands
Command  | Description
---|---
search|Download response of a search endpoint request. [See documentation](https://developer.zendesk.com/rest_api/docs/support/search#query-basics) and check what you can get from the search endpoint.
articles|Download all articles and related information from a helpcenter

