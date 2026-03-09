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
    Card(
        card_id=35,
        character="Rain Collector",
        text=(
            "We can collect rainwater from city rooftops. It can be used for watering parks and flushing toilets."
        ),
        left_choice=Choice("Leave it", {"environment": -5}),
        right_choice=Choice("Collect it!", {"environment": 10, "economy": -5}),
    ),
    Card(
        card_id=36,
        character="Street Lighting Manager",
        text=(
            "Half our street lights use old bulbs. Switching to LED will cut energy use and costs."
        ),
        left_choice=Choice("Old bulbs are fine", {"energy": -5, "economy": -5}),
        right_choice=Choice("Switch to LED", {"energy": 10, "economy": 5}),
    ),
    Card(
        card_id=37,
        character="Park Ranger",
        text=(
            "City parks are getting crowded. We can expand green spaces by using unused city land."
        ),
        left_choice=Choice("Not needed", {"happiness": -5}),
        right_choice=Choice("Expand parks!", {"happiness": 15, "environment": 10, "economy": -10}),
    ),
    Card(
        card_id=38,
        character="Air Quality Monitor",
        text=(
            "Our sensors show bad air quality near the highway. We can add green barriers of bushes and trees."
        ),
        left_choice=Choice("Leave it", {"environment": -10, "happiness": -5}),
        right_choice=Choice("Plant barriers", {"environment": 15, "happiness": 5, "economy": -5}),
    ),
    Card(
        card_id=39,
        character="Heating Engineer",
        text=(
            "Many old buildings waste heat in winter. Upgrading insulation will lower energy bills for residents."
        ),
        left_choice=Choice("Too costly", {"energy": -10, "economy": -5}),
        right_choice=Choice("Upgrade insulation", {"energy": 15, "economy": -15, "happiness": 10}),
    ),
    Card(
        card_id=40,
        character="Market Vendor",
        text=(
            "Local farmers want to sell fresh food in the city centre. It could reduce food miles and support local business."
        ),
        left_choice=Choice("No new markets", {"economy": 5, "environment": -5}),
        right_choice=Choice("Open a market", {"economy": 10, "environment": 5, "happiness": 10}),
    ),
    Card(
        card_id=41,
        character="Beach Cleanup Lead",
        text=(
            "Our city riverbank is covered in litter. Organising a volunteer cleanup will improve the area."
        ),
        left_choice=Choice("Not a priority", {"environment": -10, "happiness": -5}),
        right_choice=Choice("Organise cleanup", {"environment": 15, "happiness": 10, "economy": -5}),
    ),
    Card(
        card_id=42,
        character="School Science Teacher",
        text=(
            "Students want to measure air and water quality in the city as a science project."
        ),
        left_choice=Choice("Stick to class", {"happiness": -5}),
        right_choice=Choice("Support the project", {"happiness": 10, "environment": 5, "economy": -5}),
    ),
    Card(
        card_id=43,
        character="Local Radio Host",
        text=(
            "A weekly radio show about green city news could raise public awareness and pride."
        ),
        left_choice=Choice("Not important", {"happiness": -5}),
        right_choice=Choice("Start the show", {"happiness": 10, "economy": -5}),
    ),
    Card(
        card_id=44,
        character="Sports Club Leader",
        text=(
            "The city stadium uses a lot of energy. Solar panels on the roof could power most of the building."
        ),
        left_choice=Choice("Too complex", {"energy": -5}),
        right_choice=Choice("Install solar panels", {"energy": 15, "economy": -10, "environment": 5}),
    ),
    Card(
        card_id=45,
        character="Waste Manager",
        text=(
            "We can separate food waste and turn it into fertiliser for city parks."
        ),
        left_choice=Choice("Not worth it", {"environment": -5}),
        right_choice=Choice("Start composting", {"environment": 15, "happiness": 5, "economy": -5}),
    ),
    Card(
        card_id=46,
        character="Bike Share Director",
        text=(
            "A bike-sharing scheme with docking stations can cut car traffic and offer cheap city travel."
        ),
        left_choice=Choice("Not needed", {"environment": -5, "happiness": -5}),
        right_choice=Choice("Launch bike share", {"environment": 10, "happiness": 15, "economy": -10}),
    ),
    Card(
        card_id=47,
        character="Hospital Manager",
        text=(
            "The city hospital runs on fossil fuel backup generators. Switching to solar backup will cut emissions."
        ),
        left_choice=Choice("Too risky", {"environment": -10}),
        right_choice=Choice("Switch to solar backup", {"environment": 15, "economy": -15}),
    ),
    Card(
        card_id=48,
        character="Community Centre Lead",
        text=(
            "A local community centre wants to become a zero-waste hub and teaching space for residents."
        ),
        left_choice=Choice("Not a city job", {"happiness": -5}),
        right_choice=Choice("Support it", {"happiness": 15, "economy": -5, "environment": 5}),
    ),
    Card(
        card_id=49,
        character="River Warden",
        text=(
            "Fish have returned to a cleaned river section. We can protect this zone as a nature reserve."
        ),
        left_choice=Choice("No restrictions", {"environment": -10}),
        right_choice=Choice("Create reserve", {"environment": 20, "happiness": 5}),
    ),
    Card(
        card_id=50,
        character="Taxi Driver Union",
        text=(
            "Electric taxis could replace old diesel cabs. The city can offer low-interest loans to drivers."
        ),
        left_choice=Choice("Let drivers decide", {"environment": -10}),
        right_choice=Choice("Offer loans", {"environment": 15, "economy": -10, "happiness": 5}),
    ),
    Card(
        card_id=51,
        character="Youth Council",
        text=(
            "Young people want a vote on which green projects the city funds next year."
        ),
        left_choice=Choice("Adults decide", {"happiness": -15}),
        right_choice=Choice("Give them a vote", {"happiness": 20, "economy": -5}),
    ),
    Card(
        card_id=52,
        character="Construction Worker",
        text=(
            "The new sports hall is being built. Should we use recycled steel and wood instead of new materials?"
        ),
        left_choice=Choice("Standard materials", {"economy": 5, "environment": -10}),
        right_choice=Choice("Use recycled materials", {"economy": -10, "environment": 15}),
    ),
    Card(
        card_id=53,
        character="Library Director",
        text=(
            "The city library wants to host free workshops on saving energy at home."
        ),
        left_choice=Choice("Not the library's job", {"happiness": -5}),
        right_choice=Choice("Host workshops", {"happiness": 10, "economy": -5, "environment": 5}),
    ),
    Card(
        card_id=54,
        character="Food Bank Organiser",
        text=(
            "Food banks are collecting surplus food from supermarkets to cut waste and feed those in need."
        ),
        left_choice=Choice("Not a city issue", {"happiness": -10, "environment": -5}),
        right_choice=Choice("City support", {"happiness": 15, "environment": 5, "economy": -5}),
    ),
    Card(
        card_id=55,
        character="Electric Scooter Company",
        text=(
            "A scooter rental company wants to launch in the city. It could reduce short car trips."
        ),
        left_choice=Choice("Reject them", {"environment": -5, "happiness": -5}),
        right_choice=Choice("Allow scooters", {"environment": 10, "happiness": 5, "economy": 5}),
    ),
    Card(
        card_id=56,
        character="Playground Designer",
        text=(
            "Old playgrounds can be replaced with eco-friendly ones made from natural and recycled materials."
        ),
        left_choice=Choice("Keep old ones", {"happiness": -5, "environment": -5}),
        right_choice=Choice("Build eco playgrounds", {"happiness": 15, "environment": 10, "economy": -10}),
    ),
    Card(
        card_id=57,
        character="City Architect",
        text=(
            "Our newest office block is very wasteful. We can redesign it to use natural light and better airflow."
        ),
        left_choice=Choice("Too expensive now", {"energy": -5, "environment": -5}),
        right_choice=Choice("Redesign it", {"energy": 10, "environment": 10, "economy": -15}),
    ),
    Card(
        card_id=58,
        character="Night Market Organiser",
        text=(
            "A monthly night market selling local and eco-friendly goods could bring people together."
        ),
        left_choice=Choice("Too much hassle", {"happiness": -5}),
        right_choice=Choice("Approve the market", {"happiness": 15, "economy": 5, "environment": 5}),
    ),
    Card(
        card_id=59,
        character="Bus Driver",
        text=(
            "City bus drivers suggest adding more bus routes to underserved areas to cut car trips."
        ),
        left_choice=Choice("Routes are enough", {"happiness": -10, "environment": -5}),
        right_choice=Choice("Add more routes", {"happiness": 15, "environment": 10, "economy": -10}),
    ),
    Card(
        card_id=60,
        character="Pollution Inspector",
        text=(
            "A factory is secretly dumping waste into the river. We can fine them and force a cleanup."
        ),
        left_choice=Choice("Wait for more proof", {"environment": -20}),
        right_choice=Choice("Fine them now", {"environment": 20, "economy": 5, "happiness": 10}),
    ),
    Card(
        card_id=61,
        character="Clothes Swap Event Lead",
        text=(
            "A clothes-swapping event would cut textile waste and save money for families."
        ),
        left_choice=Choice("Not a city event", {"environment": -5}),
        right_choice=Choice("Support it", {"environment": 10, "happiness": 10, "economy": -5}),
    ),
    Card(
        card_id=62,
        character="Pet Shelter Manager",
        text=(
            "The city shelter has solar panels on the waiting list. Approving them speeds the process."
        ),
        left_choice=Choice("Wait for normal queue", {"energy": -5}),
        right_choice=Choice("Fast-track approval", {"energy": 5, "happiness": 10, "environment": 5}),
    ),
    Card(
        card_id=63,
        character="Flood Expert",
        text=(
            "Flooding is a growing risk. Green drainage systems in roads and parks can absorb heavy rain."
        ),
        left_choice=Choice("Old drains are fine", {"environment": -10, "happiness": -5}),
        right_choice=Choice("Build green drainage", {"environment": 15, "happiness": 5, "economy": -10}),
    ),
    Card(
        card_id=64,
        character="Bakery Owner",
        text=(
            "Local bakeries want to switch to bio-gas ovens fuelled by food waste. They need a small city grant."
        ),
        left_choice=Choice("Not our concern", {"environment": -5, "economy": -5}),
        right_choice=Choice("Give grants", {"environment": 10, "economy": 5, "happiness": 5}),
    ),
    Card(
        card_id=65,
        character="Journalist",
        text=(
            "A newspaper article is covering the city's green progress. Sharing data openly will build trust."
        ),
        left_choice=Choice("Keep data private", {"happiness": -10}),
        right_choice=Choice("Share openly", {"happiness": 15, "economy": -5}),
    ),
    Card(
        card_id=66,
        character="Electricity Regulator",
        text=(
            "Time-of-use pricing lets residents pay less for energy used off-peak. We can roll it out city-wide."
        ),
        left_choice=Choice("Current pricing OK", {"energy": -5, "economy": -5}),
        right_choice=Choice("Roll it out", {"energy": 10, "economy": 10, "happiness": 5}),
    ),
    Card(
        card_id=67,
        character="Urban Planner",
        text=(
            "A new district is planned. Making it car-free from the start will be cheaper than retrofitting later."
        ),
        left_choice=Choice("Allow cars", {"environment": -10, "happiness": -5}),
        right_choice=Choice("Car-free zone", {"environment": 20, "happiness": 10, "economy": -5}),
    ),
    Card(
        card_id=68,
        character="Artist Collective",
        text=(
            "Local artists want to paint murals promoting green living on city walls."
        ),
        left_choice=Choice("No murals", {"happiness": -5}),
        right_choice=Choice("Yes to murals", {"happiness": 15, "environment": 5, "economy": -5}),
    ),
    Card(
        card_id=69,
        character="Senior Residents Group",
        text=(
            "Older residents want easy-to-read guides on how to save energy at home."
        ),
        left_choice=Choice("Not a priority", {"happiness": -5}),
        right_choice=Choice("Produce guides", {"happiness": 10, "economy": -5, "environment": 5}),
    ),
    Card(
        card_id=70,
        character="Data Science Team",
        text=(
            "Using city data to predict energy demand could help us balance the grid more efficiently."
        ),
        left_choice=Choice("Too complicated", {"energy": -5}),
        right_choice=Choice("Use the data", {"energy": 15, "economy": -10, "environment": 5}),
    ),
    Card(
        card_id=71,
        character="Carpooling App",
        text=(
            "A new app helps people share car rides to work. The city can promote it for free."
        ),
        left_choice=Choice("Let people find it", {"environment": -5, "happiness": -5}),
        right_choice=Choice("Promote it", {"environment": 10, "happiness": 5}),
    ),
    Card(
        card_id=72,
        character="City Council Member",
        text=(
            "A new law would require all new homes to have a solar panel and rainwater tank installed."
        ),
        left_choice=Choice("Too strict", {"economy": 5, "environment": -10}),
        right_choice=Choice("Pass the law", {"economy": -10, "environment": 20, "energy": 5}),
    ),
    Card(
        card_id=73,
        character="Drone Delivery Company",
        text=(
            "Electric delivery drones could cut transport pollution in the city centre."
        ),
        left_choice=Choice("Not ready yet", {"environment": -5, "economy": -5}),
        right_choice=Choice("Run a pilot", {"environment": 10, "economy": 5, "happiness": 5}),
    ),
    Card(
        card_id=74,
        character="School Canteen Manager",
        text=(
            "School canteens can switch to plant-based menus three days per week to cut food emissions."
        ),
        left_choice=Choice("Kids won't eat it", {"environment": -10, "happiness": -5}),
        right_choice=Choice("Try it out", {"environment": 15, "happiness": 5, "economy": -5}),
    ),
    Card(
        card_id=75,
        character="Building Inspector",
        text=(
            "Old city-owned buildings can be sold to developers who agree to meet green building rules."
        ),
        left_choice=Choice("Keep the buildings", {"economy": -5, "environment": -5}),
        right_choice=Choice("Sell with conditions", {"economy": 15, "environment": 10}),
    ),
    Card(
        card_id=76,
        character="City Treasurer",
        text=(
            "Green bonds — loans from investors for eco projects — could fund three new solar farms."
        ),
        left_choice=Choice("Too risky", {"energy": -10, "environment": -5}),
        right_choice=Choice("Issue green bonds", {"energy": 20, "environment": 10, "economy": -5}),
    ),
    Card(
        card_id=77,
        character="Community Leader",
        text=(
            "A neighbourhood wants to manage its own small wind turbines and share the profits locally."
        ),
        left_choice=Choice("City manages energy", {"happiness": -10}),
        right_choice=Choice("Allow it", {"happiness": 20, "energy": 5, "economy": 5}),
    ),
    Card(
        card_id=78,
        character="IT Manager",
        text=(
            "Making city meetings online instead of in person could cut business travel and save time."
        ),
        left_choice=Choice("Keep meetings in person", {"economy": -5, "environment": -5}),
        right_choice=Choice("Go online", {"economy": 5, "environment": 10, "happiness": 5}),
    ),
    Card(
        card_id=79,
        character="Forest Scout",
        text=(
            "Volunteers want to monitor forest health on city outskirts and report illegal dumping."
        ),
        left_choice=Choice("Not needed", {"environment": -10}),
        right_choice=Choice("Support volunteers", {"environment": 15, "happiness": 5, "economy": -5}),
    ),
    Card(
        card_id=80,
        character="Harbour Manager",
        text=(
            "The city harbour can switch from diesel ferries to electric boats powered by renewable energy."
        ),
        left_choice=Choice("Ferries work fine", {"environment": -10, "energy": -5}),
        right_choice=Choice("Switch ferries", {"environment": 20, "energy": -5, "economy": -15}),
    ),
    Card(
        card_id=81,
        character="Sports Coach",
        text=(
            "Schools want to add outdoor fitness areas powered by kinetic energy from equipment."
        ),
        left_choice=Choice("Too experimental", {"energy": -5, "happiness": -5}),
        right_choice=Choice("Build them", {"energy": 5, "happiness": 15, "economy": -10}),
    ),
    Card(
        card_id=82,
        character="Local Bank Manager",
        text=(
            "The city bank can offer low-rate green home loans to help families insulate their houses."
        ),
        left_choice=Choice("Not our role", {"economy": -5, "environment": -5}),
        right_choice=Choice("Launch scheme", {"economy": 10, "environment": 15, "happiness": 10}),
    ),
    Card(
        card_id=83,
        character="Digital Kiosk Designer",
        text=(
            "Interactive kiosks in the city centre can teach visitors about our green projects."
        ),
        left_choice=Choice("Skip kiosks", {"happiness": -5}),
        right_choice=Choice("Install kiosks", {"happiness": 10, "economy": -5, "environment": 5}),
    ),
    Card(
        card_id=84,
        character="Night-time Economy Advisor",
        text=(
            "Nightclubs and bars generate huge noise and light pollution. New rules can cut this."
        ),
        left_choice=Choice("No new rules", {"happiness": 5, "environment": -10}),
        right_choice=Choice("Introduce rules", {"happiness": -5, "environment": 15}),
    ),
    Card(
        card_id=85,
        character="Greenhouse Grower",
        text=(
            "A city greenhouse can grow fresh vegetables year-round using excess heat from factories."
        ),
        left_choice=Choice("Too niche", {"economy": -5}),
        right_choice=Choice("Build the greenhouse", {"economy": 10, "environment": 10, "happiness": 5}),
    ),
    Card(
        card_id=86,
        character="Disaster Relief Team",
        text=(
            "The city needs emergency power reserves in case of extreme weather events."
        ),
        left_choice=Choice("Current backup is fine", {"energy": -10}),
        right_choice=Choice("Build reserves", {"energy": 15, "economy": -15, "happiness": 5}),
    ),
    Card(
        card_id=87,
        character="Tech School Principal",
        text=(
            "A free coding course on smart city technology could train 500 young people this year."
        ),
        left_choice=Choice("No room in budget", {"economy": -5, "happiness": -5}),
        right_choice=Choice("Fund the course", {"economy": -10, "happiness": 20, "energy": 5}),
    ),
    Card(
        card_id=88,
        character="Green Taxi Fleet",
        text=(
            "Ten electric taxis will join the city fleet. We can add charging spots at taxi ranks."
        ),
        left_choice=Choice("Drivers choose their cars", {"environment": -10}),
        right_choice=Choice("Add charging spots", {"environment": 15, "economy": -5, "happiness": 5}),
    ),
    Card(
        card_id=89,
        character="Urban Biologist",
        text=(
            "An urban wildlife corridor connecting parks can help birds and insects move across the city."
        ),
        left_choice=Choice("Not practical", {"environment": -10}),
        right_choice=Choice("Build the corridor", {"environment": 20, "happiness": 5, "economy": -10}),
    ),
    Card(
        card_id=90,
        character="Rooftop Farm Group",
        text=(
            "Three office buildings want to convert their flat rooftops into vegetable gardens."
        ),
        left_choice=Choice("Too risky structurally", {"environment": -5}),
        right_choice=Choice("Approve them", {"environment": 15, "happiness": 10, "economy": -5}),
    ),
    Card(
        card_id=91,
        character="Parking Authority",
        text=(
            "Converting two large car parks into mixed-use green spaces would reduce traffic and add parks."
        ),
        left_choice=Choice("Keep the car parks", {"economy": 5, "environment": -10}),
        right_choice=Choice("Convert them", {"economy": -10, "environment": 20, "happiness": 10}),
    ),
    Card(
        card_id=92,
        character="Heat Network Engineer",
        text=(
            "Underground pipes carrying waste heat from factories can warm homes in winter."
        ),
        left_choice=Choice("Too expensive", {"energy": -10, "economy": -5}),
        right_choice=Choice("Build the network", {"energy": 20, "economy": -20, "environment": 10}),
    ),
    Card(
        card_id=93,
        character="City Marathon Organiser",
        text=(
            "The annual marathon can become zero-waste by banning single-use cups and plastics."
        ),
        left_choice=Choice("Runners need cups", {"environment": -10}),
        right_choice=Choice("Go zero-waste", {"environment": 15, "happiness": 5, "economy": -5}),
    ),
    Card(
        card_id=94,
        character="Child Safety Officer",
        text=(
            "Safe walking routes to school can replace many car school runs if paths are well-lit and clear."
        ),
        left_choice=Choice("Roads are safe", {"environment": -10, "happiness": -5}),
        right_choice=Choice("Upgrade walkways", {"environment": 15, "happiness": 10, "economy": -10}),
    ),
    Card(
        card_id=95,
        character="Pop-up Repair Café Lead",
        text=(
            "A monthly repair café lets people fix broken gadgets instead of throwing them away."
        ),
        left_choice=Choice("People can do this at home", {"environment": -5}),
        right_choice=Choice("Support the café", {"environment": 10, "happiness": 15, "economy": -5}),
    ),
    Card(
        card_id=96,
        character="Energy Audit Team",
        text=(
            "A free energy audit for city businesses could help them cut bills and pollution."
        ),
        left_choice=Choice("Businesses decide alone", {"energy": -5, "environment": -5}),
        right_choice=Choice("Run the audit", {"energy": 10, "environment": 10, "economy": -5}),
    ),
    Card(
        card_id=97,
        character="Migrant Support Worker",
        text=(
            "New residents need guides to the city's recycling and energy-saving schemes in their languages."
        ),
        left_choice=Choice("One language is enough", {"happiness": -10, "environment": -5}),
        right_choice=Choice("Translate guides", {"happiness": 15, "environment": 5, "economy": -5}),
    ),
    Card(
        card_id=98,
        character="Outdoor Cinema Group",
        text=(
            "Solar-powered outdoor cinemas would entertain residents and showcase green technology."
        ),
        left_choice=Choice("Stick to indoor cinemas", {"happiness": -5, "environment": -5}),
        right_choice=Choice("Launch outdoor cinema", {"happiness": 15, "environment": 5, "economy": -5}),
    ),
    Card(
        card_id=99,
        character="River Clean Energy Co.",
        text=(
            "Tidal turbines under the city bridge can generate clean power with zero visual impact."
        ),
        left_choice=Choice("Too experimental", {"energy": -5}),
        right_choice=Choice("Trial the turbines", {"energy": 15, "economy": -10, "environment": 5}),
    ),
    Card(
        card_id=100,
        character="City Historian",
        text=(
            "Old factory buildings can be renovated as eco-offices instead of being demolished."
        ),
        left_choice=Choice("Knock them down", {"environment": -10, "economy": 5}),
        right_choice=Choice("Renovate them", {"environment": 15, "economy": -10, "happiness": 10}),
    ),
    Card(
        card_id=101,
        character="Volunteer Network",
        text=(
            "10,000 residents signed up to reduce electricity use between 5 and 7 pm daily."
        ),
        left_choice=Choice("People won't bother", {"energy": -5, "happiness": -5}),
        right_choice=Choice("Launch the scheme", {"energy": 15, "happiness": 10, "economy": 5}),
    ),
    Card(
        card_id=102,
        character="Lighting Designer",
        text=(
            "Dynamic street lighting — brighter only when people are nearby — can save 40% energy."
        ),
        left_choice=Choice("Fixed lighting is safer", {"energy": -10}),
        right_choice=Choice("Install smart lights", {"energy": 15, "economy": 10, "happiness": 5}),
    ),
    Card(
        card_id=103,
        character="Water Engineer",
        text=(
            "Leaky water pipes waste 20% of the city's water. Fixing them will save money and resources."
        ),
        left_choice=Choice("Later", {"environment": -10, "economy": -5}),
        right_choice=Choice("Fix them now", {"environment": 15, "economy": 10}),
    ),
    Card(
        card_id=104,
        character="Pop Star Fan Club",
        text=(
            "A famous musician offered to perform at a free green-themed concert in the city park."
        ),
        left_choice=Choice("Decline politely", {"happiness": -10}),
        right_choice=Choice("Accept the offer", {"happiness": 25, "economy": -5, "environment": 5}),
    ),
    Card(
        card_id=105,
        character="City Data Officer",
        text=(
            "Publishing real-time pollution maps online lets residents see air quality on their phones."
        ),
        left_choice=Choice("Data stays internal", {"happiness": -5, "environment": -5}),
        right_choice=Choice("Publish the map", {"happiness": 10, "environment": 5}),
    ),
    Card(
        card_id=106,
        character="Tool Library Lead",
        text=(
            "A city tool library lets residents borrow drills and ladders instead of buying new ones."
        ),
        left_choice=Choice("Not practical", {"economy": -5, "environment": -5}),
        right_choice=Choice("Open the library", {"economy": 5, "environment": 10, "happiness": 10}),
    ),
    Card(
        card_id=107,
        character="Green Festival Planner",
        text=(
            "A three-day green festival with food, music, and workshops can draw visitors and boost the local economy."
        ),
        left_choice=Choice("Too costly", {"economy": -5, "happiness": -5}),
        right_choice=Choice("Host the festival", {"economy": 10, "happiness": 20, "environment": 5}),
    ),
    Card(
        card_id=108,
        character="Child Health Doctor",
        text=(
            "Air pollution near primary schools is linked to breathing problems in children. We need action."
        ),
        left_choice=Choice("Levels are within limits", {"environment": -15, "happiness": -10}),
        right_choice=Choice("Create clean air zones", {"environment": 20, "happiness": 10, "economy": -10}),
    ),
    Card(
        card_id=109,
        character="Bike Maintenance Team",
        text=(
            "A free bike repair scheme will keep more bikes on the road and cut car use."
        ),
        left_choice=Choice("People fix their own", {"environment": -5, "happiness": -5}),
        right_choice=Choice("Fund the scheme", {"environment": 10, "happiness": 10, "economy": -5}),
    ),
    Card(
        card_id=110,
        character="Street Food Vendor",
        text=(
            "Allowing electric food carts in parks will reduce takeaway packaging and delight visitors."
        ),
        left_choice=Choice("Stick to restaurants", {"happiness": -5, "environment": -5}),
        right_choice=Choice("Allow electric carts", {"happiness": 10, "environment": 5, "economy": 5}),
    ),
    Card(
        card_id=111,
        character="Night Watchman",
        text=(
            "Offices and shops leave lights on all night. A rule to switch off after closing will save energy."
        ),
        left_choice=Choice("Business choice", {"energy": -10, "environment": -5}),
        right_choice=Choice("Introduce the rule", {"energy": 15, "environment": 10, "happiness": -5}),
    ),
    Card(
        card_id=112,
        character="Green Future Advisor",
        text=(
            "The city can set an official goal of being 100% renewable by 2040 and publish a clear plan."
        ),
        left_choice=Choice("Goals can change", {"happiness": -10, "environment": -5}),
        right_choice=Choice("Commit to the goal", {"happiness": 15, "environment": 20, "energy": 5, "economy": -5}),
    ),
]
