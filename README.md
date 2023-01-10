# subset-json

Subset the Confluence workflow JSON files based on a list of reach 
identifiers.

The list is passed into subset via a JSON file. A command line argument points
subset to the path of the input JSON file.

Assumes the following names for JSON files:
- basin.json
- continent.json
- reach_node.json
- reaches.json
- sets.json

***Note: Reaches are removed from sets. This may impact the validity of sets.***

## operation

Example command: `python3 subset.py -s /../../reach-subset.json -d /../../json-data -o /../../subset-out`

Command line arguments:
-s, --subset: Path to JSON file that contains a list of reach IDs to subset
-d, --datadir: Path to directory where JSON files to subset are located
-o, --outdir: Path to directory where subset files will be saved