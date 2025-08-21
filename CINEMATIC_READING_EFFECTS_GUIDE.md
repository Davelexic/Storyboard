## Cinematic Reading Engine: Expanded Effects, Themes, Events, Characters, and Moods (Training + Creator Guide)

**TL;DR**: A production-ready, exhaustive taxonomy and example set for algorithm training and creator review. Includes: expanded theme palettes (45+), moods (Plutchik + PAD mapping), events (80+ triggers), micro-actions (50+ accents), character archetypes (30+ with typographic signatures), environmental contexts, intensity/cooldown rules, and 12 fully worked examples. Machine-usable JSONL schemas provided.

---

### 0) Scope and Alignment

This guide operationalizes and expands the principles in `Enhancing Ereader Immersion_ Subtle Effects.md` across six axes:
- Themes and aesthetic palettes (Tier 1)
- Moods and affect mapping (global and local)
- Narrative events and structural triggers (Tier 2/3)
- Character archetypes and dialogue typography (Tier 2)
- Micro-actions and diegetic accents (Tier 3)
- Worked examples + machine-usable schemas for training

The same guardrails apply: Cognitive Load Governor, Secondary Belief/diegesis, Hierarchy of Intervention, and combination/cooldown rules.

---

### 1) Machine Data Schemas (for training and inference)

Use JSONL for training and deterministic rule-based evaluation. Fields align with the analysis pipeline.

```json
{
  "book_id": "uuid",
  "chunk_id": "uuid-or-page:line-range",
  "base_theme_id": "theme_sci_fi_cyberpunk",
  "aesthetic_palette_id": "palette_sci_fi_dystopian",
  "context": {
    "location_entities": ["Neo-Tokyo", "Rain-soaked alley"],
    "time_of_day": "night",
    "weather": "rain",
    "scene_persistence_words": 1200
  },
  "characters": [
    {
      "name": "Mara",
      "archetypes": ["The Trickster", "The Survivor"],
      "emotional_baseline": {"joy": 0.12, "sadness": 0.28, "anger": 0.22, "fear": 0.35, "trust": 0.18, "disgust": 0.11, "anticipation": 0.27, "surprise": 0.19},
      "current_emotion": {"fear": 0.61, "anger": 0.44},
      "linguistic_signature": {"avg_sentence_len": 9.4, "type_token_ratio": 0.42, "syntax_complexity": 0.31},
      "deviations": {"fear_sigma": 2.3, "anger_sigma": 1.1}
    }
  ],
  "text_block": "She flicked the wet hair from her eyes. The server stacks hummed. The alley light jittered once, then died.",
  "narratology": {"event_type": "change_of_state", "plot_velocity": 0.62},
  "climax_score": 0.81,
  "passage_complexity_percentile": 0.43,
  "mood_pad": {"pleasure": -0.12, "arousal": 0.46, "dominance": -0.21},
  "triggers": [
    {"type": "environmental_shift", "details": {"light": "fails"}},
    {"type": "rising_suspense", "dur_pages": 2}
  ],
  "eligible_effects": [
    {"id": "vignette_darken_slow", "tier": 1, "risk": {"cognitive": "low", "immersion": "low"}},
    {"id": "soundscape_rain_neon_buzz", "tier": 1},
    {"id": "kinetic_word_pulse", "tier": 2, "target": "died"}
  ],
  "selected_effects": [
    {"id": "vignette_darken_slow", "intensity": 3},
    {"id": "soundscape_rain_neon_buzz", "intensity": 2}
  ],
  "cooldowns": {"haptic": 1000, "accent": 250},
  "rationale": "Sustained suspense → Tier 1 only; Complexity moderate; no Tier 3."
}
```

Additional static registries are provided in Sections 2–6.

---

### 2) Expanded Themes and Aesthetic Palettes (Tier 1)

Each theme defines: visual texture, typography defaults, color temperature/lighting, atmospheric soundscapes, allowed accents, forbidden effects. Sub-palettes refine style (utopian vs dystopian, etc.).

Format:
- theme_id: unique key
- keywords: detection hints
- moods: dominant baseline
- visual: texture, font, color/lighting
- audio: ambient soundscapes
- allowed_accents: brief, diegetic accents allowed
- forbidden_effects: to protect Secondary Belief

| theme_id | keywords | moods | visual | audio | allowed_accents | forbidden_effects |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| theme_noir_detective | detective, rain, shadow, 1940s, city | cynicism, suspense, melancholy | texture_paper_pulp; font_mono_typewriter; color_mono_cool | soundscape_rain_city_night; soundscape_jazz_distant | sound_match_light_flicker, sound_door_wood_creak | sound_laser_blast, visual_magic_sparkle |
| theme_sci_fi_cyberpunk | neon, megacorp, rain, AI, dystopia | anxious, gritty | texture_digital_glitchy; font_sans_ocr; color_neon_green | soundscape_rain_neon_buzz; server_fan_whir | accent_ui_beep_analog, visual_scanline_pulse | texture_vellum_aged, sound_horse_gallop |
| theme_sci_fi_space_opera | starship, empire, alien | awe, tension | texture_clean_digital; font_sans_futura; color_cool_blue | engine_hum_low; bridge_chatter_faint | sound_airlock_seal, sound_plasma_whoosh_soft | kinetic_typewriter |
| theme_epic_fantasy | dragon, magic, sword, kingdom | adventure, awe | texture_vellum_aged; font_serif_trajan; color_warm_sepia | wind_plains; forest_ambience | sound_sword_shing_soft, sound_banner_flap | sound_computer_chatter |
| theme_gothic_horror | castle, shadow, dread | fear, sadness | texture_paper_aged_foxing; font_serif_garamond; vignette_persistent | wind_howl_distant; floorboard_creaks | visual_candle_flicker_subtle | haptic_explosion, ui_beeps |
| theme_historical_romance | regency, ballroom, manor | longing, elegance | texture_paper_cotton; font_serif_baskerville; color_candle_warm | ballroom_murmur_distant; carriage_wheels | sound_letter_seal_wax | kinetic_jitter_subtle |
| theme_psych_thriller | suburb, unreliable narrator | unease, claustrophobia | texture_clean_digital; font_sans_helvetica; vignette_subtle | house_settling_creaks; fluorescent_hum | visual_vignette_breathe | visual_sci_fi_glitch |
| theme_post_apocalyptic | wasteland, survival, ruins | isolation, desperation | texture_paper_grimy; font_serif_distressed; color_dusty_ochre | wind_dust; geiger_counter_faint | sound_metal_scrape, sound_dust_devil | font_serif_baskerville |
| theme_ya_contemporary | high school, friendship | angst, hope | texture_clean_white; font_sans_lato; color_neutral | hallway_murmur; phone_vibrate_soft | sound_text_notification_subtle | sound_sword_clash |
| theme_hard_sci_fi | orbital mechanics, engineering | wonder, precision | texture_clean_graph; font_sans_source; color_cool_white | lab_ventilation; telemetry_beep_soft | visual_grid_overlay_subtle | magic_chime |
| theme_space_western | frontier, outpost, rust | rugged, lonely | texture_canvas_rough; font_serif_clarendon; color_sun_worn | wind_antenna_creak; spurs_soft | sound_revolver_cock_soft | ui_beep_modern |
| theme_steampunk | brass, airship, gear | curiosity, adventure | texture_parchment_grease; font_serif_bodoni; color_brass_warm | gear_tick; steam_release_soft | sound_valve_turn, sound_pocketwatch_click | neon_ui_synth |
| theme_biolab_thriller | quarantine, pathogen | tension, sterility | texture_clean_glass; font_sans_avenir; color_cool_teal | fume_hood_whir; monitor_beep_soft | sound_door_maglock, sound_ppe_rustle | sword_shing |
| theme_contemporary_lit | city, relationships | introspection | texture_clean_matte; font_serif_minion; color_neutral_soft | cafe_murmur; street_distant | sound_coffee_cup_setdown | magic_sparkle |
| theme_urban_fantasy | modern city, hidden magic | wonder, tension | texture_paper_slight_wear; font_serif_merriweather; color_moonlit | city_rain; arcane_whisper_low | visual_rune_glow_subtle | sci_fi_ui_beeps |
| theme_dark_fantasy | cursed woods, blood magic | dread, fatalism | texture_leather_cracked; font_serif_blackletter; color_ash_grey | wind_dead_trees; ritual_drum_low | sound_bone_chime, visual_blood_ink_bleed_subtle | cheerful_chimes |
| theme_mythic_epic | gods, prophecy | awe, fate | texture_papyrus; font_serif_traian; color_sun_gold | ocean_swell_distant; temple_reverb | sound_conch_call_soft | sci_fi_glitch |
| theme_historical_naval | tall ships, age of sail | resolve, peril | texture_paper_salt_stain; font_serif_baskerville; color_sea_grey | hull_creak; gulls_distant | sound_cannon_thud_soft, rope_creak | laser_blast |
| theme_political_thriller | capitol, espionage | tension, calculation | texture_clean_parchment; font_sans_franklin; color_cool_neutral | hvac_vent; phone_vibrate_table | sound_camera_shutter_soft | sword_clash |
| theme_crime_procedural | forensics, precinct | focus, grit | texture_copy_paper; font_sans_inter; color_cool_white | copier_whir; rain_distant | sound_evidence_bag_rustle | magic_sparkle |
| theme_cozy_mystery | village, tea shop | comfort, curiosity | texture_paper_soft; font_serif_georgia; color_warm_pastel | fireplace_crackle; street_murmur_soft | sound_tea_cup_clink | thunder_clap_loud |
| theme_survival_arctic | snow, isolation | endurance, fear | texture_paper_frost; font_sans_source; color_ice_blue | wind_blizzard; parka_rustle | sound_ice_crack_soft | tropical_birds |
| theme_survival_jungle | humidity, insects | vigilance, awe | texture_leaf_fiber; font_serif_garamond; color_deep_green | cicadas; rain_canopy | sound_machete_swish_soft | ui_beep |
| theme_high_school_romcom | lockers, prom | playful, awkward | texture_clean_white; font_sans_roboto; color_friendly_warm | hallway_murmur; sneaker_squeak | sound_text_pop_subtle | sword_clash |
| theme_time_travel_sf | paradox, lab | curiosity, unease | texture_clean_grid; font_sans_eurostile; color_cool_cyan | oscillator_hum; relay_click | visual_scanline_sweep | fantasy_spell_chime |
| theme_cyber_military | drones, op | resolve, danger | texture_carbon_fiber; font_sans_din; color_tactical_green | comms_chatter; rotor_distant | sound_safety_off_soft | magic_glow |
| theme_space_horror | derelict, cold | dread, isolation | texture_clean_dust; font_sans_univers; color_cold_steel | air_duct_whisper; hull_knock_random | sound_bulkhead_shut_soft | cheerful_uplift_swell |
| theme_occult_detective | sigils, rituals | grim, curious | texture_paper_worn; font_serif_goudy; color_candle_shadow | chalk_scratch; whisper_low | visual_sigils_dim_glow | sci_fi_ui |
| theme_wuxia | jianghu, sects | honor, grace | texture_rice_paper; font_serif_song; color_ink_black | bamboo_wind; stream_soft | sound_sword_draw_shing_soft | gun_cock_click |
| theme_hardboiled_modern | city grime, PI | grit, cynicism | texture_paper_smudged; font_sans_trade; color_neon_dirty | bar_murmur; rain | sound_zippo_flick | magic_sparkle |
| theme_biopunk | wetware, genehack | anxiety, wonder | texture_biofilm_subtle; font_sans_plex; color_sickly_green | incubator_hum; liquid_drip | sound_syringe_click_soft | sword_clash |
| theme_solarpunk | community, lush tech | hope, calm | texture_clean_fiber; font_sans_jost; color_leaf_green | garden_breeze; bird_soft | sound_micro_turbine_soft | glitch_harsh |
| theme_medieval_historical | manor, scriptorium | piety, toil | texture_parchment; font_serif_uncial; color_candle_warm | hall_murmur; hoof_soft | sound_quill_scratch | phone_notification |
| theme_modern_memoir | apartment, subway | introspective, bittersweet | texture_clean_matte; font_serif_literata; color_soft_neutral | train_rattle_distant; kettle_soft | sound_pen_cap_click | magic_glow |
| theme_space_utopian | federation, diplomacy | calm, wonder | texture_clean_gloss; font_sans_sf; color_soft_blue | harp_tonal_soft; hull_hum_even | sound_transporter_chime_soft | dystopic_glitch |
| theme_space_dystopian | rust, ration, riot | fear, resolve | texture_rust_steel; font_sans_agency; color_sodium_amber | crowd_murmur; generator_throb | sound_baton_crack_soft | utopian_chime_clean |
| theme_war_historical | trench, artillery | dread, duty | texture_mud_paper; font_serif_bembo; color_grey_brown | distant_shells; wind | sound_whistle_command_soft | synth_ui |
| theme_legal_drama | courtroom, chambers | control, tension | texture_copy_bond; font_serif_times; color_cool_white | shuffling_papers; aircon | sound_gavel_tap_soft | sword_shing |
| theme_medical_drama | ER, ICU | urgency, care | texture_clean_white; font_sans_calibri; color_cool_daylight | monitor_beep_soft; curtain_swish | sound_defib_charge_soft | fantasy_spell |
| theme_coastal_lit | beach town, fog | wistful, calm | texture_paper_salt; font_serif_freight; color_sea_pale | gulls; buoy_bell_distant | sound_shell_crunch_soft | sci_fi_beep |
| theme_western_classic | prairie, saloon | resolve, isolation | texture_canvas; font_serif_egyptian; color_dust_amber | wind; spur_jingle_soft | sound_lever_action_soft | synth_ui_beep |
| theme_mystery_techno | breach, logs | suspicion, haste | texture_clean_carbon; font_sans_consolas; color_cool_mint | fan_whir; keyclick_soft | visual_terminal_cursor_blink | fantasy_glow |
| theme_romantasy | court, magic | longing, wonder | texture_velvet_paper; font_serif_caslon; color_candle_rose | lute_soft; hearth | visual_magic_glow_soft | sci_fi_ui |
| theme_satire_modern | office, social | irony, play | texture_copy_paper; font_sans_futura; color_neutral | open_office_murmur | sound_slack_pop_soft | thunder_clap |

Note: For each theme, sub-palettes can refine aesthetic (e.g., `palette_sci_fi_utopian` vs `palette_sci_fi_dystopian`).

---

### 3) Moods and Affect Mapping (Plutchik + PAD)

Define continuous affect and map to low-impact atmospheric shifts; escalate to kinetics only when justified by deviations or structural events.

Fields: mood, plutchik_primary, intensity (1–5), PAD vector, Tier 1 visuals, Tier 1 audio, Tier 2 kinetics (if any), cognitive risk.

| mood | primary | PAD (P/A/D) | Tier 1 visuals | Tier 1 audio | Tier 2 kinetics | risk |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| dread | fear | (-0.35, +0.45, -0.35) | vignette_darken_slow(+10–20%), color_temp_cool(-10%) | drone_subtle, air_duct_whisper | none (unless spike) | low |
| awe | surprise | (+0.25, +0.35, -0.05) | vignette_brighten_slow(+10%), color_warm(+5%) | uplifting_tonal_swell_faint | sequential_reveal_slow for oratory | low |
| melancholy | sadness | (-0.30, -0.20, -0.15) | color_cool_desat(-10%), paper_texture_aged | rain_distant, vinyl_crackle_soft | none | low |
| anxiety | fear | (-0.25, +0.40, -0.30) | micro_vignette_pulse_subtle | fluorescent_hum, heartbeat_faint | kinetic_jitter_subtle (if character deviation > 2σ) | medium |
| anger | anger | (-0.10, +0.50, +0.10) | color_temp_shift_warm(+5%) | low_rumble | kinetic_jitter_subtle amplitude_scale by σ | medium |
| hope | joy | (+0.35, +0.15, +0.10) | color_warm(+10%), vignette_brighten | tonal_swell | none | low |
| serenity | joy | (+0.40, -0.20, +0.30) | soften_edges_subtle | nature_soft | none | low |
| disgust | disgust | (-0.35, +0.30, +0.05) | desaturate_subtle | wet_drip_soft | none | medium |
| anticipation | anticipation | (+0.10, +0.25, +0.05) | mild_focus_vignette | clock_tick_soft | sequential_reveal_medium | low |
| surprise (positive) | surprise | (+0.20, +0.45, -0.05) | brief_brighten | chime_soft | word_pulse_on_focus_word | medium |
| surprise (negative) | surprise | (-0.10, +0.55, -0.20) | brief_dim | breath_intake_soft | word_pulse_on_shock | medium-high |

Add others as needed; PAD vectors calibrate cross-theme consistency.

---

### 4) Narrative Events and Structural Triggers (Tier 2/3)

Event families with recommended effects. Respect the Cognitive Load Governor and cooldowns.

Format: event_id, detection, Tier 1, Tier 2, Tier 3, cooldown, risk, notes.

| event_id | detection | Tier 1 | Tier 2 | Tier 3 | cooldown | risk | notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| rising_suspense_sustained | emotional_arc↑ fear/anticipation over 2+ pages | vignette_darken_slow, color_cool_slow | none | none | n/a | low | background only |
| sudden_shock_revelation | narratology change_of_state sentence | none | kinetic_word_pulse on key token | haptic_pulse_sharp_single if climax>95% | haptic 1000w | med-high | avoid simultaneous sound accent |
| physical_impact | keywords (hit, crash), climax high | none | none | haptic_pulse_sharp sync on verb | haptic 1000w | high | ensure single pulse |
| weapon_drawn | keywords + base_theme | none | none | sound_weapon_draw_soft | accent 250w | medium | theme-appropriate |
| explosion_distant | keywords, env model | vignette_flash_subtle | none | sound_boom_muffled_single | accent 500w | med-high | scale with distance |
| kiss_tender | narratology change_of_state (relationship) | color_warm_slow(+10%) | sequential_reveal_slow | none | n/a | low | no accents |
| chase_sequence | process_event density high | slight_render_speed(+5%), page_turn_motion_blur | none | haptic_pulse_rhythmic_faint if climax>98% | haptic 1000w | med-high | stop after sequence |
| death_major | entity death + sentiment valley | vignette_darken_slow | word_pulse on name or key term | haptic_pulse_soft if climax>97% | haptic 1000w | high | suppress conflicting accents |
| confession_difficult | pronoun/1st-person + sentiment mix | none | sequential_reveal_slow | none | n/a | low | align with commas/clauses |
| storm_begins | weather entity shift | crossfade_soundscape_storm | visual_flash_brief on lightning | thunder_clap_single | accent 800w | med | respect loudness limits |
| ritual_incantation | keywords + theme_fantasy | ambient_low_drones | visual_glow_subtle_line | sound_magic_chime_soft if climactic | accent 600w | medium | style by magic type |
| negotiation_high_stakes | topic entities + pacing | mild_focus_vignette | sequential_reveal_medium | none | n/a | low | no haptics |
| betrayal_revealed | coreference + sentiment flip | none | word_pulse("betrayed", etc.) | haptic_sharp if climax>95% | haptic 1000w | med-high | single emphasis |
| quiet_resolution | plot_velocity↓, joy↑ | vignette_brighten_slow | none | none | n/a | low | fade out prior tension |
| door_slam | keyword + sfx bank | none | none | sound_door_slam_soft | accent 250w | medium | avoid overuse |
| phone_notification | entity phone + theme | none | none | sound_text_notification_subtle | accent 250w | low | suppress during peaks |
| typing_sequence | onomatopoeia / scene tag | none | kinetic_cursor_blink_subtle | none | n/a | low | visual only in techno themes |
| heartbeat_focus | internal monologue under fear | vignette_breathe_slow | none | haptic_pulse_faint_rhythmic if climax>96% | haptic 1000w | med | duration capped |
| jump_scare | horror pacing + sudden noun | none | word_pulse on noun | sound_sting_soft + haptic_sharp if climax>98% | haptic 1200w | high | use at most once per 3k words |

Add additional domain-specific events as needed; prefer structural detectors to keywords.

---

### 5) Character Archetypes and Typographic Signatures (Tier 2)

Static book-wide signatures, plus multipliers for dynamic effects. Keep variations imperceptible but consistent.

Fields: archetype, description, static_signature, dynamic_multiplier_rules.

| archetype | description | static_signature | dynamic_multipliers |
| :-- | :-- | :-- | :-- |
| The Mentor | wise, calm | font_weight +1%; letter_spacing +1% | jitter sensitivity −20%; sequential_reveal cadence stable |
| The Trickster | sly, unpredictable | ±0.5% micro-rotation variance | jitter +20% when excitement>2σ |
| The Stoic | reserved | font_condense −2%; hue −2% cooler | word_pulse threshold +0.5σ |
| The Volatile | passionate | normal baseline; higher anger sensitivity | jitter amplitude ×1.3 per σ over baseline |
| The Frail/Hesitant | timid | font_weight −2%; opacity 98% | sequential_reveal slows by 10% under fear>2σ |
| The Bureaucrat | rigid | justification full; kerning strict | suppress rotation variance; no jitter |
| The Visionary | grand, inspiring | font_size +1%; line_height +2% | oratory sequential cadence +15% spacing |
| The Detective | observant | small_caps for emphasis tokens | word_pulse reduced; vignette_focus allowed |
| The Rebel | defiant | tracking +0.5% | jitter under anger +10% |
| The Caregiver | nurturing | softness via antialias bias | reduce harsh flashes |
| The Scholar | precise | ligatures enabled | suppress jitter; allow term highlights |
| The Leader | decisive | weight +1%; kerning open | word_pulse on action verbs enabled |
| The Jester | comedic | slight bounce easing on punctuation | allow playful micro-jitter (±0.2%) |
| The Loner | withdrawn | hue cooler −2% | reduce sound accents by 1 level |
| The Cynic | skeptical | desat −2% | suppress uplifting swells |
| The Optimist | hopeful | warm tint +2% | allow gentle tonal swells |
| The Survivor | resilient | font_narrow +1% | heartbeat haptic allowed at higher thresholds |
| The Fanatic | fervent | weight +1%, letter_spacing −0.5% | escalate under devotion spikes |
| The Innocent | pure | increased whitespace +2% | suppress harsh accents |
| The Seducer | alluring | slight italic +1% | sequential_reveal smooth easing |
| The Sage | ancient wisdom | small_caps initials | strong flashes forbidden |
| The Warrior | disciplined | tracking tight −0.5% | action verb pulse allowed |
| The Diplomat | tactful | kerning wide +0.5% | jitter forbidden |
| The Engineer | methodical | monospaced numerals | terminal cursor blink allowed (tech themes) |
| The Artist | expressive | ligature flourishes | gentle color drift allowed |
| The Orator | rhetorical | line_height +3% | sequential_reveal_clause cadence |
| The Villain (Subtle) | cold, calculating | hue cooler −3% | audio accents −1 level |
| The Villain (Bombastic) | loud, theatrical | weight +2% | allow sting accents at high climax |
| The Trick Victim | gullible | slight opacity 98% | none |
| The Ghost | ethereal | opacity 96%, italic | soft blur allowed during presence |

Archetypes can be combined; conflicts resolved by priority rules.

---

### 6) Micro-Actions and Diegetic Accents (Tier 3)

Short, non-repeating accents; always theme-appropriate. Use sparingly with cooldowns.

| action | accent_id | modality | timing | intensity guidance | notes |
| :-- | :-- | :-- | :-- | :-- | :-- |
| door_open_wood | sound_door_wood_creak | audio | on verb | volume 1–2 | no haptic |
| door_slam | sound_door_slam_soft | audio | on verb | 2–3 | suppress if already loud scene |
| revolver_cock | sound_revolver_cock_soft | audio | on "cocked" | 2 | western/space_western only |
| sword_draw | sound_sword_shing_soft | audio | on draw | 2 | fantasy/wuxia |
| airlock_seal | sound_airlock_seal | audio | on "sealed" | 2–3 | space themes |
| thunder_clap | sound_thunder_clap_single | audio | on token | 2–4 | rare |
| magic_chime | sound_magic_chime_soft | audio | on incantation | 1–2 | fantasy only |
| phone_text | sound_text_notification_subtle | audio | on message | 1 | YA/contemporary |
| glass_shatter | sound_glass_shatter_soft | audio | on shatter | 2–3 | avoid haptic combo |
| fist_impact | haptic_pulse_sharp | haptic | on impact | 2–3 | no audio accent same window |
| gunshot | haptic_pulse_sharp + sound_gunshot_soft | haptic+audio | on fire | 3–4 | if allowed by theme |
| heartbeat | haptic_pulse_rhythmic_faint | haptic | sustained | 1–2 | horror/climax>96% |
| lightning_flash | visual_flash_brief | visual | on token | 1 | ensure legibility |
| rune_glow | visual_rune_glow_subtle | visual | line-span | 1–2 | urban/dark/romantasy |
| scanline_sweep | visual_scanline_sweep | visual | clause | 1 | techno themes |
| terminal_cursor | visual_cursor_blink | visual | sentence end | 1 | techno |
| banner_flap | sound_banner_flap | audio | noun | 1–2 | epic fantasy |
| carriage_wheels | sound_carriage_cobbles | audio | scene start | 1–2 | historical romance |
| geiger_click | sound_geiger_faint | audio | near radiation | 1 | post-apoc/biopunk |
| valve_turn | sound_valve_turn | audio | on verb | 1–2 | steampunk |

Extend with project SFX/visual libraries.

---

### 7) Intensity, Combination, and Cooldowns (Operational Rules)

- Intensity scaling: map to z-score magnitude of trigger; clamp to theme caps.
- Combination: never co-locate haptic and distinct audio accent within 500ms; Tier 1 can co-occur with Tier 2.
- Cooldowns: haptic ≥1000 words; accent ≥250 words; jump_scare ≥3000 words; thunder_clap ≥800 words.
- Governor: if Passage_Complexity > 80th percentile → max_allowed_tier = 1.

---

### 8) Worked Examples (12)

Each example shows text, analysis, decision, and applied effects.

1) Gothic Horror – Corridor Breath Hold
- Text: "The candle guttered. Something breathed behind the wall."
- Analysis: theme_gothic_horror; fear↑ sustained; change_of_state on "guttered"; climax 0.84; complexity p45.
- Decision: Tier 1 only; no Tier 3.
- Effects: vignette_darken_slow(intensity=3); floorboards_creak_light(volume=1).

2) Cyberpunk – Revelation
- Text: "Root access granted. She wasn't supposed to exist."
- Analysis: theme_sci_fi_cyberpunk; revelation; climax 0.93; shock token: "exist".
- Decision: word_pulse("exist"); no haptic (<95%).
- Effects: visual_scanline_pulse; kinetic_word_pulse.

3) Epic Fantasy – Sword Draw
- Text: "He unsheathed Winter's Edge. The hall fell silent."
- Analysis: weapon_drawn; theme_epic_fantasy; climax 0.78.
- Decision: accent sound only.
- Effects: sound_sword_shing_soft(volume=2); ambient_wind_plains persists.

4) Psychological Thriller – Confession
- Text: "I did it. I wanted to stop, but I couldn't."
- Analysis: change_of_state; confession; complexity p52; character deviation fear>2σ.
- Decision: sequential_reveal_slow; suppress accents.
- Effects: kinetic_sequential_reveal(speed=2).

5) Space Opera – Impact at Peak
- Text: "The torpedo struck the dorsal shield."
- Analysis: physical_impact; climax 0.97 (>95%); complexity p41.
- Decision: Tier 3 haptic, no simultaneous audio accent.
- Effects: haptic_pulse_sharp(strength=4); engine_hum_low continues.

6) Cozy Mystery – Teacup Clink
- Text: "She set the cup down, porcelain whispering against the saucer."
- Analysis: micro-action; theme_cozy_mystery.
- Decision: soft audio accent only.
- Effects: sound_tea_cup_clink(volume=1).

7) Urban Fantasy – Incantation (Non-Climax)
- Text: "The sigil warmed under her palm as she spoke the old word."
- Analysis: ritual_incantation; climax 0.82.
- Decision: visual glow; no chime.
- Effects: visual_rune_glow_subtle(intensity=2).

8) War Historical – Whistle and Charge
- Text: "The whistle cut the fog, and they went over the top."
- Analysis: command; high event density.
- Decision: no haptic; soft whistle accent.
- Effects: sound_whistle_command_soft(volume=2); vignette_darken_slow.

9) Romance – Tender Kiss
- Text: "Their foreheads touched, and the room exhaled."
- Analysis: low velocity; joy↑; complexity p33.
- Decision: warm color shift; no kinetics.
- Effects: color_temp_warm_slow(+10%); tonal_swell_faint.

10) Space Horror – Jump Scare (Rare)
- Text: "The duct above her flexed. Then it moved."
- Analysis: jump_scare; climax 0.99; horror theme.
- Decision: single sting + haptic; enforce 3000w cooldown.
- Effects: sound_sting_soft(volume=3); haptic_pulse_sharp(3).

11) Legal Drama – Verdict Delivered
- Text: "We, the jury, find the defendant—guilty."
- Analysis: change_of_state; climax 0.94; token: "guilty".
- Decision: word_pulse("guilty"); no accents.
- Effects: kinetic_word_pulse.

12) Steampunk – Valve Turn
- Text: "She spun the brass valve and the pressure fell."
- Analysis: micro-action; theme_steampunk.
- Decision: valve audio; no visuals.
- Effects: sound_valve_turn(volume=2); steam_release_soft resumes.

---

### 9) Creator-Facing Playbook Templates

Provide human-readable presets creators can choose/tweak.

```yaml
preset: "Noir: Rainy Alley Interrogation"
theme: theme_noir_detective
mood_curve:
  - page: 1
    mood: suspense
    tier1: [vignette_darken_slow:3, soundscape_rain_city_night:2]
  - page: 3
    event: confession_difficult
    tier2: [sequential_reveal_slow:2]
  - page: 4
    event: sudden_shock_revelation
    tier2: [word_pulse:"betrayed"]
cooldowns:
  haptic_words: 1000
  accent_words: 250
forbidden:
  - sound_laser_blast
  - visual_magic_sparkle
```

```yaml
preset: "Epic Fantasy: Ritual at Dusk"
theme: theme_dark_fantasy
tier1: [forest_ambience:2, vignette_darken_slow:2, color_ash_grey:1]
events:
  - ritual_incantation: [visual_rune_glow_subtle:2]
  - sudden_shock_revelation: [word_pulse:"blood"]
```

---

### 10) Dataset Construction Guidelines

- Unit: JSONL per paragraph/scene with gold labels (selected_effects + rationale).
- Balance: Ensure event diversity; limit jump_scare to <0.5% of samples.
- Stratify: By theme, PAD region, complexity percentile.
- Augment: Paraphrase triggers; maintain labels.
- Validate: Human rater pass for diegesis and legibility.

---

### 11) Implementation Notes

- Deterministic pre-filters: theme → allowed/forbidden set; governor caps tier.
- Priority ordering: Climax > Emotional deviation > Narratology > Keyword.
- Audio loudness: LUFS targets −28 to −24 for ambiences; −20 max for accents.
- Typography shifts: keep within ±2% except for explicit presets.
- Accessibility: never impair contrast; adhere to WCAG AA minimums.

---

This guide is intended to be expanded continuously. Additions should include: new sub-palettes per theme, domain-specific micro-actions, and more worked examples keyed to real texts in your dataset.

---

### 12) Priority Expansions by Genre/Sub-Palette

The following sections deepen coverage for sci‑fi, romance/romantasy (micro-actions), medieval fantasy, comedy, horror, mystery, and suspense. Each includes sub-palettes, allowed/forbidden rules, micro-actions, and worked examples.

#### 12.1 Sci‑Fi Sub-Palettes

| palette_id | parent_theme | visual | audio | allowed_accents | forbidden | notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| palette_sci_fi_utopian_lab | theme_hard_sci_fi | texture_clean_gloss; font_sans_source; color_cool_white_high | lab_ventilation_even; soft_harp_tones | visual_grid_overlay_subtle; sound_autodoor_soft | visual_glitch_harsh; thunder_clap | sterile, calm precision; avoid fear cues |
| palette_sci_fi_dystopian_street | theme_sci_fi_cyberpunk | texture_digital_grit; font_sans_ocr; neon_green_tint | rain_neon_buzz; server_fan_whir | visual_scanline_pulse; sound_ui_beep_analog | magic_chime; horse_gallop | street-level grit; mild interference effects ok |
| palette_sci_fi_corporate_clean | theme_sci_fi_cyberpunk | texture_clean_glass; font_sans_helvetica; color_cool_cyan | hvac_even; elevator_ding_soft | sound_badge_reader_beep_soft | glitch/noise artifacts | corporate polish; suppress street grit |
| palette_space_opera_bridge | theme_sci_fi_space_opera | texture_clean_digital; font_sans_futura; color_cool_blue | engine_hum_low; bridge_chatter_faint | sound_airlock_seal; sound_console_tap_soft | thunder_clap; medieval_clinks | command environment; low arousal |
| palette_space_opera_outlands | theme_sci_fi_space_opera | texture_rust_steel; font_sans_agency; color_sodium_amber | generator_throb; crowd_murmur | sound_baton_crack_soft; door_hydraulic_soft | transporter_chime_utopian | rough frontier energy |
| palette_space_horror_derelict | theme_space_horror | texture_clean_dust; font_sans_univers; cold_steel_hue | air_duct_whisper; random_hull_knock | visual_breath_condense_subtle | cheerful_tonal_swell; ui_beeps | maximize dread; very sparse accents |
| palette_time_travel_lab | theme_time_travel_sf | texture_clean_grid; font_sans_eurostile; cool_cyan | oscillator_hum; relay_click | visual_scanline_sweep; sound_geiger_faint | magic_glow; thunder_clap | precision and paradox vibe |
| palette_time_travel_retro | theme_time_travel_sf | texture_paper_faded; font_sans_futura_classic; warm_sepia | tape_reel_soft; typewriter_distant | sound_camera_shutter_soft | neon_synth_ui | retro-futurism; respect era |

Sci‑Fi micro-actions (add to Section 6 registry):
- console_tap_soft: audio on "typed/entered"; vol 1–2
- autodoor_whoosh: audio on "door opened"; vol 1–2
- magnetic_boot_clink: audio on "stepped" (EVA); vol 1–2
- helmet_seal: audio on "sealed"; vol 2–3
- reactor_ramp: audio swell on "powered up"; vol +1 for 2s
- visor_fog_brief: visual 300ms on breath in cold compartments

Worked examples:
- Text: "Negative thrust. Re-vector to retrograde." → palette_space_opera_bridge; Tier 1 only; no accents.
- Text: "The badge reader chirped green." → sound_badge_reader_beep_soft (2); no kinetic.
- Text: "Her visor bloomed white with breath." → visual_breath_condense_subtle (1); suppress audio.

#### 12.2 Romance / Romantasy Micro-Actions

Principles: gentle, intimate, low arousal unless climax > 96%; avoid startling sounds/haptics; lean on warmth and pacing.

| action | accent_id | modality | timing | intensity | notes |
| :-- | :-- | :-- | :-- | :-- | :-- |
| fingertip_brush | sound_fabric_brush_soft | audio | on verb/noun | 1 | silk/linen rustle per theme |
| breath_hitch | sound_breath_hitch_soft | audio | on clause break | 1 | gate to climax>85% |
| heartbeat_sync | haptic_pulse_rhythmic_faint | haptic | sustained 2–4s | 1–2 | only if climax>96%; romance/romantasy only |
| jewelry_clink | sound_chain_clink_soft | audio | on noun | 1 | medieval/romantasy use metal type |
| fabric_sigh | sound_fabric_sigh_soft | audio | on sit/lean verbs | 1 | couches, beds |
| quill_scratch | sound_quill_scratch | audio | on writing | 1 | historical/romantasy |
| fireplace_settle | sound_fireplace_settle | audio | scene beat | 1 | room quiet moments |
| rain_on_window | sound_rain_tap_soft | audio | scene beat | 1 | moody intimacy |

Romance pacing kinetics:
- sequential_reveal_slow on confessions; align to commas; cap speed=2.
- soft_emphasis italics on internal monologue; warm tint +2%.

Worked examples:
- Text: "Her fingers grazed his sleeve." → sound_fabric_brush_soft (1).
- Text: "He exhaled, then smiled." → no accents; color_warm_slow (+8%).
- Text: "Our words tangled, then found their place." → sequential_reveal_slow (2).

#### 12.3 Medieval Fantasy (Distinct from Epic/Dark)

Sub-palettes:

| palette_id | parent_theme | visual | audio | allowed_accents | forbidden | notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| palette_medieval_court_day | theme_medieval_historical | parchment_clean; serif_uncial; candle_warm | hall_murmur_soft; quill_scratch | sound_ring_seal_wax; footstep_stone_soft | sci_fi_ui; thunder_clap_modern | courtly restraint |
| palette_medieval_tavern_night | theme_medieval_historical | parchment_smudge; serif_bembo; warm_amber | lute_soft; fire_crackle | sound_mug_setdown_wood; chair_scrape_soft | electric_hum | convivial but gentle |
| palette_medieval_forest_glade | theme_medieval_historical | vellum_light; serif_garamond; leaf_green_tint | brook_soft; birds | sound_bow_string_twang_soft | gun_cock_click | pastoral |
| palette_medieval_storm_keep | theme_medieval_historical | parchment_damp; serif_times; cool_slate | wind_through_arrowslits | visual_torch_sputter_subtle; thunder_clap_single (rare) | neon_synth | allow one controlled clap per 800w |

Micro-actions:
- chain_mail_rustle; leather_creak; hoof_clop_muffled; banner_flap; scabbard_tap; prayer_beads_click.

Worked examples:
- Text: "Mail whispered as they knelt." → chain_mail_rustle (1).
- Text: "The banner worried the wind." → banner_flap (1–2).

#### 12.4 Comedy (Romcom, Satire, Slapstick)

Principles: prioritize timing and typography over loud accents; avoid haptic; use light, diegetic sounds only.

Sub-palettes:

| palette_id | parent_theme | visual | audio | allowed_accents | forbidden | notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| palette_comedy_romcom_school | theme_high_school_romcom | clean_white; sans_roboto; friendly_warm | hallway_murmur; sneaker_squeak | sound_text_notification_subtle; locker_close_soft | haptic; horror_stings | playful, modern |
| palette_comedy_office_satire | theme_satire_modern | copy_paper; sans_futura; neutral | open_office_murmur | sound_email_ding_soft; chair_wheel_soft | thunder_clap; magic_chime | keep subtle |
| palette_comedy_slapstick_home | theme_contemporary_lit | clean_matte; serif_literata; bright | floor_creak_soft; kitchen_utensils | sound_pan_clink_soft; door_squeak_soft | cartoony_boings | keep diegetic; no cartoon SFX |

Kinetic timing:
- punctuation_bounce_micro on commas/ellipses; amplitude ≤0.2%.
- sequential_reveal_comedic beat alignment to punchline token.

Worked examples:
- Text: "...and then the cat sat on send." → sequential_reveal_comedic; sound_email_ding_soft (1).
- Text: "The chair protested his plan." → chair_wheel_soft (1).

#### 12.5 Horror (Gothic, Cosmic, Slasher, Folk, Psychological)

Principles: atmosphere over accents; extreme sparsity; enforce long cooldowns for stings and haptics.

Sub-palettes:

| palette_id | parent_theme | visual | audio | allowed_accents | forbidden | notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| palette_horror_gothic_candle | theme_gothic_horror | aged_foxing; serif_garamond; vignette_persistent | wind_howl_distant; house_settle | visual_candle_flicker_subtle; floorboard_creak | sci_fi_ui; cheerful_swell | slow dread |
| palette_horror_cosmic_void | theme_space_horror | cold_steel; sans_univers; desat | low_subsonic_drone | none (rare sting only) | heartbeat_haptic unless peak | silence is a tool |
| palette_horror_slasher_suburban | theme_psych_thriller | clean_digital; sans_helvetica; cool | fridge_hum; distant_dog | door_chain_rattle_soft | magic_chime | keep mundane, uncanny |
| palette_horror_folk_wood | theme_dark_fantasy | parchment_rough; serif_blackletter; ash | wind_dead_trees; rope_swing_creak | bone_chime_soft | sci_fi_ui | ritual dread |

High-risk accents (cap frequency):
- sound_sting_soft (≤1 per 3000w); haptic_pulse_sharp (≤1 per 1000w at climax>98%).

Micro-actions:
- wet_drip_soft, rope_creak_swing, window_latch_rattle, distant_child_laugh_faint (use with caution), mirror_hairline_crack_visual.

Worked examples:
- Text: "A drip counted the dark." → wet_drip_soft (1), no kinetic.
- Text: "The latch trembled, though no wind came." → window_latch_rattle (1), vignette_darken_slow.

#### 12.6 Mystery and Suspense

Principles: build curiosity and tension with Tier 1; limit accents to investigative diegetics; favor focus and pacing.

Sub-palettes:

| palette_id | parent_theme | visual | audio | allowed_accents | forbidden | notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| palette_mystery_cozy_bookshop | theme_cozy_mystery | paper_soft; serif_georgia; warm_pastel | fireplace_crackle; bell_door_soft | tea_cup_clink; page_turn_soft | thunder_clap; haptic | comfort first |
| palette_mystery_procedural_lab | theme_crime_procedural | copy_paper; sans_inter; cool_white | copier_whir; fluorescent_hum | evidence_bag_rustle; camera_shutter_soft | magic_glow | clinical focus |
| palette_suspense_rain_stakeout | theme_psych_thriller | clean_digital; sans_helvetica; cool_dark | rain_on_roof; wiper_squeak_soft | car_seat_creak_soft; phone_vibrate_table | loud_stings | slow-burn tension |
| palette_suspense_interrogation | theme_political_thriller | parchment_clean; sans_franklin; neutral | hvac_vent; clock_tick_soft | chair_scrape_soft | sword_clash | compress time with pacing |

Micro-actions:
- ziplock_seal_rustle, camera_shutter_soft, evidence_tag_snap, umbrella_shake_soft, seat_belt_click_soft, pen_click_soft (limit), recorder_beep_soft.

Kinetics:
- focus_vignette_micro during key observation lines; sequential_reveal_medium during hesitant statements.

Worked examples:
- Text: "Bag and tag, now." → evidence_bag_rustle (1), no kinetic.
- Text: "He stared too long at the umbrella stand." → focus_vignette_micro (1), rain_on_roof continues.

---

### 13) Detection Heuristics (Additions)

- Comedy punchline: clause-final token with sentiment flip or incongruent noun; enable sequential_reveal_comedic and punctuation_bounce_micro.
- Romantasy tenderness: proximity verbs (brush, graze, linger) + pronoun pairs; enable fabric/breath micro-accents; suppress haptic unless climax>96%.
- Space horror silence cue: ambient RMS falls below −40 dBFS for ≥2s; consider single soft sting within cooldown.
- Mystery focus: named entity (object) mentioned ≥3 times in page; allow focus_vignette_micro on mention 3.


