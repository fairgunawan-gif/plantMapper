"""
Plant database for the Plant Mapper application.
Contains two databases: cursor database and GartenZauber database.
Also handles custom plants stored in a JSON file.
"""

import json
import os

CUSTOM_PLANTS_FILE = "custom_plants.json"
NEXT_CUSTOM_ID_START = 1000

# Cursor Database - Main plant database
PLANTS_CURSOR = [
    {
        'id': 1,
        'name': 'Broccoli',
        'type': 'Vegetable',
        'companions': [8, 9, 10, 15, 17, 18],
        'avoid_plants': [19, 21, 22, 23],
        'companion_info': "Benefits from: Onions, Garlic (repel pests), Celery (nutrient help), Marigolds (pest control), Leeks, Lettuce (ground cover). Avoid: Tomatoes, Squash, Pumpkin (nutrient competition)",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 60,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece for first 6-8 weeks to protect from pests and frost"
    },
    {
        'id': 2,
        'name': 'Cauliflower',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 18],
        'avoid_plants': [19, 21, 22, 23],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (repel pests), Lettuce. Avoid: Tomatoes, Squash, Pumpkin (compete for nutrients)",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 60,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece for first 6-8 weeks to protect from pests and cold weather"
    },
    {
        'id': 8,
        'name': 'Onions',
        'type': 'Vegetable',
        'companions': [1, 2, 13, 18],
        'avoid_plants': [16],
        'companion_info': "Good with: Brassicas (broccoli, cauliflower), Lettuce, Cucumber. Avoid: Potatoes. Helps repel many garden pests",
        'spacing': {
            'plant_to_plant': 10,
            'row_to_row': 30,
            'depth': 2.5,
            'height': 45,
            'spread': 10
        },
        'needs_fleece_cover': False
    },
    {
        'id': 9,
        'name': 'Garlic',
        'type': 'Vegetable',
        'companions': [1, 2, 13, 19],
        'avoid_plants': [16],
        'companion_info': "Good with: Brassicas, Tomatoes, Cucumber. Avoid: Potatoes. Excellent pest deterrent",
        'spacing': {
            'plant_to_plant': 10,
            'row_to_row': 30,
            'depth': 5,
            'height': 45,
            'spread': 10
        },
        'needs_fleece_cover': False
    },
    {
        'id': 10,
        'name': 'Celery',
        'type': 'Vegetable',
        'companions': [1, 18, 19],
        'avoid_plants': [],
        'companion_info': "Good with: Brassicas, Lettuce, Tomatoes. Helps improve soil and neighbor plant growth",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 60,
            'depth': 0.6,
            'height': 30,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 12,
        'name': 'Fennel',
        'type': 'Vegetable',
        'companions': [],
        'avoid_plants': [1, 2, 13, 19],
        'companion_info': "Generally not a good companion plant - keep separate from most vegetables",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 60,
            'depth': 0.6,
            'height': 120,
            'spread': 60
        },
        'needs_fleece_cover': False
    },
    {
        'id': 13,
        'name': 'Cucumber',
        'type': 'Vegetable',
        'companions': [12, 9, 36, 34, 27, 17, 10, 8],
        'avoid_plants': [28, 19, 20],
        'companion_info': "Benefits from: Fennel, Garlic, White and Red Cabbage, Butterhead Lettuce, Leek, Celery, Onion. Avoid: Turnip, Tomato, and Zucchini.",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 120,
            'depth': 2.5,
            'height': 180,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants until established to protect from cold and pests"
    },
    {
        'id': 14,
        'name': 'Eggplant',
        'type': 'Vegetable',
        'companions': [15, 19],
        'avoid_plants': [13],
        'companion_info': "Good with: Marigolds (pest control), Tomatoes. Avoid: Cucumbers",
        'spacing': {
            'plant_to_plant': 60,
            'row_to_row': 90,
            'depth': 0.6,
            'height': 90,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from cold and flea beetles"
    },
    {
        'id': 15,
        'name': 'Marigolds',
        'type': 'Vegetable',
        'companions': [1, 2, 11, 13, 14, 19],
        'avoid_plants': [],
        'companion_info': "Excellent companion for most plants - repels pests and nematodes",
        'spacing': {
            'plant_to_plant': 20,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 30,
            'spread': 20
        },
        'needs_fleece_cover': False
    },
    {
        'id': 16,
        'name': 'Potato',
        'type': 'Vegetable',
        'companions': [1, 2, 25, 26],
        'avoid_plants': [14, 34, 36, 10, 19, 8],
        'companion_info': "Benefits from: Broccoli, Cauliflower, Blue Kohlrabi, White Kohlrabi. Avoid: Eggplants, Red Cabbage, White Cabbage, Celery, Tomato, and Onion.",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 90,
            'depth': 10,
            'height': 60,
            'spread': 60
        },
        'needs_fleece_cover': False
    },
    {
        'id': 17,
        'name': 'Leek',
        'type': 'Vegetable',
        'companions': [1, 2, 13],
        'avoid_plants': [16],
        'companion_info': "Good with: Brassicas, Cucumber. Avoid: Potatoes. Helps repel pests",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 30,
            'depth': 15,
            'height': 60,
            'spread': 15
        },
        'needs_fleece_cover': False
    },
    {
        'id': 18,
        'name': 'Lettuce',
        'type': 'Vegetable',
        'companions': [1, 2, 8, 10, 13],
        'avoid_plants': [],
        'companion_info': "Good companion for many plants - works well as ground cover and shallow roots don't compete",
        'spacing': {
            'plant_to_plant': 20,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 20,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 19,
        'name': 'Tomatoes',
        'type': 'Vegetable',
        'companions': [9, 10, 14, 15],
        'avoid_plants': [1, 2, 11, 16],
        'companion_info': "Good with: Garlic, Celery, Eggplant, Marigolds. Avoid: Brassicas, Potatoes (disease risk)",
        'spacing': {
            'plant_to_plant': 60,
            'row_to_row': 120,
            'depth': 0.6,
            'height': 180,
            'spread': 60
        },
        'needs_fleece_cover': False
    },
    {
        'id': 20,
        'name': 'Zucchini',
        'type': 'Vegetable',
        'companions': [11, 16],
        'avoid_plants': [],
        'companion_info': "Good with: Potatoes. Can be planted near most vegetables",
        'spacing': {
            'plant_to_plant': 90,
            'row_to_row': 120,
            'depth': 2.5,
            'height': 60,
            'spread': 120
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from cold and pests until flowering begins"
    },
    {
        'id': 21,
        'name': 'Pumpkin',
        'type': 'Vegetable',
        'companions': [15],
        'avoid_plants': [1, 2],
        'companion_info': "Good with: Marigolds (pest control). Avoid: Brassicas (heavy feeder, competes for nutrients)",
        'spacing': {
            'plant_to_plant': 120,
            'row_to_row': 180,
            'depth': 2.5,
            'height': 30,
            'spread': 360
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants until established and weather is consistently warm"
    },
    {
        'id': 22,
        'name': 'Squash',
        'type': 'Vegetable',
        'companions': [15],
        'avoid_plants': [1, 2],
        'companion_info': "Good with: Marigolds (pest control). Avoid: Brassicas (heavy feeder, competes for nutrients)",
        'spacing': {
            'plant_to_plant': 90,
            'row_to_row': 150,
            'depth': 2.5,
            'height': 60,
            'spread': 180
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants until established and weather is consistently warm"
    },
    {
        'id': 23,
        'name': 'Kale',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce (ground cover). Avoid: Fennel (inhibits growth)",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 60,
            'spread': 45
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece for first 6-8 weeks to protect from cabbage white butterflies and pigeons"
    },
    {
        'id': 24,
        'name': 'Celeriac',
        'type': 'Vegetable',
        'companions': [1, 2, 18, 15],
        'avoid_plants': [12],
        'companion_info': "Good with: Brassicas (improves growth), Lettuce, Marigolds (pest control). Avoid: Fennel (inhibits growth)",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 45,
            'depth': 0.6,
            'height': 60,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 25,
        'name': 'Kohlrabi (Blue)',
        'type': 'Vegetable',
        'companions': [16, 27, 10, 19],
        'avoid_plants': [12, 36, 34],
        'companion_info': "Benefits from: Potato, Butterhead Lettuce, Celery, Tomato. Avoid: Fennel, White Cabbage, and Red Cabbage.",
        'spacing': {
            'plant_to_plant': 25,
            'row_to_row': 30,
            'depth': 1.3,
            'height': 30,
            'spread': 25
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from flea beetles and cabbage root fly"
    },
    {
        'id': 26,
        'name': 'Kohlrabi (White)',
        'type': 'Vegetable',
        'companions': [16, 27, 10, 19],
        'avoid_plants': [12, 36, 34],
        'companion_info': "Benefits from: Potato, Butterhead Lettuce, Celery, Tomato. Avoid: Fennel, White Cabbage, and Red Cabbage.",
        'spacing': {
            'plant_to_plant': 25,
            'row_to_row': 30,
            'depth': 1.3,
            'height': 30,
            'spread': 25
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from flea beetles and cabbage root fly"
    },
    {
        'id': 27,
        'name': 'Butterhead Lettuce',
        'type': 'Vegetable',
        'companions': [1, 2, 8, 9, 10],
        'avoid_plants': [],
        'companion_info': "Good companion for most plants. Works well with Brassicas, Onions, Garlic, and Celery. Shallow roots don't compete for nutrients",
        'spacing': {
            'plant_to_plant': 25,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 20,
            'spread': 25
        },
        'needs_fleece_cover': False
    },
    {
        'id': 28,
        'name': 'Turnip (May Turnip)',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 18],
        'avoid_plants': [12],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Lettuce. Avoid: Fennel",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 30,
            'depth': 1.3,
            'height': 30,
            'spread': 15
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from flea beetles"
    },
    {
        'id': 29,
        'name': 'Swiss Chard (Rainbow)',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 18],
        'avoid_plants': [12],
        'companion_info': "Good with: Onions, Garlic (pest control), Marigolds (pest deterrent), Lettuce. Avoid: Fennel",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 45,
            'depth': 2.5,
            'height': 60,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 30,
        'name': 'Pak Choi (Mini)',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12, 19],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce. Avoid: Fennel, Tomatoes",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 30,
            'depth': 1.3,
            'height': 20,
            'spread': 15
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from flea beetles and cabbage root fly"
    },
    {
        'id': 31,
        'name': 'Parsley',
        'type': 'Herb',
        'companions': [1, 2, 19, 15],
        'avoid_plants': [12],
        'companion_info': "Good with: Brassicas (improves growth and flavor), Tomatoes, Marigolds. Avoid: Fennel",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 30,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 32,
        'name': 'Romanesco',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12, 19],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce. Avoid: Fennel, Tomatoes",
        'spacing': {
            'plant_to_plant': 60,
            'row_to_row': 75,
            'depth': 1.3,
            'height': 60,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece for first 6-8 weeks to protect from cabbage white butterflies"
    },
    {
        'id': 33,
        'name': 'Brussels Sprouts',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12, 19],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce. Avoid: Fennel, Tomatoes",
        'spacing': {
            'plant_to_plant': 60,
            'row_to_row': 75,
            'depth': 1.3,
            'height': 90,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from cabbage white butterflies and pigeons"
    },
    {
        'id': 34,
        'name': 'Red Cabbage',
        'type': 'Vegetable',
        'companions': [14, 13, 27, 17, 29, 28, 10, 19],
        'avoid_plants': [2, 1, 16, 9, 25, 26, 8],
        'companion_info': "Benefits from: Eggplants, Cucumber, Butterhead Lettuce, Leek, Swiss Chard, Turnip, Celery, Tomatoes. Avoid: Cauliflower, Broccoli, Potato, Garlic, both Kohlrabi varieties, and Onion.",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 45,
            'spread': 45
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from cabbage white butterflies and pigeons"
    },
    {
        'id': 35,
        'name': 'Lollo Rossa Lettuce',
        'type': 'Vegetable',
        'companions': [1, 2, 8, 9, 10],
        'avoid_plants': [],
        'companion_info': "Good companion for most plants. Works well with Brassicas, Onions, Garlic, and Celery. Shallow roots don't compete for nutrients",
        'spacing': {
            'plant_to_plant': 25,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 20,
            'spread': 25
        },
        'needs_fleece_cover': False
    },
    {
        'id': 36,
        'name': 'White Cabbage',
        'type': 'Vegetable',
        'companions': [14, 13, 27, 17, 29, 28, 10, 19],
        'avoid_plants': [2, 1, 16, 9, 25, 26, 8],
        'companion_info': "Benefits from: Eggplants, Cucumber, Butterhead Lettuce, Leek, Swiss Chard, Turnip, Celery, Tomatoes. Avoid: Cauliflower, Broccoli, Potato, Garlic, both Kohlrabi varieties, and Onion.",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 45,
            'spread': 45
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from cabbage white butterflies and pigeons"
    },
    {
        'id': 37,
        'name': 'Savoy Cabbage',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12, 19],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce. Avoid: Fennel, Tomatoes",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 45,
            'spread': 45
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from cabbage white butterflies and pigeons"
    }
]

# GartenZauber Database - Alternative plant database
PLANTS_GARTENZAUBER = [
    {
        'id': 1,
        'name': 'Broccoli',
        'type': 'Vegetable',
        'companions': [14, 16, 10],
        'avoid_plants': [34, 36, 8],
        'companion_info': "Benefits from: Eggplants, Potatoes, Celery. Avoid: Red Cabbage, White Cabbage, and Onions.",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 60,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece for first 6-8 weeks to protect from pests and frost"
    },
    {
        'id': 2,
        'name': 'Cauliflower',
        'type': 'Vegetable',
        'companions': [14, 16, 10],
        'avoid_plants': [34, 36, 8],
        'companion_info': "Benefits from: Eggplants, Potatoes, Celery. Avoid: Red Cabbage, White Cabbage, and Onions.",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 60,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece for first 6-8 weeks to protect from pests and cold weather"
    },
    {
        'id': 8,
        'name': 'Onions',
        'type': 'Vegetable',
        'companions': [1, 2, 13, 18],
        'avoid_plants': [16],
        'companion_info': "Good with: Brassicas (broccoli, cauliflower), Lettuce, Cucumber. Avoid: Potatoes. Helps repel many garden pests",
        'spacing': {
            'plant_to_plant': 10,
            'row_to_row': 30,
            'depth': 2.5,
            'height': 45,
            'spread': 10
        },
        'needs_fleece_cover': False
    },
    {
        'id': 9,
        'name': 'Garlic',
        'type': 'Vegetable',
        'companions': [1, 2, 13, 19],
        'avoid_plants': [16],
        'companion_info': "Good with: Brassicas, Tomatoes, Cucumber. Avoid: Potatoes. Excellent pest deterrent",
        'spacing': {
            'plant_to_plant': 10,
            'row_to_row': 30,
            'depth': 5,
            'height': 45,
            'spread': 10
        },
        'needs_fleece_cover': False
    },
    {
        'id': 10,
        'name': 'Celery',
        'type': 'Vegetable',
        'companions': [1, 18, 19],
        'avoid_plants': [],
        'companion_info': "Good with: Brassicas, Lettuce, Tomatoes. Helps improve soil and neighbor plant growth",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 60,
            'depth': 0.6,
            'height': 30,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 12,
        'name': 'Fennel',
        'type': 'Vegetable',
        'companions': [],
        'avoid_plants': [1, 2, 13, 19],
        'companion_info': "Generally not a good companion plant - keep separate from most vegetables",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 60,
            'depth': 0.6,
            'height': 120,
            'spread': 60
        },
        'needs_fleece_cover': False
    },
    {
        'id': 13,
        'name': 'Cucumber',
        'type': 'Vegetable',
        'companions': [12, 9, 36, 34, 27, 17, 10, 8],
        'avoid_plants': [28, 19, 20],
        'companion_info': "Benefits from: Fennel, Garlic, White and Red Cabbage, Butterhead Lettuce, Leek, Celery, Onion. Avoid: Turnip, Tomato, and Zucchini.",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 120,
            'depth': 2.5,
            'height': 180,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants until established to protect from cold and pests"
    },
    {
        'id': 14,
        'name': 'Eggplant',
        'type': 'Vegetable',
        'companions': [15, 19],
        'avoid_plants': [13],
        'companion_info': "Good with: Marigolds (pest control), Tomatoes. Avoid: Cucumbers",
        'spacing': {
            'plant_to_plant': 60,
            'row_to_row': 90,
            'depth': 0.6,
            'height': 90,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from cold and flea beetles"
    },
    {
        'id': 15,
        'name': 'Marigolds',
        'type': 'Vegetable',
        'companions': [1, 2, 11, 13, 14, 19],
        'avoid_plants': [],
        'companion_info': "Excellent companion for most plants - repels pests and nematodes",
        'spacing': {
            'plant_to_plant': 20,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 30,
            'spread': 20
        },
        'needs_fleece_cover': False
    },
    {
        'id': 16,
        'name': 'Potato',
        'type': 'Vegetable',
        'companions': [1, 2, 25, 26],
        'avoid_plants': [14, 34, 36, 10, 19, 8],
        'companion_info': "Benefits from: Broccoli, Cauliflower, Blue Kohlrabi, White Kohlrabi. Avoid: Eggplants, Red Cabbage, White Cabbage, Celery, Tomato, and Onion.",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 90,
            'depth': 10,
            'height': 60,
            'spread': 60
        },
        'needs_fleece_cover': False
    },
    {
        'id': 17,
        'name': 'Leek',
        'type': 'Vegetable',
        'companions': [1, 2, 13],
        'avoid_plants': [16],
        'companion_info': "Good with: Brassicas, Cucumber. Avoid: Potatoes. Helps repel pests",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 30,
            'depth': 15,
            'height': 60,
            'spread': 15
        },
        'needs_fleece_cover': False
    },
    {
        'id': 18,
        'name': 'Lettuce',
        'type': 'Vegetable',
        'companions': [1, 2, 8, 10, 13],
        'avoid_plants': [],
        'companion_info': "Good companion for many plants - works well as ground cover and shallow roots don't compete",
        'spacing': {
            'plant_to_plant': 20,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 20,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 19,
        'name': 'Tomatoes',
        'type': 'Vegetable',
        'companions': [9, 10, 14, 15],
        'avoid_plants': [1, 2, 11, 16],
        'companion_info': "Good with: Garlic, Celery, Eggplant, Marigolds. Avoid: Brassicas, Potatoes (disease risk)",
        'spacing': {
            'plant_to_plant': 60,
            'row_to_row': 120,
            'depth': 0.6,
            'height': 180,
            'spread': 60
        },
        'needs_fleece_cover': False
    },
    {
        'id': 20,
        'name': 'Zucchini',
        'type': 'Vegetable',
        'companions': [11, 16],
        'avoid_plants': [],
        'companion_info': "Good with: Potatoes. Can be planted near most vegetables",
        'spacing': {
            'plant_to_plant': 90,
            'row_to_row': 120,
            'depth': 2.5,
            'height': 60,
            'spread': 120
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from cold and pests until flowering begins"
    },
    {
        'id': 21,
        'name': 'Pumpkin',
        'type': 'Vegetable',
        'companions': [15],
        'avoid_plants': [1, 2],
        'companion_info': "Good with: Marigolds (pest control). Avoid: Brassicas (heavy feeder, competes for nutrients)",
        'spacing': {
            'plant_to_plant': 120,
            'row_to_row': 180,
            'depth': 2.5,
            'height': 30,
            'spread': 360
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants until established and weather is consistently warm"
    },
    {
        'id': 22,
        'name': 'Squash',
        'type': 'Vegetable',
        'companions': [15],
        'avoid_plants': [1, 2],
        'companion_info': "Good with: Marigolds (pest control). Avoid: Brassicas (heavy feeder, competes for nutrients)",
        'spacing': {
            'plant_to_plant': 90,
            'row_to_row': 150,
            'depth': 2.5,
            'height': 60,
            'spread': 180
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants until established and weather is consistently warm"
    },
    {
        'id': 23,
        'name': 'Kale',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce (ground cover). Avoid: Fennel (inhibits growth)",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 60,
            'spread': 45
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece for first 6-8 weeks to protect from cabbage white butterflies and pigeons"
    },
    {
        'id': 24,
        'name': 'Celeriac',
        'type': 'Vegetable',
        'companions': [1, 2, 18, 15],
        'avoid_plants': [12],
        'companion_info': "Good with: Brassicas (improves growth), Lettuce, Marigolds (pest control). Avoid: Fennel (inhibits growth)",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 45,
            'depth': 0.6,
            'height': 60,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 25,
        'name': 'Kohlrabi (Blue)',
        'type': 'Vegetable',
        'companions': [16, 27, 10, 19],
        'avoid_plants': [12, 36, 34],
        'companion_info': "Benefits from: Potato, Butterhead Lettuce, Celery, Tomato. Avoid: Fennel, White Cabbage, and Red Cabbage.",
        'spacing': {
            'plant_to_plant': 25,
            'row_to_row': 30,
            'depth': 1.3,
            'height': 30,
            'spread': 25
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from flea beetles and cabbage root fly"
    },
    {
        'id': 26,
        'name': 'Kohlrabi (White)',
        'type': 'Vegetable',
        'companions': [16, 27, 10, 19],
        'avoid_plants': [12, 36, 34],
        'companion_info': "Benefits from: Potato, Butterhead Lettuce, Celery, Tomato. Avoid: Fennel, White Cabbage, and Red Cabbage.",
        'spacing': {
            'plant_to_plant': 25,
            'row_to_row': 30,
            'depth': 1.3,
            'height': 30,
            'spread': 25
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from flea beetles and cabbage root fly"
    },
    {
        'id': 27,
        'name': 'Butterhead Lettuce',
        'type': 'Vegetable',
        'companions': [1, 2, 8, 9, 10],
        'avoid_plants': [],
        'companion_info': "Good companion for most plants. Works well with Brassicas, Onions, Garlic, and Celery. Shallow roots don't compete for nutrients",
        'spacing': {
            'plant_to_plant': 25,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 20,
            'spread': 25
        },
        'needs_fleece_cover': False
    },
    {
        'id': 28,
        'name': 'Turnip (May Turnip)',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 18],
        'avoid_plants': [12],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Lettuce. Avoid: Fennel",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 30,
            'depth': 1.3,
            'height': 30,
            'spread': 15
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover young plants to protect from flea beetles"
    },
    {
        'id': 29,
        'name': 'Swiss Chard (Rainbow)',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 18],
        'avoid_plants': [12],
        'companion_info': "Good with: Onions, Garlic (pest control), Marigolds (pest deterrent), Lettuce. Avoid: Fennel",
        'spacing': {
            'plant_to_plant': 30,
            'row_to_row': 45,
            'depth': 2.5,
            'height': 60,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 30,
        'name': 'Pak Choi (Mini)',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12, 19],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce. Avoid: Fennel, Tomatoes",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 30,
            'depth': 1.3,
            'height': 20,
            'spread': 15
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from flea beetles and cabbage root fly"
    },
    {
        'id': 31,
        'name': 'Parsley',
        'type': 'Herb',
        'companions': [1, 2, 19, 15],
        'avoid_plants': [12],
        'companion_info': "Good with: Brassicas (improves growth and flavor), Tomatoes, Marigolds. Avoid: Fennel",
        'spacing': {
            'plant_to_plant': 15,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 30,
            'spread': 30
        },
        'needs_fleece_cover': False
    },
    {
        'id': 32,
        'name': 'Romanesco',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12, 19],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce. Avoid: Fennel, Tomatoes",
        'spacing': {
            'plant_to_plant': 60,
            'row_to_row': 75,
            'depth': 1.3,
            'height': 60,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece for first 6-8 weeks to protect from cabbage white butterflies"
    },
    {
        'id': 33,
        'name': 'Brussels Sprouts',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12, 19],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce. Avoid: Fennel, Tomatoes",
        'spacing': {
            'plant_to_plant': 60,
            'row_to_row': 75,
            'depth': 1.3,
            'height': 90,
            'spread': 60
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from cabbage white butterflies and pigeons"
    },
    {
        'id': 34,
        'name': 'Red Cabbage',
        'type': 'Vegetable',
        'companions': [14, 13, 27, 17, 29, 28, 10, 19],
        'avoid_plants': [2, 1, 16, 9, 25, 26, 8],
        'companion_info': "Benefits from: Eggplants, Cucumber, Butterhead Lettuce, Leek, Swiss Chard, Turnip, Celery, Tomatoes. Avoid: Cauliflower, Broccoli, Potato, Garlic, both Kohlrabi varieties, and Onion.",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 45,
            'spread': 45
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from cabbage white butterflies and pigeons"
    },
    {
        'id': 35,
        'name': 'Lollo Rossa Lettuce',
        'type': 'Vegetable',
        'companions': [1, 2, 8, 9, 10],
        'avoid_plants': [],
        'companion_info': "Good companion for most plants. Works well with Brassicas, Onions, Garlic, and Celery. Shallow roots don't compete for nutrients",
        'spacing': {
            'plant_to_plant': 25,
            'row_to_row': 30,
            'depth': 0.6,
            'height': 20,
            'spread': 25
        },
        'needs_fleece_cover': False
    },
    {
        'id': 36,
        'name': 'White Cabbage',
        'type': 'Vegetable',
        'companions': [14, 13, 27, 17, 29, 28, 10, 19],
        'avoid_plants': [2, 1, 16, 9, 25, 26, 8],
        'companion_info': "Benefits from: Eggplants, Cucumber, Butterhead Lettuce, Leek, Swiss Chard, Turnip, Celery, Tomatoes. Avoid: Cauliflower, Broccoli, Potato, Garlic, both Kohlrabi varieties, and Onion.",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 45,
            'spread': 45
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from cabbage white butterflies and pigeons"
    },
    {
        'id': 37,
        'name': 'Savoy Cabbage',
        'type': 'Vegetable',
        'companions': [8, 9, 15, 17, 18],
        'avoid_plants': [12, 19],
        'companion_info': "Benefits from: Onions, Garlic (pest control), Marigolds (pest deterrent), Leeks, Lettuce. Avoid: Fennel, Tomatoes",
        'spacing': {
            'plant_to_plant': 45,
            'row_to_row': 60,
            'depth': 1.3,
            'height': 45,
            'spread': 45
        },
        'needs_fleece_cover': True,
        'fleece_info': "Cover with fleece to protect from cabbage white butterflies and pigeons"
    }
]

# Default plant selections with quantities
DEFAULT_PLANT_SELECTIONS = [
    {'id': 2, 'count': 3},   # Cauliflower
    {'id': 1, 'count': 6},   # Broccoli
    {'id': 12, 'count': 3},  # Fennel
    {'id': 23, 'count': 3},  # Kale
    {'id': 16, 'count': 12}, # Potato
    {'id': 24, 'count': 3},  # Celeriac
    {'id': 25, 'count': 3},  # Kohlrabi (Blue)
    {'id': 26, 'count': 6},  # Kohlrabi (White)
    {'id': 27, 'count': 3},  # Butterhead Lettuce
    {'id': 17, 'count': 8},  # Leek
    {'id': 28, 'count': 6},  # Turnip (May turnip)
    {'id': 29, 'count': 3},  # Swiss Chard (Rainbow)
    {'id': 30, 'count': 3},  # Pak Choi (Mini)
    {'id': 31, 'count': 3},  # Parsley
    {'id': 32, 'count': 3},  # Romanesco
    {'id': 33, 'count': 3},  # Brussels Sprouts
    {'id': 34, 'count': 3},  # Red Cabbage
    {'id': 35, 'count': 3},  # Lollo Rossa Lettuce
    {'id': 36, 'count': 3},  # White Cabbage
    {'id': 37, 'count': 3},  # Savoy Cabbage
    {'id': 8, 'count': 3}    # Onion
]


def get_plant_by_id(plant_id, database):
    """Get a plant by its ID from the specified database."""
    for plant in database:
        if plant['id'] == plant_id:
            return plant
    return None


def get_plant_name(plant_id, database):
    """Get the name of a plant by its ID."""
    plant = get_plant_by_id(plant_id, database)
    return plant['name'] if plant else 'Unknown'


def get_plant_companion_info(plant_id, database):
    """Get companion planting information for a plant."""
    plant = get_plant_by_id(plant_id, database)
    return plant['companion_info'] if plant else ''


# ============================================================
# Custom Plant Management Functions
# ============================================================

def load_custom_plants():
    """Load custom plants from JSON file."""
    if os.path.exists(CUSTOM_PLANTS_FILE):
        try:
            with open(CUSTOM_PLANTS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_custom_plants(custom_plants):
    """Save custom plants to JSON file."""
    with open(CUSTOM_PLANTS_FILE, 'w') as f:
        json.dump(custom_plants, f, indent=2)


def get_next_custom_id():
    """Get the next available custom plant ID."""
    custom_plants = load_custom_plants()
    if not custom_plants:
        return NEXT_CUSTOM_ID_START
    
    max_id = max(p['id'] for p in custom_plants)
    return max(NEXT_CUSTOM_ID_START, max_id + 1)


def add_custom_plant(plant_data):
    """
    Add a new custom plant.
    plant_data should contain: name, type, companions, avoid_plants, companion_info,
    spacing (with plant_to_plant, row_to_row, depth, height, spread),
    needs_fleece_cover, fleece_info (optional)
    Returns the new plant ID.
    """
    custom_plants = load_custom_plants()
    new_id = get_next_custom_id()
    
    new_plant = {
        'id': new_id,
        'name': plant_data['name'],
        'type': plant_data.get('type', 'Vegetable'),
        'companions': plant_data.get('companions', []),
        'avoid_plants': plant_data.get('avoid_plants', []),
        'companion_info': plant_data.get('companion_info', ''),
        'spacing': {
            'plant_to_plant': plant_data.get('plant_to_plant', 30),
            'row_to_row': plant_data.get('row_to_row', 45),
            'depth': plant_data.get('depth', 1.0),
            'height': plant_data.get('height', 30),
            'spread': plant_data.get('spread', 30)
        },
        'needs_fleece_cover': plant_data.get('needs_fleece_cover', False),
        'fleece_info': plant_data.get('fleece_info', ''),
        'is_custom': True
    }
    
    custom_plants.append(new_plant)
    save_custom_plants(custom_plants)
    return new_id


def update_custom_plant(plant_id, plant_data):
    """
    Update an existing custom plant.
    Returns True if successful, False if plant not found.
    """
    custom_plants = load_custom_plants()
    for i, plant in enumerate(custom_plants):
        if plant['id'] == plant_id:
            custom_plants[i].update(plant_data)
            custom_plants[i]['id'] = plant_id  # Ensure ID doesn't change
            save_custom_plants(custom_plants)
            return True
    return False


def delete_custom_plant(plant_id):
    """
    Delete a custom plant.
    Returns True if successful, False if plant not found.
    """
    custom_plants = load_custom_plants()
    original_len = len(custom_plants)
    custom_plants = [p for p in custom_plants if p['id'] != plant_id]
    
    if len(custom_plants) < original_len:
        save_custom_plants(custom_plants)
        return True
    return False


def get_custom_plant(plant_id):
    """Get a specific custom plant by ID."""
    custom_plants = load_custom_plants()
    for plant in custom_plants:
        if plant['id'] == plant_id:
            return plant
    return None


def get_merged_database(base_database):
    """
    Merge the base database with custom plants.
    Custom plants override base plants with the same ID.
    Returns the merged database.
    """
    merged = [plant.copy() for plant in base_database]
    merged_dict = {plant['id']: plant for plant in merged}
    
    custom_plants = load_custom_plants()
    for custom_plant in custom_plants:
        merged_dict[custom_plant['id']] = custom_plant.copy()
    
    return list(merged_dict.values())


def get_all_plants_with_custom(base_database):
    """
    Get all plants including custom ones, sorted by name.
    """
    merged = get_merged_database(base_database)
    return sorted(merged, key=lambda p: p['name'].lower())


def is_custom_plant(plant_id):
    """Check if a plant is a custom plant."""
    return plant_id >= NEXT_CUSTOM_ID_START


def create_plant_override(base_plant_id, base_database, modifications):
    """
    Create a custom override for an existing base plant.
    This allows editing base plant attributes.
    Returns the new custom plant ID.
    """
    base_plant = get_plant_by_id(base_plant_id, base_database)
    if not base_plant:
        return None
    
    # Create a copy with modifications
    override_data = base_plant.copy()
    override_data['spacing'] = base_plant['spacing'].copy()
    override_data['is_override'] = True
    override_data['original_id'] = base_plant_id
    
    # Apply modifications
    for key, value in modifications.items():
        if key == 'spacing':
            override_data['spacing'].update(value)
        else:
            override_data[key] = value
    
    # Remove base-specific keys that shouldn't be in override
    override_data.pop('id', None)
    
    return add_custom_plant(override_data)
