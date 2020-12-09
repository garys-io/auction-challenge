import json
from sys import stdin, stdout


# read config
with open('config.json') as f:
    config = json.load(f)

# convert list into dic and set for faster lookup later
config_sites = {}
for site in config['sites']:
    name = site['name']
    config_sites[name] = {
        'bidders': set(site['bidders']),
        'floor': site['floor']
    }

config_bidders = {}
for bidder in config['bidders']:
    name = bidder['name']
    config_bidders[name] = bidder['adjustment']

# read input bids from stdin
with open('input.json') as f:
    input_bids = json.load(f)

output = []
for b_obj in input_bids:

    # add empty [] and continue if site invalid or not found
    site = b_obj['site']
    if not site in config_sites:
        output.append([])
        continue

    # filter out bids
    # which doesn't have valid bidder in config
    # or the unit is not in b_obj
    valid_bidders = config_sites[site]['bidders']
    valid_units = set(b_obj['units'])

    bids = [b for b in b_obj['bids']
            if b['bidder'] in valid_bidders
            and b['unit'] in valid_units]

    # add adjusted bid to bids
    for b in bids:
        b['adjusted_bid'] = b['bid'] * (1 + config_bidders[b['bidder']])

    # filter out bids where adjusted_bid < floor
    valid_bids = [b for b in bids
                  if b['adjusted_bid'] >= config_sites[site]['floor']]

    # return empty list if no valid bid is found
    if not valid_bids:
        output.append([])
        continue

    # get the larget bid for each unit
    largest_bids = {}
    for b in valid_bids:
        if not b['unit'] in largest_bids:
            largest_bids[b['unit']] = b
        elif b['adjusted_bid'] > largest_bids[b['unit']]['adjusted_bid']:
            largest_bids[b['unit']] = b

    # format for output.json
    largest_bids_list = [{'bid': val['bid'], 'bidder': val['bidder'], 'unit': val['unit']}
                         for key, val in largest_bids.items()]

    # add them to ouput
    output.append(largest_bids_list)

# write output.json to stdout
stdout.write(json.dumps(output))
