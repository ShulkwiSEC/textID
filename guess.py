import sys
from engine import StylometryEngine

def run_analysis(text):
    """
    Identifies the author of the provided text by comparing it against 
    the registered fingerprints in the data directory.
    """
    engine = StylometryEngine()
    results = engine.predict(text)
    
    if not results:
        print("[!] No results found. Ensure 'data/' contains suspect samples.")
        return

    print(f"\n{'SUSPECT':<15} | {'MATCH CONFIDENCE':<10}")
    print("-" * 35)
    for name, score in results:
        bar = "█" * int(score * 20)
        print(f"{name:<15} | {score*100:>12.2f}% {bar}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_analysis(sys.argv[1])
    else:
        print("Usage: python guess.py \"your text here\"")
