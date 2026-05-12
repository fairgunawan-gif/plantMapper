"""
Planting algorithm for generating garden layouts.
Implements companion planting logic and map generation.
"""

from plants_data import get_plant_by_id


def get_plant_compatibility_score(plant1, plant2):
    """
    Check if two plants can be planted next to each other and get compatibility score.
    Returns:
        0 - Incompatible (should avoid each other)
        1 - Neutral (can be planted together)
        2 - Good companions
    """
    # Check if plants are incompatible
    if plant1['id'] in plant2.get('avoid_plants', []) or \
       plant2['id'] in plant1.get('avoid_plants', []):
        return 0
    
    # Check if plants are companions
    if plant1['id'] in plant2.get('companions', []) or \
       plant2['id'] in plant1.get('companions', []):
        return 2
    
    return 1


def count_consecutive_plants(row, plant_id):
    """Count consecutive plants of the same type from the end of the row."""
    count = 0
    for i in range(len(row) - 1, -1, -1):
        if row[i]['plant']['id'] == plant_id:
            count += 1
        else:
            break
    return count


def group_selected_plants(selected_plant_ids, database):
    """
    Group selected plants by type and count instances.
    Returns a list of groups with plant info and count.
    """
    plant_counts = {}
    for plant_id in selected_plant_ids:
        plant_counts[plant_id] = plant_counts.get(plant_id, 0) + 1
    
    groups = []
    for plant_id, count in plant_counts.items():
        plant = get_plant_by_id(plant_id, database)
        if plant:
            groups.append({
                'plant': plant,
                'count': count
            })
    
    return groups


def find_best_next_plant(current_plant, remaining_groups, current_row, row_width, plot_width_cm, 
                         group_same_plants, mix_culture, group_fleece, max_group_size):
    """
    Find the best next plant to place based on compatibility and algorithm settings.
    
    Args:
        current_plant: The last placed plant (or None if first)
        remaining_groups: List of available plant groups
        current_row: Current row being built
        row_width: Current total width used in the row (in cm)
        plot_width_cm: Total available width (in cm)
        group_same_plants: Whether to group same plants together
        mix_culture: Whether to use mix culture algorithm
        group_fleece: Whether to group plants with same fleece requirements
        max_group_size: Maximum number of same plants to group together
    
    Returns:
        The best plant group to place next, or None if no suitable plant found
    """
    best_score = 0
    best_group = None
    
    if not remaining_groups:
        return None
    
    # First, try to continue the current group if possible and grouping is enabled
    if group_same_plants and current_plant and len(current_row) > 0:
        consecutive_count = count_consecutive_plants(current_row, current_plant['id'])
        if consecutive_count < max_group_size:
            # Look for more of the same plant
            same_group = next((g for g in remaining_groups if g['plant']['id'] == current_plant['id']), None)
            if same_group and (row_width + same_group['plant']['spacing']['plant_to_plant'] <= plot_width_cm):
                return same_group
    
    # Look for the best option among remaining groups
    for group in remaining_groups:
        plant = group['plant']
        plant_spacing = plant['spacing']['plant_to_plant']
        
        # Skip if adding this plant would exceed plot width
        if row_width + plant_spacing > plot_width_cm:
            continue
        
        # Count consecutive same plants from the end of current row
        consecutive_count = count_consecutive_plants(current_row, plant['id'])
        
        # Skip if would exceed max_group_size (only if grouping is enabled)
        if group_same_plants and consecutive_count >= max_group_size:
            continue
        
        # Calculate base compatibility score
        score = get_plant_compatibility_score(current_plant, plant) if current_plant else 1
        
        # Calculate grouping score based on enabled algorithms
        grouping_score = 0
        
        if current_plant:
            # Priority 1: Same plant grouping
            if group_same_plants and plant['id'] == current_plant['id'] and consecutive_count < max_group_size:
                grouping_score = 10  # Highest priority
            # Priority 2: Companion planting with fleece consideration
            elif mix_culture:
                has_matching_fleece = current_plant['needs_fleece_cover'] == plant['needs_fleece_cover']
                if score == 2:  # Good companion
                    grouping_score = 8 if has_matching_fleece else 6
                else:  # Neutral companion
                    grouping_score = 7 if has_matching_fleece else 5
            # Priority 3: Fleece grouping
            elif group_fleece and current_plant['needs_fleece_cover'] == plant['needs_fleece_cover']:
                grouping_score = 4
            else:
                grouping_score = 1  # Default score for any valid placement
        else:
            grouping_score = 1
        
        if grouping_score > best_score:
            best_score = grouping_score
            best_group = group
    
    # If no suitable plant found and mix culture is enabled, try to find any plant with double spacing
    if not best_group and mix_culture:
        for group in remaining_groups:
            plant = group['plant']
            double_spacing = plant['spacing']['plant_to_plant'] * 2
            if row_width + double_spacing <= plot_width_cm:
                # Return a modified group with double spacing
                modified_plant = plant.copy()
                modified_plant['spacing'] = plant['spacing'].copy()
                modified_plant['spacing']['plant_to_plant'] = double_spacing
                return {
                    'plant': modified_plant,
                    'count': group['count']
                }
    
    return best_group


def generate_planting_map(selected_plant_ids, plot_width_m, plot_length_m, database,
                          group_same_plants=True, mix_culture=False, group_fleece=False,
                          max_group_size=3):
    """
    Generate a planting map based on selected plants and plot dimensions.
    
    Args:
        selected_plant_ids: List of selected plant IDs
        plot_width_m: Plot width in meters
        plot_length_m: Plot length in meters
        database: Plant database to use
        group_same_plants: Whether to group same plants together
        mix_culture: Whether to use mix culture algorithm
        group_fleece: Whether to group plants with same fleece requirements
        max_group_size: Maximum number of same plants to group together
    
    Returns:
        List of columns, each containing a list of plant placements
    """
    # Convert dimensions to cm
    plot_width_cm = plot_width_m * 100
    plot_length_cm = plot_length_m * 100
    
    # Group selected plants
    plant_groups = group_selected_plants(selected_plant_ids, database)
    if not plant_groups:
        return []
    
    # Initialize the map
    planting_map = []
    remaining_groups = plant_groups.copy()
    
    while remaining_groups:
        current_row = []
        row_width = 0
        max_row_to_row_distance = 0
        
        # Keep adding plants to the column while there's space
        while row_width < plot_width_cm and remaining_groups:
            # Get the last plant in the current column (if any)
            last_plant = current_row[-1]['plant'] if current_row else None
            
            # Find the best next plant
            next_group = find_best_next_plant(
                last_plant, remaining_groups, current_row, row_width, 
                plot_width_cm, group_same_plants, mix_culture, group_fleece, max_group_size
            )
            
            if not next_group:
                break
            
            # Determine group status
            group_start = len(current_row) == 0 or current_row[-1]['plant']['id'] != next_group['plant']['id']
            group_end = True  # Will be updated if next plant is same type
            
            # Add the plant
            current_row.append({
                'plant': next_group['plant'],
                'distance': next_group['plant']['spacing']['plant_to_plant'],
                'row_to_row': next_group['plant']['spacing']['row_to_row'],
                'group_start': group_start,
                'group_end': group_end
            })
            
            # Update the previous plant's group_end if it's the same type
            if len(current_row) > 1 and current_row[-2]['plant']['id'] == next_group['plant']['id']:
                current_row[-2]['group_end'] = False
            
            row_width += next_group['plant']['spacing']['plant_to_plant']
            max_row_to_row_distance = max(max_row_to_row_distance, next_group['plant']['spacing']['row_to_row'])
            
            # Update remaining count and remove group if depleted
            next_group['count'] -= 1
            if next_group['count'] == 0:
                remaining_groups = [g for g in remaining_groups if g != next_group]
        
        # Add the column to the map
        if current_row:
            planting_map.append({
                'plants': current_row,
                'max_row_to_row_distance': max_row_to_row_distance,
                'total_width': row_width
            })
    
    return planting_map


def get_plant_details(plant_id, database):
    """Get detailed information about a plant."""
    plant = get_plant_by_id(plant_id, database)
    if not plant:
        return None
    
    # Get companion and avoid plant names
    good_companions = [get_plant_by_id(cid, database)['name'] 
                       for cid in plant.get('companions', []) 
                       if get_plant_by_id(cid, database)]
    bad_companions = [get_plant_by_id(aid, database)['name'] 
                      for aid in plant.get('avoid_plants', []) 
                      if get_plant_by_id(aid, database)]
    
    return {
        'id': plant['id'],
        'name': plant['name'],
        'type': plant['type'],
        'spacing': plant['spacing'],
        'good_companions': good_companions,
        'bad_companions': bad_companions,
        'companion_info': plant.get('companion_info', ''),
        'needs_fleece_cover': plant.get('needs_fleece_cover', False),
        'fleece_info': plant.get('fleece_info', '')
    }