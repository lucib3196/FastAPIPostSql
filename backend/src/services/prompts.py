pokemon_description_prompt = """You are given the following information about a user-created Pokémon:

    - Name: {name}
    - Current Description: {description}
    - Physical Attributes: {physical_attr}
    - Type: {ptype}

    Your task is to rewrite and improve the description.

    Guidelines:
    - Make the description fun, lighthearted, and a little humorous — something that feels interesting and playful to read.
    - Keep it short and punchy: about 750 characters max.
    - Expand slightly on what the user originally wrote, adding flair or small funny details, but don’t lose the original intent.
    - The final description should feel like a witty Pokédex entry that makes readers smile while still giving useful info.
    - Reminder that these are essentially Pokémon, so the tone should highlight their animal-like qualities while also giving them fun and loving personalities.
    
    Additionally you are tasked with generating an image description for the pokemon
    This description will expand on the physical attributes provided by the user and use the description as well to take into account. The description should be 
    descriptive of the pokemons feature as it will be used for image generation, but also keep it in the style of the pokedex so it can work as an individual description as well
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
    Core Concept: {new_description}
    Image Description: {image_description}
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
  - **Description** (short, fun explanation of what the move does, in a Pokémon-style flavor)
- Make sure the moves balance between offensive, defensive, and flavor-based.

### Pokemon Data
    Name: {name}
    Core Concept: {description}
    Pokémon Type: {ptype}
"""


pokemon_cute_animations = """
You are designing playful, non-combat animations for a fan-created, Pokémon-inspired creature.
These are not battle moves — they are cute, goofy, or endearing expressions that showcase personality.

Generate EXACTLY 3 personality-based animations.

Constraints:
- Tone: lighthearted, charming, anime/Pokédex side-content vibes.
- Avoid combat terms (damage, accuracy, power, status conditions).
- Animations should be short and loopable (2–6 frames).
- Descriptions: concise (1–2 sentences, <= 200 characters).
- Prefer the creature’s typing ({ptype}); Normal-type allowed for neutral actions.
- Categories: ["Flavor", "Cute", "Playful"].
- Moods: ["happy", "silly", "sleepy", "curious", "proud", "shy", "mischievous", "calm"].
- Styles: ["idle", "dance", "pose", "reaction", "quirk"].

Input:
- Name: {name}
- Core Concept: {description}
- Pokémon Type: {ptype}

Examples:

# Example 1 (Water-type, goofy personality)
1. Bubble Hop (Water, Cute, happy, dance) — Hops side-to-side while blowing bubbles that pop around its horns.
2. Puddle Prance (Normal, Playful, mischievous, quirk) — Prances through a puddle, splashing water in a looping rhythm.
3. Clumsy Tumble (Normal, Cute, silly, reaction) — Trips over its own feet in a goofy way, making others laugh.

# Example 2 (Fire-type, proud personality)
1. Tail Torch Spin (Fire, Flavor, proud, pose) — Spins its flaming tail like a baton, grinning with confidence.
2. Warm Nap (Normal, Cute, sleepy, idle) — Curls up and snoozes, tiny heat waves rising gently from its body.
3. Flicker Wink (Fire, Playful, mischievous, quirk) — Winks as its tail flame flickers into a heart shape.

# Example 3 (Electric-type, energetic personality)
1. Spark Bounce (Electric, Playful, happy, dance) — Bounces in place with little sparks popping at its feet each time it lands.
2. Static Fluff (Electric, Cute, silly, reaction) — Shakes itself, puffing up with static-charged fur that sticks out messily.
3. Zippy Dash (Normal, Flavor, curious, idle) — Darts forward in a quick blur, then looks back proudly with a cheeky grin.
"""


pokemon_sprite_base = """
You are a professional pixel artist creating sprite bitmaps for a Game Boy Advance–inspired video game. 
Follow these artistic and technical constraints:

🎨 Art Style Guidelines
- Resolution per sprite frame: 16×16, 32×32, or 64×64 pixels, depending on sprite scale.
- Color Palette: Use 16–32 colors that are vibrant yet slightly muted, matching the GBA aesthetic.
- Background: Ensure the background is pure white (#FFFFFF), with no transparency.
- Stylistic Details:
  • Strong black outlines
  • High-contrast shading
  • Clear, readable silhouettes
- Animation Consistency: Keep proportions and readability uniform across all frames.

🖼️ Output Instructions
- Animation Type:
  Create a **3/4 quarter-view animation** with exactly 4 frames.
  Each frame must be unique and clearly depict progression in the animation cycle.

- Layout Format:
  • Present all 4 frames in a 2×2 grid, with one sprite per quadrant only.
  • Each sprite must be scaled and positioned to take up as much space as possible within its quadrant, while keeping consistent proportions across frames.
  • The entire grid must fit within a 1024×1024-pixel canvas.
  • Sprites must be perfectly centered in their quadrants with consistent alignment.

- Return Format:
  • Output the pixel grid only.
  • Do not include explanatory text, captions, or additional metadata.
  • Ensure pixel art style strictly matches Game Boy Advance limitations.

## Pose to Generate
Animation: {animation}
"""
