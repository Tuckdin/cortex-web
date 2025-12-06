#!/usr/bin/env python3
"""
Full Cortex Extraction Script
Extracts ALL 20,829 chunks from The Cortex - the complete ICT knowledge base.
Organizes by source transcript for comprehensive coverage.
"""

import os
import json
from datetime import datetime
from supabase import create_client

# Environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Batch size for pagination (Supabase has row limits)
BATCH_SIZE = 1000


def fetch_all_chunks(supabase):
    """Fetch ALL chunks from the Cortex using pagination."""
    all_chunks = []
    offset = 0

    while True:
        print(f"  Fetching chunks {offset} to {offset + BATCH_SIZE}...")

        response = supabase.table('ict_chunks') \
            .select('*') \
            .range(offset, offset + BATCH_SIZE - 1) \
            .execute()

        if not response.data:
            break

        all_chunks.extend(response.data)

        if len(response.data) < BATCH_SIZE:
            break

        offset += BATCH_SIZE

    return all_chunks


def organize_by_source(chunks):
    """Organize chunks by their source transcript."""
    by_source = {}

    for chunk in chunks:
        source = chunk.get('source_transcript', 'unknown')

        if source not in by_source:
            by_source[source] = {
                'source': source,
                'chunks': [],
                'total_chunks': 0
            }

        by_source[source]['chunks'].append({
            'id': chunk.get('id'),
            'content': chunk.get('content'),
            'chunk_index': chunk.get('chunk_index')
        })
        by_source[source]['total_chunks'] += 1

    # Sort chunks within each source by chunk_index
    for source in by_source:
        by_source[source]['chunks'].sort(key=lambda x: x.get('chunk_index', 0) or 0)

    return by_source


def extract_ict_concepts(chunks):
    """Extract and categorize ICT concepts mentioned across all chunks."""
    concepts = {
        'power_of_three': [],
        'order_blocks': [],
        'fair_value_gaps': [],
        'liquidity': [],
        'market_structure': [],
        'optimal_trade_entry': [],
        'silver_bullet': [],
        'judas_swing': [],
        'turtle_soup': [],
        'breaker_blocks': [],
        'mitigation_blocks': [],
        'killzones': [],
        'asian_session': [],
        'london_session': [],
        'new_york_session': [],
        'midnight_open': [],
        'true_day': [],
        'weekly_profiles': [],
        'monthly_profiles': [],
        'quarterly_shifts': [],
        'institutional_order_flow': [],
        'smart_money': [],
        'displacement': [],
        'imbalance': [],
        'inefficiency': [],
        'premium_discount': [],
        'equilibrium': [],
        'swing_points': [],
        'pivot_points': [],
        'time_and_price': [],
        'fibonacci': [],
        'pd_arrays': [],
        'draw_on_liquidity': [],
        'raid': [],
        'stop_hunt': [],
        'manipulation': [],
        'accumulation': [],
        'distribution': [],
        'expansion': [],
        'retracement': [],
        'consolidation': [],
        'propulsion_block': [],
        'rejection_block': [],
        'volume_imbalance': [],
        'opening_range_gap': [],
        'new_week_opening_gap': [],
        'new_day_opening_gap': [],
        'consequent_encroachment': [],
        'model_2022': [],
        'unicorn_model': [],
        'ict_mentorship': [],
        'amd': [],
        'cbdr': [],
        'nwog': [],
        'ndog': [],
        'macro_time': [],
        'algorithmically_delivered': [],
        'seek_and_destroy': [],
        'standard_deviation': [],
    }

    # Keywords mapping for each concept
    keywords = {
        'power_of_three': ['power of three', 'po3', 'accumulation manipulation distribution'],
        'order_blocks': ['order block', 'bullish order block', 'bearish order block'],
        'fair_value_gaps': ['fair value gap', 'fvg', 'imbalance'],
        'liquidity': ['liquidity', 'buy side liquidity', 'sell side liquidity', 'bsl', 'ssl', 'equal highs', 'equal lows'],
        'market_structure': ['market structure', 'bos', 'break of structure', 'choch', 'change of character'],
        'optimal_trade_entry': ['optimal trade entry', 'ote', '.62', '.705', '.79'],
        'silver_bullet': ['silver bullet'],
        'judas_swing': ['judas swing', 'judas'],
        'turtle_soup': ['turtle soup'],
        'breaker_blocks': ['breaker block', 'breaker'],
        'mitigation_blocks': ['mitigation block', 'mitigation'],
        'killzones': ['killzone', 'kill zone'],
        'asian_session': ['asian session', 'asian range'],
        'london_session': ['london session', 'london open', 'london close'],
        'new_york_session': ['new york session', 'ny session', 'new york open'],
        'midnight_open': ['midnight open', 'midnight'],
        'true_day': ['true day'],
        'weekly_profiles': ['weekly profile', 'weekly range'],
        'monthly_profiles': ['monthly profile', 'monthly range'],
        'quarterly_shifts': ['quarterly shift'],
        'institutional_order_flow': ['institutional order flow', 'institutional'],
        'smart_money': ['smart money'],
        'displacement': ['displacement'],
        'imbalance': ['imbalance'],
        'inefficiency': ['inefficiency'],
        'premium_discount': ['premium', 'discount'],
        'equilibrium': ['equilibrium'],
        'swing_points': ['swing high', 'swing low'],
        'pivot_points': ['pivot'],
        'time_and_price': ['time and price'],
        'fibonacci': ['fibonacci', 'fib'],
        'pd_arrays': ['pd array'],
        'draw_on_liquidity': ['draw on liquidity', 'dol'],
        'raid': ['raid', 'liquidity raid'],
        'stop_hunt': ['stop hunt', 'stop run'],
        'manipulation': ['manipulation'],
        'accumulation': ['accumulation'],
        'distribution': ['distribution'],
        'expansion': ['expansion'],
        'retracement': ['retracement'],
        'consolidation': ['consolidation', 'range'],
        'propulsion_block': ['propulsion block'],
        'rejection_block': ['rejection block'],
        'volume_imbalance': ['volume imbalance'],
        'opening_range_gap': ['opening range gap'],
        'new_week_opening_gap': ['new week opening gap', 'nwog'],
        'new_day_opening_gap': ['new day opening gap', 'ndog'],
        'consequent_encroachment': ['consequent encroachment'],
        'model_2022': ['2022 model', 'model 2022'],
        'unicorn_model': ['unicorn'],
        'ict_mentorship': ['mentorship'],
        'amd': ['amd'],
        'cbdr': ['cbdr', 'central bank dealer range'],
        'nwog': ['nwog'],
        'ndog': ['ndog'],
        'macro_time': ['macro', ':50', ':10'],
        'algorithmically_delivered': ['algorithm', 'algorithmically'],
        'seek_and_destroy': ['seek and destroy'],
        'standard_deviation': ['standard deviation'],
    }

    for chunk in chunks:
        content = chunk.get('content', '').lower()
        source = chunk.get('source_transcript', 'unknown')

        for concept, kws in keywords.items():
            for kw in kws:
                if kw.lower() in content:
                    concepts[concept].append({
                        'source': source,
                        'chunk_id': chunk.get('id'),
                        'excerpt': chunk.get('content', '')[:500]
                    })
                    break

    # Remove duplicates and count
    concept_stats = {}
    for concept, matches in concepts.items():
        unique_sources = list(set([m['source'] for m in matches]))
        concept_stats[concept] = {
            'total_mentions': len(matches),
            'unique_sources': len(unique_sources),
            'sources': unique_sources[:20]  # Limit to first 20 sources
        }

    return concept_stats


def main():
    print("=" * 60)
    print("🧠 FULL CORTEX EXTRACTION")
    print("   The Complete ICT Knowledge Base")
    print("=" * 60)

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: Missing SUPABASE_URL or SUPABASE_KEY")
        return

    print("\n🔌 Connecting to The Cortex...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Get total count
    try:
        stats = supabase.table('ict_chunks').select('*', count='exact').limit(1).execute()
        total_chunks = stats.count if stats.count else 0
        print(f"✅ Connected! Total chunks in Cortex: {total_chunks:,}")
    except Exception as e:
        print(f"⚠️ Could not get exact count: {e}")
        total_chunks = 0

    # Fetch ALL chunks
    print("\n📥 Extracting ALL chunks from The Cortex...")
    all_chunks = fetch_all_chunks(supabase)
    print(f"✅ Extracted {len(all_chunks):,} chunks")

    # Organize by source
    print("\n📂 Organizing by source transcript...")
    by_source = organize_by_source(all_chunks)
    print(f"✅ Found {len(by_source)} unique sources/transcripts")

    # Extract concept statistics
    print("\n🔍 Analyzing ICT concepts across all chunks...")
    concept_stats = extract_ict_concepts(all_chunks)

    # Build final output
    output = {
        'extraction_info': {
            'timestamp': datetime.now().isoformat(),
            'total_chunks': len(all_chunks),
            'total_sources': len(by_source),
            'source': 'The Cortex - Complete ICT Knowledge Base'
        },
        'concept_analysis': concept_stats,
        'transcripts': by_source
    }

    # Save to file
    output_file = 'ict_wisdom.json'
    print(f"\n💾 Saving to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"✅ Saved! File size: {file_size:.2f} MB")

    # Print summary
    print("\n" + "=" * 60)
    print("📊 EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total chunks extracted: {len(all_chunks):,}")
    print(f"Total transcripts: {len(by_source)}")
    print(f"\nTop 10 transcripts by chunk count:")

    sorted_sources = sorted(by_source.items(), key=lambda x: x[1]['total_chunks'], reverse=True)
    for i, (source, data) in enumerate(sorted_sources[:10], 1):
        print(f"  {i}. {source}: {data['total_chunks']} chunks")

    print("\n🎯 Top ICT concepts by mentions:")
    sorted_concepts = sorted(concept_stats.items(), key=lambda x: x[1]['total_mentions'], reverse=True)
    for concept, stats in sorted_concepts[:15]:
        if stats['total_mentions'] > 0:
            print(f"  • {concept}: {stats['total_mentions']} mentions across {stats['unique_sources']} sources")

    print("\n" + "=" * 60)
    print("✅ FULL CORTEX EXTRACTION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
