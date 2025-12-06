#!/usr/bin/env python3
"""
ICT Wisdom Extractor for God Mode Indicator
Extracts all ICT trading rules from The Cortex for automated indicator logic.
"""

import json
import os
from openai import OpenAI
from supabase import create_client

# =============================================================================
# CONFIGURATION
# =============================================================================
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# =============================================================================
# COMPREHENSIVE ICT CONCEPTS (40+ queries for God Mode)
# =============================================================================
ICT_QUERIES = [
    # === POWER OF THREE / AMD ===
    ("po3_overview", "power of three AMD accumulation manipulation distribution"),
    ("po3_accumulation", "accumulation phase asian session range midnight open"),
    ("po3_manipulation", "manipulation phase judas swing false move liquidity grab stop hunt"),
    ("po3_distribution", "distribution phase expansion real move true direction"),
    ("po3_timing", "power of three timing when accumulation ends manipulation starts"),

    # === 2022 MODEL ===
    ("model_2022_overview", "2022 model entry rules complete sequence"),
    ("model_2022_steps", "2022 model step by step liquidity sweep MSS FVG"),
    ("model_2022_entry", "2022 model entry fair value gap order block"),
    ("model_2022_confirmation", "2022 model confirmation displacement candle"),

    # === SILVER BULLET ===
    ("silver_bullet_overview", "silver bullet model complete rules"),
    ("silver_bullet_time", "silver bullet time window 10am 11am 2pm 3pm new york"),
    ("silver_bullet_entry", "silver bullet entry fair value gap formation"),
    ("silver_bullet_target", "silver bullet target profit taking"),

    # === DRAW ON LIQUIDITY ===
    ("dol_overview", "draw on liquidity where price goes next"),
    ("dol_determining", "how to determine draw on liquidity"),
    ("dol_external", "external range liquidity buy stops sell stops"),
    ("dol_internal", "internal range liquidity fair value gap"),
    ("dol_priority", "liquidity priority which target first"),

    # === ORDER BLOCKS ===
    ("ob_definition", "order block definition what makes valid"),
    ("ob_rules", "order block rules requirements displacement"),
    ("ob_entry", "order block entry how to trade"),
    ("ob_mitigation", "order block mitigation what happens when touched"),
    ("ob_breaker", "order block becomes breaker when violated"),

    # === FAIR VALUE GAPS ===
    ("fvg_definition", "fair value gap definition imbalance"),
    ("fvg_valid", "fair value gap valid requirements"),
    ("fvg_entry", "fair value gap entry consequent encroachment"),
    ("fvg_ce", "consequent encroachment 50% of FVG"),
    ("ifvg", "inversion fair value gap IFVG when FVG fails"),

    # === MARKET STRUCTURE ===
    ("structure_bullish", "bullish market structure higher highs higher lows"),
    ("structure_bearish", "bearish market structure lower highs lower lows"),
    ("mss", "market structure shift MSS rules confirmation"),
    ("choch", "change of character ChoCH reversal signal"),
    ("bos", "break of structure BOS continuation"),
    ("displacement", "displacement requirements strong candle institutional"),

    # === LIQUIDITY CONCEPTS ===
    ("liquidity_pools", "liquidity pools where stops rest"),
    ("equal_highs", "equal highs EQH liquidity resting above"),
    ("equal_lows", "equal lows EQL liquidity resting below"),
    ("liquidity_sweep", "liquidity sweep stop hunt reversal"),
    ("liquidity_void", "liquidity void volume imbalance"),

    # === TIME AND SESSIONS ===
    ("killzone_london", "london killzone time rules"),
    ("killzone_ny", "new york killzone time rules"),
    ("macro_time", "macro time 50 past 10 after hour"),
    ("asian_session", "asian session range importance"),
    ("true_day_open", "true day open 9:30 importance"),
    ("midnight_open", "midnight open new york time"),

    # === PREMIUM DISCOUNT ===
    ("premium_discount", "premium discount equilibrium 50%"),
    ("ote_zone", "optimal trade entry zone 62% 79% fibonacci"),
    ("discount_array", "discount array buy in discount"),
    ("premium_array", "premium array sell in premium"),

    # === SPECIFIC SETUPS ===
    ("turtle_soup", "turtle soup false breakout reversal"),
    ("judas_swing", "judas swing false move london new york"),
    ("breaker_block", "breaker block failed swing"),
    ("mitigation_block", "mitigation block retest"),
    ("rejection_block", "rejection block wick"),
    ("propulsion_block", "propulsion block continuation"),

    # === CBDR & NWOG ===
    ("cbdr", "CBDR central bank dealer range 2pm 8pm"),
    ("nwog", "NWOG new week opening gap sunday"),

    # === WEEKLY PROFILE ===
    ("weekly_profile", "weekly profile which day high low"),
    ("day_of_week", "day of week monday tuesday wednesday thursday friday"),
    ("weekly_range", "weekly range expansion contraction"),

    # === BIAS & DIRECTION ===
    ("daily_bias", "daily bias determination how to know"),
    ("htf_ltf", "higher timeframe lower timeframe alignment"),
    ("bias_confirmation", "bias confirmation what confirms direction"),
    ("bias_invalidation", "bias invalidation when to flip"),

    # === RISK & TARGETS ===
    ("stop_loss", "stop loss placement where"),
    ("take_profit", "take profit targets liquidity"),
    ("risk_reward", "risk reward ratio minimum"),
    ("invalidation", "invalidation when trade is wrong"),

    # === INSTITUTIONAL BEHAVIOR ===
    ("smart_money", "smart money what institutions do"),
    ("accumulation_distribution", "accumulation distribution wyckoff"),
    ("manipulation", "manipulation how market makers trap"),
    ("algorithm", "algorithm how price delivered"),
]

# =============================================================================
# FUNCTIONS
# =============================================================================

def generate_embedding(client, text):
    """Generate embedding for semantic search."""
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def search_cortex(supabase, openai_client, query, num_results=10):
    """Semantic search in The Cortex."""
    embedding = generate_embedding(openai_client, query)

    response = supabase.rpc('search_ict_knowledge', {
        'query_embedding': embedding,
        'match_threshold': 0.30,
        'match_count': num_results
    }).execute()

    return response.data if response.data else []


def text_search(supabase, query, num_results=10):
    """Direct text search for exact phrases."""
    response = supabase.table('ict_chunks') \
        .select('content, source_transcript') \
        .ilike('content', f'%{query}%') \
        .limit(num_results) \
        .execute()

    return response.data if response.data else []


def main():
    print("=" * 60)
    print("  ICT WISDOM EXTRACTOR FOR GOD MODE INDICATOR")
    print("=" * 60)

    # Validate environment
    if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY]):
        raise ValueError("Missing required environment variables")

    # Initialize clients
    print("\n🔌 Connecting to The Cortex...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    # Verify connection
    stats = supabase.table('ict_chunks').select('id', count='exact').execute()
    total_chunks = stats.count or 0
    print(f"✅ Connected! Total chunks in Cortex: {total_chunks}")

    # Extract all ICT wisdom
    wisdom = {}
    total_queries = len(ICT_QUERIES)

    print(f"\n📚 Extracting {total_queries} ICT concepts...\n")

    for i, (concept_key, query) in enumerate(ICT_QUERIES, 1):
        print(f"  [{i}/{total_queries}] {concept_key}...")

        try:
            # Semantic search
            results = search_cortex(supabase, openai_client, query, num_results=8)

            # Also try text search for key terms
            key_term = query.split()[0]
            text_results = text_search(supabase, key_term, num_results=3)

            wisdom[concept_key] = {
                "query": query,
                "semantic_results": [
                    {
                        "content": r.get("content", ""),
                        "source": r.get("source_transcript", ""),
                        "similarity": round(r.get("similarity", 0), 4)
                    }
                    for r in results
                ],
                "text_results": [
                    {
                        "content": r.get("content", ""),
                        "source": r.get("source_transcript", "")
                    }
                    for r in text_results
                ]
            }

        except Exception as e:
            print(f"      ⚠️ Error: {e}")
            wisdom[concept_key] = {"query": query, "error": str(e)}

    # Get unique sources
    print("\n📋 Getting source list...")
    sources_resp = supabase.table('ict_chunks') \
        .select('source_transcript') \
        .limit(5000) \
        .execute()

    unique_sources = list(set([s['source_transcript'] for s in sources_resp.data]))
    unique_sources.sort()

    # Compile final output
    output = {
        "metadata": {
            "total_chunks": total_chunks,
            "total_sources": len(unique_sources),
            "concepts_extracted": len(wisdom),
            "extraction_version": "1.0"
        },
        "sources": unique_sources,
        "wisdom": wisdom
    }

    # Save to file
    output_file = "ict_wisdom.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ EXTRACTION COMPLETE!")
    print(f"   📁 Saved to: {output_file}")
    print(f"   📊 Total concepts: {len(wisdom)}")
    print(f"   📚 Total sources: {len(unique_sources)}")


if __name__ == "__main__":
    main()
