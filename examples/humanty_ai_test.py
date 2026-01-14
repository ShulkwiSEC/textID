# challange wallkthrough: https://shulkwisec.github.io/post/how-shulkwisec-build-an-engine-to-detect-ai-authorship-physics/

from engine import StylometryEngine
import time

# --- Evaluation Data ---
# These are the paragraphs add more samples/challanges as needed
# but check data/ and ensure the model has been trained.
tests = {
    "openai": [
        "War scars nations and souls alike, shattering lives in the name of power or fear. Amid chaos, humanity is tested, revealing cruelty and courage side by side. Its true cost is not victory or defeat, but the generations forever changed.",
        "A father is a quiet strength, guiding with patience, protecting without praise. Through sacrifice and love, he shapes lives not by what he says, but by what he does every day.",
        "A mother is endless love, gentle strength, and unwavering care, shaping hearts through kindness, sacrifice, and warmth."
    ],
    "gemini": [
        "War is a devastating collision of power that shatters lives and landscapes. Beyond the strategic maneuvers, it leaves a lasting legacy of grief and displacement. While it may be waged for ideals, the true cost is always paid in human suffering and the irreversible loss of peace.",
        "A father serves as a steady anchor, providing strength, guidance, and quiet sacrifices. He is a teacher of resilience and a protector of dreams. Through his presence, he builds a foundation of security, shaping a child's world with lessons that resonate long after they are first taught.",
        "A mother is a selfless source of unconditional love, providing warmth, wisdom, and a lifelong foundation of unwavering support."
    ]
}

def run_evaluation():
    engine = StylometryEngine()
    
    print("\n" + "="*70)
    print(" 🧪 AI MODEL DETECTION - EVALUATION SUITE ")
    print("="*70)
    
    # Render Table
    header = " {0:<12} | {1:<12} | {2:<12} | {3:<8} ".format("EXPECTED", "GUESSED", "CONFIDENCE", "STATUS")
    print(header)
    print("-" * 70)

    stats = {"total": 0, "correct": 0}
    start_time = time.time()

    for expected_author, samples in tests.items():
        for text in samples:
            stats["total"] += 1
            results = engine.predict(text)
            
            if results:
                top_guess, confidence = results[0]
                is_correct = top_guess.lower() == expected_author.lower()
                
                # Visual Status
                status = "[ OK ]" if is_correct else "[FAIL]"
                
                if is_correct:
                    stats["correct"] += 1
                
                print(" {0:<12} | {1:<12} | {2:>10.2f}% | {3:<8} ".format(
                    expected_author, top_guess, confidence*100, status
                ))
            else:
                print(" {0:<12} | {1:<12} | {2:>10.2f}% | {3:<8} ".format(expected_author, "---", 0, "[SKIP]"))

    end_time = time.time()
    accuracy = (stats["correct"] / stats["total"]) * 100 if stats["total"] > 0 else 0
    duration = (end_time - start_time) * 1000

    print("-" * 70)
    print(f" 📊 FINAL METRICS")
    print(f"    - Accuracy:  {accuracy:.2f}% ({stats['correct']}/{stats['total']} samples)")
    print(f"    - Latency:   {duration/stats['total']:.2f}ms per query")
    print(f"    - Throughput: {stats['total']/(duration/1000):.1f} queries/sec")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_evaluation()