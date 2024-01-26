from stix2 import Relationship
import random

def create_relationship(source, target, relationship_type):
    return Relationship(source_ref=source, target_ref=target, relationship_type=relationship_type)

def randomly_connect_objects(stix_objects, min_relations=1, max_relations=4):
    relationships = []
    # Initialize a dictionary to keep track of relations for each source object
    source_relations_count = {obj['id']: 0 for obj in stix_objects}

    for source in stix_objects:
        # Determine the number of relationships for this source object
        num_relations = random.randint(min_relations, min(max_relations, len(stix_objects) - 1))
        chosen_targets = set()

        while len(chosen_targets) < num_relations:
            target = random.choice(stix_objects)
            # Check if target is valid (not the same object, different type, and not already chosen)
            if target['id'] != source['id'] and target['type'] != source['type'] and target['id'] not in chosen_targets:
                possible_relationships = get_possible_relationships(source['type'], target['type'])
                if possible_relationships:
                    relationship_type = random.choice(possible_relationships)
                    # Enforce the maximum number of relations per source object
                    if source_relations_count[source['id']] < max_relations:
                        relationships.append(create_relationship(source['id'], target['id'], relationship_type))
                        source_relations_count[source['id']] += 1
                        chosen_targets.add(target['id'])

    return relationships


def get_possible_relationships(source_type, target_type):
    relationship_map = {
        "threat-actor": {"campaign": ["attributed-to"], "intrusion-set": ["attributed-to"], "malware": ["uses"], "tool": ["uses"]},
        "identity": {"threat-actor": ["attributed-to"], "campaign": ["attributed-to"]},
        "malware": {"vulnerability": ["targets"], "tool": ["uses"]},
        "indicator": {"campaign": ["indicates"], "malware": ["indicates"], "threat-actor": ["indicates"]},
        "campaign": {"threat-actor": ["attributed-to"], "intrusion-set": ["part-of"]},
        "intrusion-set": {"campaign": ["part-of"], "threat-actor": ["attributed-to"]},
        "vulnerability": {"malware": ["exploits"]},
        "attack-pattern": {"malware": ["uses"], "threat-actor": ["uses"]},
        "tool": {"threat-actor": ["uses"], "malware": ["uses"]}
    }
    return relationship_map.get(source_type, {}).get(target_type, [])

# Example usage:
# stix_objects = [... list of STIX objects ...]
# relationships = randomly_connect_objects(stix_objects, max_relations=2)