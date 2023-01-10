# -*- coding: utf-8 -*-
"""Subset: Subset Confluence workflow JSON files based on a list of reach 
identifiers.

The list is passed into subset via a JSON file. A command line argument points
subset to the path of the input JSON file.

Assumes the following names for JSON files:
- basin.json
- continent.json
- reach_node.json
- reaches.json
- sets.json

Note: Reaches are removed from sets. This may impact the validity of sets.

Example command: python3 subset.py -s /../../reach-subset.json -d /../../json-data -o /../../subset-out

Command line arguments:
-s, --subset: Path to JSON file that contains a list of reach IDs to subset
-d, --datadir: Path to directory where JSON files to subset are located
-o, --outdir: Path to directory where subset files will be saved
"""

# Standard imports
import argparse
import json
import pathlib

def get_args():
    """Create and return argparser with arguments."""

    arg_parser = argparse.ArgumentParser(description="Subset JSON files")
    arg_parser.add_argument("-s",
                            "--subset",
                            type=str,
                            help="Path to JSON file with list of reaches")
    arg_parser.add_argument("-d",
                            "--datadir",
                            type=str,
                            help="Path to directory where JSON files to subset are located")
    arg_parser.add_argument("-o",
                            "--outdir",
                            type=str,
                            help="Path to directory where subset files will be saved")
    return arg_parser

def get_reach_subset(json_file):
    """Load subset of reach identifiers from JSON file."""
    
    with open(json_file) as jf:
        reach_subset = json.load(jf)
    return reach_subset

def subset_basin(reach_subset, json_file, out_dir):
    """Subset basin.json to only include reach subset and write out data."""
    
    basin_subset_ids = list(set(list(map(lambda x: int(str(x)[0:6]), reach_subset))))
    
    with open(json_file) as jf:
        basin_data = json.load(jf)
    
    basin_subset_data = [ basin for basin in basin_data if basin["basin_id"] in basin_subset_ids ]    
    write_json(basin_subset_data, out_dir.joinpath("basin-subset.json"))
    
def subset_continent(reach_subset, json_file, out_dir):
    """Subset continent.json to only include reach subset and write out data."""
    
    continent_ids = list(set(list(map(lambda x: int(str(x)[0:1]), reach_subset))))
    
    with open(json_file) as jf:
        continent_data = json.load(jf)
        
    continent_subset_data = []
    for continent in continent_data:
        intersect = set(list(continent.values())[0]).intersection(set(continent_ids))
        if len(intersect) > 0:
            continent_subset_data.append(continent)
    write_json(continent_subset_data, out_dir.joinpath("continent-subset.json"))    
    
def subset_reach_node(reach_subset, json_file, out_dir):
    """Subset reach_node.json to only include reach subset and write out data."""
    
    with open(json_file) as jf:
        reach_data = json.load(jf)
    
    reach_subset_data = [ reach for reach in reach_data if int(reach[0]) in reach_subset ]        
    write_json(reach_subset_data, out_dir.joinpath("reach_node-subset.json"))
    
def subset_reaches(reach_subset, json_file, out_dir):
    """Subset reaches.json to only include reach subset and write out data."""
    
    with open(json_file) as jf:
        reach_data = json.load(jf)
    
    reach_subset_data = [ reach for reach in reach_data if int(reach["reach_id"]) in reach_subset ]    
    write_json(reach_subset_data, out_dir.joinpath("reaches-subset.json"))
    
def subset_sets(reach_subset, json_file, out_dir):
    """Subset sets.json to only include reach subset and write out data."""
    
    with open(json_file) as jf:
        sets = json.load(jf)
    
    set_subset_data = []
    for set_data in sets: 
        set_reach_ids = set([ int(reach_id["reach_id"]) for reach_id in set_data ])
        intersect = set_reach_ids.intersection(set(reach_subset))
        reach_data = []
        for reach in set_data:
            if reach["reach_id"] in intersect:
                reach_data.append(reach)
        if len(reach_data) > 0: set_subset_data.append(reach_data)
        
    write_json(set_subset_data, out_dir.joinpath("sets-subset.json"))

def write_json(data, json_file):
    """Write data to JSON file."""
    
    with open(json_file, 'w') as jf:
        json.dump(data, jf, indent=2)

def main():
    """Main function to execute the subset operations on various JSON files."""
    
    # Command line arguments
    arg_parser = get_args()
    args = arg_parser.parse_args()
    
    # Get reach identifiers to subset with
    reach_subset = get_reach_subset(args.subset)
    
    # Data directories
    data_dir = pathlib.Path(args.datadir)
    out_dir = pathlib.Path(args.outdir)
    
    # Subset data
    subset_basin(reach_subset, data_dir.joinpath("basin.json"), out_dir)
    subset_continent(reach_subset, data_dir.joinpath("continent.json"), out_dir)
    subset_reach_node(reach_subset, data_dir.joinpath("reach_node.json"), out_dir)
    subset_reaches(reach_subset, data_dir.joinpath("reaches.json"), out_dir)
    subset_sets(reach_subset, data_dir.joinpath("sets.json"), out_dir)
    
if __name__ == "__main__":
    main()