"""All card content for Green Energy City."""

from game.card import Card, Choice

# The very first card shown as an intro
INTRO_CARD = Card(
    card_id=0,
    character="Mayor",
    text=(
        "Welcome, City Manager!\n\n"
        "Our city is at a crossroads. We need a green energy future.\n"
        "Your decisions will shape our destiny."
    ),
    left_choice=Choice("I'm not ready", {"happiness": -5}),
    right_choice=Choice("I'll do my best!", {"happiness": 5}),
)

CARDS = [
    Card(
        card_id=1,
        character="Solar Engineer",
        text=(
            "We can install solar panels on all public rooftops. "
            "It's a big upfront cost, but energy returns are excellent."
        ),
        left_choice=Choice("Too expensive", {"economy": 10, "energy": -10, "environment": -5}),
        right_choice=Choice("Install them!", {"economy": -20, "energy": 20, "environment": 10}),
    ),
    Card(
        card_id=2,
        character="Wind Energy Director",
        text=(
            "There's a perfect location for a wind farm outside the city. "
            "Some residents near the site are concerned about noise."
        ),
        left_choice=Choice("Reject it", {"energy": -10, "happiness": 5}),
        right_choice=Choice("Build it!", {"energy": 25, "environment": 10, "happiness": -10}),
    ),
    Card(
        card_id=3,
        character="Transport Minister",
        text=(
            "We propose offering discounts on electric vehicle purchases "
            "to help citizens switch to clean transport faster."
        ),
        left_choice=Choice("No discounts", {"economy": 10, "environment": -10}),
        right_choice=Choice("Give discounts", {"economy": -15, "environment": 15, "happiness": 10}),
    ),
    Card(
        card_id=4,
        character="Coal Plant Manager",
        text=(
            "The old coal plant is still profitable. "
            "Should we shut it down early and transition to renewables?"
        ),
        left_choice=Choice("Keep it running", {"economy": 15, "energy": 10, "environment": -20}),
        right_choice=Choice("Shut it down", {"economy": -10, "energy": -15, "environment": 20}),
    ),
    Card(
        card_id=5,
        character="City Planner",
        text=(
            "New buildings should meet strict green standards. "
            "Construction costs will rise, but energy efficiency improves."
        ),
        left_choice=Choice("Reject standards", {"economy": 10, "environment": -10}),
        right_choice=Choice("Implement them", {"economy": -10, "environment": 15, "happiness": 5}),
    ),
    Card(
        card_id=6,
        character="Cycling Advocate",
        text=(
            "Adding dedicated cycling lanes throughout the city "
            "means reducing car lanes on main roads."
        ),
        left_choice=Choice("Cars stay", {"happiness": -5, "environment": -5}),
        right_choice=Choice("Build bike lanes", {"environment": 10, "happiness": 5, "economy": -5}),
    ),
    Card(
        card_id=7,
        character="Bus Company CEO",
        text=(
            "We can replace the entire diesel bus fleet with electric buses. "
            "Significant government funding is required."
        ),
        left_choice=Choice("Can't afford it", {"environment": -10, "economy": 10}),
        right_choice=Choice("Fund the switch", {"environment": 15, "energy": -10, "economy": -15, "happiness": 10}),
    ),
    Card(
        card_id=8,
        character="Energy Storage Startup",
        text=(
            "Our battery storage technology can stabilize the renewable energy grid. "
            "It's cutting-edge but still unproven at city scale."
        ),
        left_choice=Choice("Too risky", {"energy": -5}),
        right_choice=Choice("Invest!", {"energy": 15, "economy": -20, "environment": 5}),
    ),
    Card(
        card_id=9,
        character="Forestry Department",
        text=(
            "We can plant 10,000 trees across the city. "
            "The land is currently used for surface parking."
        ),
        left_choice=Choice("Keep parking", {"happiness": 5, "environment": -10}),
        right_choice=Choice("Plant trees!", {"environment": 20, "happiness": 5}),
    ),
    Card(
        card_id=10,
        character="Recycling Initiative",
        text=(
            "Making recycling mandatory for all residents would significantly "
            "cut landfill waste. Some people will push back."
        ),
        left_choice=Choice("Keep voluntary", {"environment": -5, "happiness": 5}),
        right_choice=Choice("Make mandatory", {"environment": 10, "happiness": -10}),
    ),
    Card(
        card_id=11,
        character="Nuclear Lobbyist",
        text=(
            "A small nuclear power plant would provide reliable clean energy "
            "for 50 years. Very controversial among residents."
        ),
        left_choice=Choice("Absolutely not", {"energy": -10, "happiness": 10}),
        right_choice=Choice("Approve it", {"energy": 30, "environment": 5, "happiness": -20}),
    ),
    Card(
        card_id=12,
        character="Smart Grid Engineer",
        text=(
            "A smart grid system would optimize energy distribution and "
            "cut waste by 20%. Installation takes time and money."
        ),
        left_choice=Choice("Old system works", {"energy": -10}),
        right_choice=Choice("Build smart grid", {"energy": 15, "economy": -15, "environment": 10}),
    ),
    Card(
        card_id=13,
        character="Hydropower Expert",
        text=(
            "The city river could power a small hydro plant. "
            "But construction would affect the local river ecosystem."
        ),
        left_choice=Choice("Protect the river", {"environment": 10, "energy": -10}),
        right_choice=Choice("Build the plant", {"energy": 20, "environment": -15}),
    ),
    Card(
        card_id=14,
        character="Green Jobs Initiative",
        text=(
            "A city-funded program to train residents for renewable energy jobs "
            "would reduce unemployment and upskill workers."
        ),
        left_choice=Choice("Cut the program", {"economy": 10, "happiness": -10}),
        right_choice=Choice("Fund it", {"economy": -10, "happiness": 15, "energy": 5}),
    ),
    Card(
        card_id=15,
        character="Carbon Tax Advisor",
        text=(
            "Implementing a carbon tax on businesses would fund green projects "
            "but increase costs for local industry."
        ),
        left_choice=Choice("No carbon tax", {"economy": 10, "environment": -15}),
        right_choice=Choice("Implement it", {"economy": -10, "environment": 20, "energy": 5}),
    ),
    Card(
        card_id=16,
        character="Green Roof Architect",
        text=(
            "Mandating green roofs on all new commercial buildings "
            "would improve insulation and urban biodiversity."
        ),
        left_choice=Choice("Too costly", {"economy": 5, "environment": -5}),
        right_choice=Choice("Make it law", {"economy": -10, "environment": 15, "happiness": 5}),
    ),
    Card(
        card_id=17,
        character="Residents Support Group",
        text=(
            "Low-income residents can't afford their green energy bills. "
            "Should the city help cover part of their costs?"
        ),
        left_choice=Choice("They'll manage", {"happiness": -15, "economy": 5}),
        right_choice=Choice("Help them", {"happiness": 20, "economy": -15}),
    ),
    Card(
        card_id=18,
        character="Tech Industry Rep",
        text=(
            "A large data center wants to locate here. "
            "It brings jobs and revenue but has enormous power consumption."
        ),
        left_choice=Choice("Decline", {"economy": -10, "energy": 5}),
        right_choice=Choice("Welcome them", {"economy": 20, "energy": -15, "environment": -10}),
    ),
    Card(
        card_id=19,
        character="Geothermal Specialist",
        text=(
            "Underground heat could supply renewable heating for the entire city. "
            "The drilling project is expensive but long-lasting."
        ),
        left_choice=Choice("Skip it", {"energy": -5}),
        right_choice=Choice("Start drilling", {"energy": 15, "economy": -20, "environment": 10}),
    ),
    Card(
        card_id=20,
        character="Urban Farmer",
        text=(
            "Converting abandoned lots into community gardens and urban farms "
            "would boost food security and community wellbeing."
        ),
        left_choice=Choice("Leave them empty", {"happiness": -5, "environment": -5}),
        right_choice=Choice("Start farming!", {"happiness": 15, "environment": 10, "economy": -5}),
    ),
    Card(
        card_id=21,
        character="Emergency Manager",
        text=(
            "Our power grid is vulnerable to extreme weather. "
            "Hardening the infrastructure now is costly but reduces risk."
        ),
        left_choice=Choice("Take the risk", {"economy": 10, "energy": -10}),
        right_choice=Choice("Harden the grid", {"economy": -15, "energy": 10}),
    ),
    Card(
        card_id=22,
        character="Environmental Scientist",
        text=(
            "Air quality in the city is worsening. "
            "Stricter industrial emission limits would help but increase costs."
        ),
        left_choice=Choice("Current limits fine", {"environment": -15, "economy": 10}),
        right_choice=Choice("Tighten limits", {"environment": 20, "economy": -10, "happiness": 5}),
    ),
    Card(
        card_id=23,
        character="Tourism Board",
        text=(
            "Our green credentials could attract eco-tourists from around the world. "
            "Should we invest in a green tourism marketing campaign?"
        ),
        left_choice=Choice("Save the money", {"economy": 5, "happiness": -5}),
        right_choice=Choice("Market it!", {"economy": 15, "happiness": 10, "environment": -5}),
    ),
    Card(
        card_id=24,
        character="School Principal",
        text=(
            "Adding renewable energy and sustainability to the school curriculum "
            "will educate the next generation of green citizens."
        ),
        left_choice=Choice("Not a priority", {"happiness": -5}),
        right_choice=Choice("Teach it!", {"happiness": 10, "economy": -5, "environment": 5}),
    ),
    Card(
        card_id=25,
        character="Waste-to-Energy Company",
        text=(
            "We can convert city waste into electricity. "
            "It's not fully clean energy, but reduces landfill significantly."
        ),
        left_choice=Choice("Reject it", {"energy": -5, "economy": -5}),
        right_choice=Choice("Build the plant", {"energy": 15, "economy": 5, "environment": -10}),
    ),
    Card(
        card_id=26,
        character="Water Authority",
        text=(
            "Installing water recycling systems in all public buildings "
            "would cut water consumption by 30%."
        ),
        left_choice=Choice("Too expensive", {"environment": -10, "economy": 5}),
        right_choice=Choice("Install them", {"environment": 15, "economy": -10, "happiness": 5}),
    ),
    Card(
        card_id=27,
        character="Local Newspaper",
        text=(
            "Citizens are concerned about rising energy bills from the green transition. "
            "Will you hold a public town hall to address them?"
        ),
        left_choice=Choice("Ignore it", {"happiness": -15}),
        right_choice=Choice("Hold town hall", {"happiness": 15, "economy": -5}),
    ),
    Card(
        card_id=28,
        character="Startup Incubator",
        text=(
            "A cleantech startup hub could attract innovative green companies "
            "and create skilled jobs. It needs initial city funding."
        ),
        left_choice=Choice("Not now", {"economy": 5, "energy": -5}),
        right_choice=Choice("Fund the hub", {"economy": -15, "energy": 10, "happiness": 10}),
    ),
    Card(
        card_id=29,
        character="Grid Operator",
        text=(
            "During peak demand we must import non-green electricity. "
            "Alternatively, we can enforce demand reduction."
        ),
        left_choice=Choice("Import energy", {"energy": 15, "economy": -10, "environment": -10}),
        right_choice=Choice("Reduce demand", {"energy": -5, "happiness": -10, "environment": 10}),
    ),
    Card(
        card_id=30,
        character="Green Party Leader",
        text=(
            "Citizens want an accelerated green transition. "
            "Move faster — even if it's more costly in the short term?"
        ),
        left_choice=Choice("Steady pace", {"happiness": -5}),
        right_choice=Choice("Go faster!", {"economy": -15, "environment": 20, "energy": 10, "happiness": 10}),
    ),
    # Conditional cards — only appear when a specific stat is under pressure
    Card(
        card_id=31,
        character="Energy Crisis Advisor",
        text=(
            "Power cuts are becoming frequent. "
            "We need an emergency plan to fix the grid right away."
        ),
        left_choice=Choice("Ride it out", {"energy": -10, "happiness": -10}),
        right_choice=Choice("Emergency plan", {"energy": 20, "economy": -20}),
        conditions={"energy": (0, 35)},
    ),
    Card(
        card_id=32,
        character="Finance Minister",
        text=(
            "The city is almost out of money. "
            "Should we take an emergency loan for green energy projects?"
        ),
        left_choice=Choice("Refuse the loan", {"economy": -15, "energy": -5}),
        right_choice=Choice("Accept the loan", {"economy": 25, "environment": 10}),
        conditions={"economy": (0, 30)},
    ),
    Card(
        card_id=33,
        character="Happiness Counsellor",
        text=(
            "Citizen morale is at an all-time low. "
            "A city festival celebrating green achievements might help."
        ),
        left_choice=Choice("Cancel it", {"happiness": -10}),
        right_choice=Choice("Host the festival", {"happiness": 20, "economy": -10, "environment": 5}),
        conditions={"happiness": (0, 30)},
    ),
    Card(
        card_id=34,
        character="Environmental Alert",
        text=(
            "A major pollution incident is threatening the city. "
            "Immediate cleanup action is expensive but vital."
        ),
        left_choice=Choice("Delay cleanup", {"environment": -15, "happiness": -10}),
        right_choice=Choice("Act immediately", {"environment": 20, "economy": -20}),
        conditions={"environment": (0, 25)},
    ),
]
