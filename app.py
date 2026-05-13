"""
Plant Mapper - Streamlit Application
A companion planting tool for planning vegetable garden layouts.
"""

import math
import streamlit as st
import textwrap
from plants_data import (
    PLANTS_CURSOR, PLANTS_GARTENZAUBER, DEFAULT_PLANT_SELECTIONS,
    get_plant_by_id, get_plant_companion_info,
    load_custom_plants, save_custom_plants, get_next_custom_id,
    add_custom_plant, update_custom_plant, delete_custom_plant,
    get_merged_database, get_all_plants_with_custom, is_custom_plant,
    get_custom_plant, create_plant_override
)
from planting_algorithm import generate_planting_map, get_plant_details

# Page configuration
st.set_page_config(
    page_title="Plant Mapper",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .plant-placement {
        padding: 10px;
        margin: 5px 0;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 4px;
        text-align: center;
    }
    .plant-placement.needs-fleece {
        background-color: #90EE90 !important;
    }
    .plant-placement.group-start {
        border-radius: 4px 4px 0 0;
    }
    .plant-placement.group-end {
        border-radius: 0 0 4px 4px;
    }
    .plant-placement.group-middle {
        border-radius: 0;
    }
    .plant-name {
        font-weight: bold;
        color: #2c3e50;
    }
    .distance-value {
        font-size: 0.85em;
        color: #666;
        margin-top: 4px;
    }
    .column-total {
        margin-top: 10px;
        padding: 8px;
        background-color: #f0f0f0;
        border-radius: 4px;
        text-align: center;
        font-size: 0.9em;
        color: #666;
        border-top: 3px solid #4CAF50;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 5px 0;
    }
    .legend-sample {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        background-color: #90EE90;
    }
    .planting-map-wrapper {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
    }
    .planting-map-summary {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        width: 100%;
        max-width: 1000px;
        padding: 0 10px;
    }
    .planting-map-summary div {
        background-color: #f8faf8;
        border: 1px solid #e9f0ea;
        border-radius: 12px;
        padding: 10px 14px;
        font-size: 0.95rem;
        color: #2f5f43;
    }
    .plot-square {
        width: 100%;
        max-width: 1000px;
        aspect-ratio: 1 / 1;
        border: 2px solid #4CAF50;
        border-radius: 18px;
        background: #ffffff;
        padding: 14px;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
        position: relative;
        overflow: hidden;
        min-height: 400px;
        max-height: 80vh;
    }
    .plot-square::before {
        content: attr(data-width);
        position: absolute;
        top: 12px;
        left: 14px;
        color: #4CAF50;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .plot-square::after {
        content: attr(data-length);
        position: absolute;
        bottom: 12px;
        right: 14px;
        color: #4CAF50;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .plot-inner {
        width: 100%;
        height: 100%;
        display: grid;
        gap: 10px;
        align-items: start;
        justify-items: stretch;
        overflow: hidden;
    }
    .planting-column {
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: linear-gradient(180deg, #fbfdf9 0%, #f3f8f1 100%);
        border: 1px solid #dfe9dd;
        border-radius: 14px;
        padding: 10px;
        min-width: 0;
        overflow: hidden;
    }
    .column-path {
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(76, 175, 80, 0.08);
        border: 1px dashed #4CAF50;
        border-radius: 14px;
        color: #4F7F53;
        font-size: 0.85rem;
        padding: 8px;
        min-height: 100px;
    }
    .planting-column-header {
        font-weight: 700;
        color: #2c5d39;
        text-align: center;
        line-height: 1.2;
        margin-bottom: 4px;
    }
    .planting-column-header small {
        display: block;
        margin-top: 4px;
        font-size: 0.85rem;
        color: #4f7f53;
        font-weight: 500;
    }
    .plot-square .plant-placement {
        padding: 6px 6px;
        margin: 0;
    }
    .plot-square .plant-name {
        font-weight: bold;
        color: #2c3e50;
        font-size: 0.75em;
    }
    .plot-square .distance-value {
        font-size: 0.65em;
        color: #666;
        margin-top: 4px;
    }
    .column-total {
        margin-top: auto;
        padding: 8px;
        background-color: #f0f0f0;
        border-radius: 4px;
        text-align: center;
        font-size: 0.9em;
        color: #666;
        border-top: 3px solid #4CAF50;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 5px 0;
    }
    .legend-sample {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        background-color: #90EE90;
    }
    .description-box {
        background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #4CAF50;
    }
    .plant-item-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        margin: 4px 0;
        background-color: #f8f9fa;
        border-radius: 4px;
        border: 1px solid #e9ecef;
    }
    .plant-item-row.selected {
        background-color: #e3f2fd;
        border-color: #2196f3;
    }
    .quantity-controls {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .quantity-btn {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        border: 1px solid #ddd;
        background-color: white;
        cursor: pointer;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .quantity-btn:hover {
        background-color: #f0f0f0;
    }
    .quantity-display {
        min-width: 30px;
        text-align: center;
        font-weight: bold;
    }
    .custom-badge {
        font-size: 0.7em;
        background-color: #ff9800;
        color: white;
        padding: 2px 6px;
        border-radius: 10px;
        margin-left: 8px;
    }
    .override-badge {
        font-size: 0.7em;
        background-color: #9c27b0;
        color: white;
        padding: 2px 6px;
        border-radius: 10px;
        margin-left: 8px;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'plant_quantities' not in st.session_state:
        st.session_state.plant_quantities = {}
    if 'database_selected' not in st.session_state:
        st.session_state.database_selected = 'gartenzauber'
    if 'map_generated' not in st.session_state:
        st.session_state.map_generated = False
    if 'planting_map' not in st.session_state:
        st.session_state.planting_map = []
    if 'editing_plant' not in st.session_state:
        st.session_state.editing_plant = None


def load_default_selections():
    """Load default plant selections into session state."""
    st.session_state.plant_quantities = {}
    for selection in DEFAULT_PLANT_SELECTIONS:
        st.session_state.plant_quantities[selection['id']] = selection['count']


def prepopulate_all_plants():
    """Add one of each plant from the database."""
    database = get_current_database()
    for plant in database:
        if plant['id'] not in st.session_state.plant_quantities:
            st.session_state.plant_quantities[plant['id']] = 1


def get_current_database():
    """Get the currently selected plant database with custom plants merged."""
    base_db = PLANTS_CURSOR if st.session_state.database_selected == 'cursor' else PLANTS_GARTENZAUBER
    return get_merged_database(base_db)


def get_selected_plants_list():
    """Get a flat list of selected plant IDs based on quantities."""
    selected = []
    for plant_id, count in st.session_state.plant_quantities.items():
        selected.extend([plant_id] * count)
    return selected


def update_plant_quantity(plant_id, delta):
    """Update the quantity of a plant."""
    current = st.session_state.plant_quantities.get(plant_id, 0)
    new_count = current + delta
    if new_count <= 0:
        if plant_id in st.session_state.plant_quantities:
            del st.session_state.plant_quantities[plant_id]
    else:
        st.session_state.plant_quantities[plant_id] = new_count
    st.session_state.map_generated = False


def render_sidebar():
    """Render the sidebar with controls."""
    with st.sidebar:
        st.title("🌱 Plant Mapper")
        
        # Description
        st.markdown("""
        <div class="description-box">
            <b>New to Gardening?</b><br>
            Starting out in gardening with a dedicated plot of land is an exciting 
            opportunity to grow your own vegetables. This page supports your journey 
            into Mischkultur (companion planting) by helping you plan which vegetables 
            grow best together.
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Plot dimensions
        st.subheader("📏 Plot Dimensions")
        col1, col2 = st.columns(2)
        with col1:
            plot_length = st.number_input(
                "Length (m)",
                min_value=0.1,
                max_value=100.0,
                value=6.0,
                step=0.1,
                key="plot_length"
            )
        with col2:
            plot_width = st.number_input(
                "Width (m)",
                min_value=0.1,
                max_value=100.0,
                value=8.0,
                step=0.1,
                key="plot_width"
            )
        
        plot_area = plot_length * plot_width
        st.metric("Total Area", f"{plot_area:.1f} m²")
        
        st.divider()
        
        # Database selection
        st.subheader("🗄️ Database")
        database_option = st.radio(
            "Select Database:",
            options=["cursor", "gartenzauber"],
            format_func=lambda x: "Cursor Database" if x == "cursor" else "GartenZauber",
            index=1 if st.session_state.database_selected == "gartenzauber" else 0,
            key="database_radio"
        )
        st.session_state.database_selected = database_option
        
        st.divider()
        
        # Algorithm options
        st.subheader("⚙️ Algorithm Options")
        
        group_same = st.checkbox(
            "Group Same Plants",
            value=True,
            key="group_same"
        )
        
        if group_same:
            max_group_size = st.number_input(
                "Max plants per group",
                min_value=1,
                max_value=10,
                value=3,
                key="max_group_size"
            )
        else:
            max_group_size = 1
        
        mix_culture = st.checkbox(
            "Mix Culture Algorithm",
            value=False,
            key="mix_culture"
        )
        
        group_fleece = st.checkbox(
            "Group Fleece Plants",
            value=False,
            key="group_fleece"
        )
        
        st.divider()
        
        # Actions
        st.subheader("🎯 Actions")
        
        if st.button("🌿 Load Default Selection", use_container_width=True):
            load_default_selections()
            st.session_state.map_generated = False
            st.rerun()
        
        if st.button("🌍 Pre-populate All Plants", use_container_width=True):
            prepopulate_all_plants()
            st.session_state.map_generated = False
            st.rerun()
        
        if st.button("🗑️ Clear Selections", use_container_width=True):
            st.session_state.plant_quantities = {}
            st.session_state.map_generated = False
            st.rerun()
        
        generate_btn = st.button(
            "🗺️ Generate Planting Map",
            type="primary",
            use_container_width=True
        )
        
        if generate_btn:
            selected_plants = get_selected_plants_list()
            if len(selected_plants) == 0:
                st.error("Please select some plants first!")
            else:
                with st.spinner("Generating planting map..."):
                    database = get_current_database()
                    planting_map = generate_planting_map(
                        selected_plants,
                        plot_length,
                        plot_width,
                        database,
                        group_same_plants=group_same,
                        mix_culture=mix_culture,
                        group_fleece=group_fleece,
                        max_group_size=max_group_size
                    )
                    st.session_state.planting_map = planting_map
                    st.session_state.map_generated = True
                st.success("Planting map generated!")
        
        return plot_length, plot_width


def render_plant_selector():
    """Render the plant selector interface with quantity controls."""
    database = get_current_database()
    
    st.subheader("🌱 Available Plants")
    
    # Search box
    search_query = st.text_input("Search plants...", key="plant_search", placeholder="Type to search...")
    
    # Filter and sort plants
    sorted_plants = sorted(database, key=lambda p: p['name'].lower())
    if search_query:
        sorted_plants = [p for p in sorted_plants if search_query.lower() in p['name'].lower()]
    
    # Show total count
    total_plants = sum(st.session_state.plant_quantities.values())
    st.caption(f"Selected: {total_plants} plants ({len(st.session_state.plant_quantities)} types)")
    
    # Display plants with quantity controls
    for plant in sorted_plants:
        plant_id = plant['id']
        current_count = st.session_state.plant_quantities.get(plant_id, 0)
        
        # Determine badges
        badges = ""
        if is_custom_plant(plant_id):
            custom_plant = get_custom_plant(plant_id)
            if custom_plant and custom_plant.get('is_override'):
                badges += '<span class="override-badge" title="Custom override">Edited</span>'
            else:
                badges += '<span class="custom-badge" title="Custom plant">Custom</span>'
        
        col1, col2, col3 = st.columns([3, 1, 2])
        
        with col1:
            plant_label = f"{plant['name']} ({plant['type']}){badges}"
            st.markdown(f"<div class='plant-item-row {'selected' if current_count > 0 else ''}'>{plant_label}</div>", 
                       unsafe_allow_html=True)
        
        with col2:
            # Quantity controls
            col_minus, col_count, col_plus = st.columns([1, 1, 1])
            with col_minus:
                if st.button("−", key=f"minus_{plant_id}", disabled=current_count <= 0):
                    update_plant_quantity(plant_id, -1)
                    st.rerun()
            with col_count:
                st.markdown(f"<div class='quantity-display'>{current_count}</div>", unsafe_allow_html=True)
            with col_plus:
                if st.button("+", key=f"plus_{plant_id}"):
                    update_plant_quantity(plant_id, 1)
                    st.rerun()
        
        with col3:
            # Edit button
            if st.button("✏️", key=f"edit_{plant_id}", help="Edit plant"):
                st.session_state.editing_plant = plant_id
                st.rerun()
    
    # Show selected plants summary
    if st.session_state.plant_quantities:
        st.divider()
        st.subheader("✅ Selected Plants Summary")
        for plant_id, count in sorted(st.session_state.plant_quantities.items(), 
                                       key=lambda x: get_plant_by_id(x[0], database)['name'].lower() if get_plant_by_id(x[0], database) else ''):
            plant = get_plant_by_id(plant_id, database)
            if plant:
                st.write(f"- **{plant['name']}**: {count} plant{'s' if count > 1 else ''}")


def render_plant_editor():
    """Render the plant editor modal."""
    st.subheader("✏️ Plant Editor")
    
    if st.session_state.editing_plant is None:
        st.info("Select a plant to edit by clicking the ✏️ button next to it.")
        return
    
    database = get_current_database()
    plant_id = st.session_state.editing_plant
    plant = get_plant_by_id(plant_id, database)
    
    if not plant:
        st.error("Plant not found!")
        return
    
    is_custom = is_custom_plant(plant_id)
    is_override = plant.get('is_override', False)
    
    with st.form("plant_editor_form"):
        st.write(f"### Editing: {plant['name']}")
        
        if is_override:
            st.warning("This is a custom override of a base plant.")
        elif is_custom:
            st.info("This is a custom plant.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=plant['name'], key="edit_name")
            plant_type = st.selectbox("Type", 
                                      options=["Vegetable", "Herb", "Flower", "Fruit", "Other"],
                                      index=["Vegetable", "Herb", "Flower", "Fruit", "Other"].index(plant.get('type', 'Vegetable')),
                                      key="edit_type")
            companion_info = st.text_area("Companion Info", value=plant.get('companion_info', ''), key="edit_companion_info")
        
        with col2:
            # Spacing requirements
            st.write("**Spacing Requirements (cm)**")
            plant_to_plant = st.number_input("Plant to Plant", min_value=1.0, max_value=500.0, 
                                             value=float(plant['spacing']['plant_to_plant']), key="edit_ptp")
            row_to_row = st.number_input("Row to Row", min_value=1.0, max_value=500.0,
                                         value=float(plant['spacing']['row_to_row']), key="edit_rtr")
            depth = st.number_input("Planting Depth", min_value=0.1, max_value=50.0, step=0.1,
                                    value=float(plant['spacing']['depth']), key="edit_depth")
            height = st.number_input("Mature Height", min_value=1.0, max_value=500.0,
                                     value=float(plant['spacing']['height']), key="edit_height")
            spread = st.number_input("Mature Spread", min_value=1.0, max_value=500.0,
                                     value=float(plant['spacing']['spread']), key="edit_spread")
        
        # Companion and avoid plants
        all_plant_options = {p['id']: p['name'] for p in database if p['id'] != plant_id}
        
        col3, col4 = st.columns(2)
        with col3:
            companions = st.multiselect(
                "Good Companions",
                options=list(all_plant_options.keys()),
                format_func=lambda x: all_plant_options[x],
                default=plant.get('companions', []),
                key="edit_companions"
            )
        with col4:
            avoid_plants = st.multiselect(
                "Plants to Avoid",
                options=list(all_plant_options.keys()),
                format_func=lambda x: all_plant_options[x],
                default=plant.get('avoid_plants', []),
                key="edit_avoid"
            )
        
        # Fleece options
        needs_fleece = st.checkbox("Needs Fleece Cover", value=plant.get('needs_fleece_cover', False), key="edit_fleece")
        fleece_info = st.text_area("Fleece Info", value=plant.get('fleece_info', ''), key="edit_fleece_info") if needs_fleece else ""
        
        submitted = st.form_submit_button("💾 Save Changes")
    
    if submitted:
        plant_data = {
            'name': name,
            'type': plant_type,
            'companion_info': companion_info,
            'plant_to_plant': plant_to_plant,
            'row_to_row': row_to_row,
            'depth': depth,
            'height': height,
            'spread': spread,
            'companions': companions,
            'avoid_plants': avoid_plants,
            'needs_fleece_cover': needs_fleece,
            'fleece_info': fleece_info
        }
        
        if is_custom:
            # Update existing custom plant
            if update_custom_plant(plant_id, plant_data):
                st.success("Plant updated successfully!")
            else:
                st.error("Failed to update plant.")
        else:
            # Create override for base plant
            new_id = create_plant_override(plant_id, 
                PLANTS_CURSOR if st.session_state.database_selected == 'cursor' else PLANTS_GARTENZAUBER,
                plant_data)
            if new_id:
                st.success(f"Created custom override for {name}!")
            else:
                st.error("Failed to create override.")
        
        st.session_state.editing_plant = None
        st.session_state.map_generated = False
        st.rerun()
    
    # Delete button (only for custom plants)
    if is_custom:
        st.divider()
        if st.button("🗑️ Delete Custom Plant", type="secondary"):
            if delete_custom_plant(plant_id):
                st.success("Custom plant deleted!")
                if plant_id in st.session_state.plant_quantities:
                    del st.session_state.plant_quantities[plant_id]
                st.session_state.editing_plant = None
                st.session_state.map_generated = False
                st.rerun()
            else:
                st.error("Failed to delete plant.")
    
    # Cancel button
    if st.button("Cancel"):
        st.session_state.editing_plant = None
        st.rerun()


def render_custom_plant_creator():
    """Render the custom plant creation form."""
    st.subheader("➕ Create New Custom Plant")
    
    with st.form("create_plant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Plant Name *", key="new_name")
            plant_type = st.selectbox("Type", 
                                      options=["Vegetable", "Herb", "Flower", "Fruit", "Other"],
                                      key="new_type")
            companion_info = st.text_area("Companion Info", key="new_companion_info")
        
        with col2:
            st.write("**Spacing Requirements (cm)**")
            plant_to_plant = st.number_input("Plant to Plant", min_value=1.0, max_value=500.0, value=30.0, key="new_ptp")
            row_to_row = st.number_input("Row to Row", min_value=1.0, max_value=500.0, value=45.0, key="new_rtr")
            depth = st.number_input("Planting Depth", min_value=0.1, max_value=50.0, step=0.1, value=1.0, key="new_depth")
            height = st.number_input("Mature Height", min_value=1.0, max_value=500.0, value=30.0, key="new_height")
            spread = st.number_input("Mature Spread", min_value=1.0, max_value=500.0, value=30.0, key="new_spread")
        
        # Companion and avoid plants
        database = get_current_database()
        all_plant_options = {p['id']: p['name'] for p in database}
        
        col3, col4 = st.columns(2)
        with col3:
            companions = st.multiselect(
                "Good Companions",
                options=list(all_plant_options.keys()),
                format_func=lambda x: all_plant_options[x],
                key="new_companions"
            )
        with col4:
            avoid_plants = st.multiselect(
                "Plants to Avoid",
                options=list(all_plant_options.keys()),
                format_func=lambda x: all_plant_options[x],
                key="new_avoid"
            )
        
        needs_fleece = st.checkbox("Needs Fleece Cover", key="new_fleece")
        fleece_info = st.text_area("Fleece Info", key="new_fleece_info") if needs_fleece else ""
        
        submitted = st.form_submit_button("➕ Create Custom Plant")
    
    if submitted:
        if not name:
            st.error("Plant name is required!")
        else:
            plant_data = {
                'name': name,
                'type': plant_type,
                'companion_info': companion_info,
                'plant_to_plant': plant_to_plant,
                'row_to_row': row_to_row,
                'depth': depth,
                'height': height,
                'spread': spread,
                'companions': companions,
                'avoid_plants': avoid_plants,
                'needs_fleece_cover': needs_fleece,
                'fleece_info': fleece_info
            }
            
            new_id = add_custom_plant(plant_data)
            st.success(f"Created custom plant '{name}' with ID {new_id}!")
            st.session_state.plant_quantities[new_id] = 1
            st.session_state.map_generated = False
            st.rerun()


def render_planting_map():
    """Render the generated planting map."""
    if not st.session_state.map_generated or not st.session_state.planting_map:
        st.info("Click 'Generate Planting Map' to create your garden layout")
        return
    
    planting_map = st.session_state.planting_map
    plot_length = st.session_state.get('plot_length', 6.0)
    plot_width = st.session_state.get('plot_width', 8.0)
    plot_area = plot_length * plot_width
    
    st.subheader("🗺️ Planting Map")
    
    # Legend
    with st.expander("📖 Legend", expanded=False):
        st.markdown("""
        <div class="legend-item">
            <div class="legend-sample"></div>
            <span>Plants needing fleece cover (light green background)</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="planting-map-summary">
        <div><strong>Plot Dimensions</strong><br>{plot_length:.1f} m × {plot_width:.1f} m</div>
        <div><strong>Total Area</strong><br>{plot_area:.1f} m²</div>
        <div><strong>Columns</strong><br>{len(planting_map)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    widths = []
    for column_data in planting_map:
        raw_width = column_data['max_row_to_row_distance']
        widths.append(max(1, round(raw_width / 10, 1)))
    
    grid_tracks = []
    for idx, width in enumerate(widths):
        grid_tracks.append(f"{width}fr")
        if idx < len(widths) - 1:
            grid_tracks.append("30px")
    
    grid_style = "grid-template-columns: " + " ".join(grid_tracks) + ";"
    
    html = textwrap.dedent(f"""
    <div class="planting-map-wrapper">
    <div class="plot-square" data-width="Width: {plot_width:.1f} m" data-length="Length: {plot_length:.1f} m">
    <div class="plot-inner" style="{grid_style}">
    """)
    
    for col_idx, column_data in enumerate(planting_map):
        max_spacing = column_data['max_row_to_row_distance']
        widest_plants = [p['plant']['name'] for p in column_data['plants'] if p['plant']['spacing']['row_to_row'] == max_spacing]
        widest_text = ", ".join(set(widest_plants))  # Remove duplicates
        
        html += textwrap.dedent(f"""
    <div class='planting-column'>
    <div class='planting-column-header'>Column {col_idx + 1}
    <small>Width: {max_spacing} cm ({widest_text})</small>
    </div>
    """)
        
        for plant_idx, placement in enumerate(column_data['plants']):
            plant = placement['plant']
            fleece_class = "needs-fleece" if plant['needs_fleece_cover'] else ""
            html += textwrap.dedent(f"""
    <div class='plant-placement {fleece_class}'>
    <div class='plant-name'>{plant['name']}</div>
    <div class='distance-value'>Spacing: {placement['distance']} cm</div>
    </div>
    """)
        
        total_plant_to_plant = sum(p['plant']['spacing']['plant_to_plant'] for p in column_data['plants'])
        html += textwrap.dedent(f"""
    <div class='column-total'>
    Sum of plant-to-plant: {total_plant_to_plant} cm
    </div>
    </div>
    """)
        
        if col_idx < len(planting_map) - 1:
            html += textwrap.dedent("""
    <div class='column-path'>30 cm walking path</div>
    """)
    
    html += textwrap.dedent("""
    </div>
    </div>
    </div>
    """)
    
    st.markdown(html, unsafe_allow_html=True)


def render_plant_details():
    """Render plant details for selected plants."""
    database = get_current_database()
    
    if not st.session_state.plant_quantities:
        st.info("No plants selected")
        return
    
    st.subheader("📋 Plant Details")
    
    for plant_id, count in sorted(st.session_state.plant_quantities.items(),
                                   key=lambda x: get_plant_by_id(x[0], database)['name'].lower() if get_plant_by_id(x[0], database) else ''):
        plant = get_plant_by_id(plant_id, database)
        if plant:
            details = get_plant_details(plant_id, database)
            
            with st.expander(f"🌿 {plant['name']} (×{count})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Growing Dimensions**")
                    st.write(f"- Planting Depth: {plant['spacing']['depth']} cm")
                    st.write(f"- Mature Height: {plant['spacing']['height']} cm")
                    st.write(f"- Mature Spread: {plant['spacing']['spread']} cm")
                
                with col2:
                    st.write("**Spacing Requirements**")
                    st.write(f"- Plant to Plant: {plant['spacing']['plant_to_plant']} cm")
                    st.write(f"- Row to Row: {plant['spacing']['row_to_row']} cm")
                
                st.write("**Companion Planting**")
                if details['good_companions']:
                    st.write(f"- ✅ Good companions: {', '.join(details['good_companions'])}")
                else:
                    st.write("- No specific good companions")
                
                if details['bad_companions']:
                    st.write(f"- ❌ Avoid: {', '.join(details['bad_companions'])}")
                else:
                    st.write("- No plants to avoid")
                
                if plant['needs_fleece_cover']:
                    st.warning(f"🧣 **Protection Needed:** {plant.get('fleece_info', 'Cover with fleece')}")


def main():
    """Main application function."""
    init_session_state()
    
    st.title("🌱 Plant Mapper")
    
    # Render sidebar
    plot_length, plot_width = render_sidebar()
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌱 Plant Selection",
        "🗺️ Planting Map", 
        "📋 Plant Details",
        "➕ Create Custom Plant",
        "✏️ Edit Plant"
    ])
    
    with tab1:
        render_plant_selector()
    
    with tab2:
        render_planting_map()
    
    with tab3:
        render_plant_details()
    
    with tab4:
        render_custom_plant_creator()
    
    with tab5:
        render_plant_editor()


if __name__ == "__main__":
    main()