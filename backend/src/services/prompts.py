pokemon_description_prompt = """You are given the following information about a user-created Pokémon:

    - Name: {name}
    - Current Description: {description}
    - Physical Attributes: {physical_attr}
    - Type: {ptype}

    Your task is to rewrite and improve the description.

    Guidelines:
    - Make the description fun, lighthearted, and a little humorous — something that feels interesting and playful to read.
    - Keep it short and punchy: about 400 characters max.
    - Expand slightly on what the user originally wrote, adding flair or small funny details, but don’t lose the original intent.
    - The final description should feel like a witty Pokédex entry that makes readers smile while still giving useful info.
    - Reminder that these are essentially Pokémon, so the tone should highlight their animal-like qualities while also giving them fun and loving personalities.
"""


pokemon_image_generation_prompt = """A Pokémon in the style of the 1990s Pokémon Game Boy games mixed with the classic 90s anime art style. 
    Bold black outlines, flat colors, pixelated shading, limited retro Game Boy color palette, nostalgic vibe. 
    Looks like official Pokémon Red/Blue/Yellow art combined with 90s Saturday morning cartoon anime aesthetics. 
    Retro cel-shaded textures, slightly grainy background that resembles old cartridges and anime cels. 
    Dynamic but simple pose, clear silhouette, authentic to 1990s Pokémon designs. 
    Make sure the design strongly reflects the given description and type while keeping the look faithful to the 90s era.
    When generating the image ensure that it is just the pokemon do not include any text
    Here is a description of the Pokémon given from the user. 
    Expand on their ideas but keep the general essence of what they want. 
    Make sure the result looks like an authentic 1990s Pokémon design.
    
    ### Pokemon Data
    Name: {name}
    Core Concept: {description}
    Pokémon Type: {ptype}
    
    
    GuideLines:
    When generating the image only return the created pokemon do not return any text in the image you are just tasked at generating the image
    """


pokemon_moveset_prompt = """You are designing a moveset for a fan-created Pokémon-inspired creature. 
Base your moves on the creature’s type(s), physical attributes, and personality.

### Requirements:
- Provide **3 moves** that fit the creature at its current evolutionary stage.
- Each move should include:
  - **Move Name**
  - **Type** (must align with or complement the Pokémon’s type)
  - **Category** (Physical / Special / Status)
  - **Power** (if applicable)
  - **Accuracy**
  - **Description** (short, fun explanation of what the move does, in a Pokémon-style flavor)
- Make sure the moves balance between offensive, defensive, and flavor-based.

### Pokemon Data
    Name: {name}
    Core Concept: {description}
    Pokémon Type: {ptype}
"""


pokemon_cute_animations = """


You are designing fun, lighthearted moves for a fan-created Pokémon-inspired creature.  
The goal is to showcase the creature’s **personality** and **charm** rather than battle strength.  
Think of these as playful moves that would appear in a Pokémon anime episode, Pokédex entry, or in a side-game focused on personality.

### Requirements:
- Generate **2 basic moves**.
- Each move should include:
  - **Move Name**
  - **Type** (aligned loosely with the creature’s typing, but can include playful Normal-type)
  - **Category**: (Flavor / Cute / Playful) → instead of Physical/Special/Status
  - **Description**: A short, fun explanation of what the move looks like and why it shows off the Pokémon’s personality.
- Keep them **cute, goofy, or endearing** — not necessarily strong.

### Example Input:
- Name: Tricklehorn
- Type: Water
- Physical Attributes: Small, blue, triceratops-like creature with stubby horns and a droplet-shaped frill.
- Personality: Goofy, fun-loving, playful but hardworking.

### Example Output:
1. **Bubble Giggle**  
   - Type: Water  
   - Category: Cute  
   - The Pokémon blows a stream of bubbles and pops them with its horns while giggling.  

2. **Horn Wiggle**  
   - Type: Normal  
   - Category: Playful  
   - It wiggles its stubby horns in a silly way to look tough but only makes others smile.  

3. **Puddle Splash**  
   - Type: Water  
   - Category: Flavor  
   - The Pokémon stomps in a puddle, splashing water everywhere like a child playing.  

4. **Clumsy Tumble**  
   - Type: Normal  
   - Category: Cute  
   - Trips over its own feet in a silly way, making it oddly endearing to watch.  


### Pokemon Data
    Name: {name}
    Core Concept: {description}
    Pokémon Type: {ptype}
    
    
"""
