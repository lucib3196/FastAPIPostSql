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


pokemon_moveset_prompt = """
You are designing a moveset for a fan-created Pokémon-inspired creature. 
Base your moves on the creature’s type(s), physical attributes, and personality.

### Requirements:
- Provide **3 moves** that fit the creature at its current evolutionary stage.
- Each move must include:
  - **Move Name**
  - **Type** (must align with or complement the Pokémon’s type)
  - **Category** (Physical / Special / Status)
  - **Description** (short, fun explanation of what the move does, in a Pokémon-style flavor)
  - **sprite_animation**: a 4-step frame breakdown describing exactly how the move would look in sprite form.

### Sprite Animation Guidelines:
- Always provide exactly 4 frames.
- Each frame should describe: body pose, facial expression, secondary effects (particles, light, ripples, sparks, etc.), and transitions between frames.
- Make the loop flow naturally, with a clear visual start and finish for pixel artists.
- Keep details fun and expressive, in line with Pokémon-style battle animations.

### Pokemon Data
    Name: {name}
    Core Concept: {description}
    Pokémon Type: {ptype}

### Example
1. **Move Name**: Aqua Tail
   - Type: Water
   - Category: Physical
   - Description: Swings its tail like a crashing wave to strike the foe.
   - sprite_animation:
     - Frame 1: Creature crouches low, tail glows faintly with rippling water aura.
     - Frame 2: Tail swings upward in a wide arc, water droplets spray outward.
     - Frame 3: Impact frame — tail fully extended, large water splash effect appears.
     - Frame 4: Returns to neutral stance, droplets fall away as glow fades.

2. **Move Name**: Mist Veil
   - Type: Water
   - Category: Status
   - Description: Envelops itself in a thin mist, raising evasiveness.
   - sprite_animation:
     - Frame 1: Creature inhales deeply, eyes glow faintly.
     - Frame 2: Releases a soft mist from mouth, fog begins spreading around feet.
     - Frame 3: Mist thickens, body partly obscured, eyes shimmer through haze.
     - Frame 4: Stance resets, mist swirls gently in background loop.

3. **Move Name**: Ripple Pulse
   - Type: Water
   - Category: Special
   - Description: Fires a pulse of watery ripples that expand outward.
   - sprite_animation:
     - Frame 1: Creature leans forward, energy gathers in its mouth.
     - Frame 2: A glowing ripple orb forms, water rings start to emanate.
     - Frame 3: Orb bursts forward, ripple waves expand in concentric circles.
     - Frame 4: Returns upright, waves fade as motion settles.
"""


pokemon_cute_animations = """
You are designing playful, non-combat animations for a fan-created, Pokémon-inspired creature.
These are not battle moves — they are cute, goofy, or endearing expressions that showcase personality.

Generate EXACTLY 4 distinct personality-based animations.

Constraints:
- Each animation must be described in DETAIL, enough for a pixel artist to create 2–6 looping frames.
- Include a `sprite_animation` field: a step-by-step guide with exactly 4 entries, each describing a single frame’s pose, expression, and effects.
- Go beyond one sentence: describe body movements, facial expressions, secondary effects (like bubbles, sparks, ripples), and how the loop resets smoothly.
- Tone: lighthearted, charming, anime/Pokédex side-content vibes.
- Avoid combat terms (damage, accuracy, power, status conditions).
- Prefer the creature’s typing ({ptype}); Normal-type allowed for neutral actions.
- Each animation must include:
  • Name
  • Type
  • Category: ["Flavor", "Cute", "Playful"]
  • Mood: ["happy", "silly", "sleepy", "curious", "proud", "shy", "mischievous", "calm"]
  • Style: ["idle", "dance", "pose", "reaction", "quirk"]
  • Description: High-level summary (≤ 350 characters).
  • sprite_animation: Detailed 4-step frame breakdown.

Input:
- Name: {name}
- Core Concept: {description}
- Pokémon Type: {ptype}

Examples:

# Example 1 (Water-type, goofy personality)
1. Bubble Hop (Water, Cute, happy, dance)
   Description — The creature hops side-to-side, spitting playful bubbles that float and pop in rhythm.

   sprite_animation:
   - Frame 1: Body crouched low, cheeks puffed as a bubble forms at mouth.
   - Frame 2: Jump upward, arms flailing outward, bubble drifts upward.
   - Frame 3: Lands to the right, eyes squinted in joy, bubble pops.
   - Frame 4: Resets to center, ready to hop again with small water splash underfoot.

2. Puddle Prance (Normal, Playful, mischievous, quirk)
   Description — Splashes in a puddle while grinning mischievously, droplets scattering outward.

   sprite_animation:
   - Frame 1: Front paw dips into small puddle, ripple begins.
   - Frame 2: Both feet stomp playfully, droplets spray upward.
   - Frame 3: Head leans forward with wide grin, droplets still in the air.
   - Frame 4: Returns upright, puddle ripples settle into circles, ready to repeat.

3. Clumsy Tumble (Normal, Cute, silly, reaction)
   Description — Trips forward dramatically, rolling harmlessly before popping back upright.

   sprite_animation:
   - Frame 1: Steps forward with paw outstretched, eyes wide.
   - Frame 2: Stumble in midair, arms flailing, mouth open in panic.
   - Frame 3: Body rolls onto ground, small dust puff at impact.
   - Frame 4: Pops back upright, dizzy swirl above head, loop restarts.

4. Bubble Nose Wiggle (Water, Flavor, curious, idle)
   Description — Wiggles nose, releasing tiny shimmering bubbles that drift upward.

   sprite_animation:
   - Frame 1: Head tilts slightly left, nose scrunches.
   - Frame 2: Tiny bubble forms at nostril, eyes half-closed.
   - Frame 3: Bubble floats upward, nose wiggles again.
   - Frame 4: Bubble pops gently, eyes blink, loop resets.
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
