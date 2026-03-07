import sys
from scraper import scrape_all_episodes
from generator import generate_addon_files


def main():
    print("Starting 40th PROJECT addon build...")

    try:
        episodes_by_series = scrape_all_episodes()

        total_episodes = sum(len(eps) for eps in episodes_by_series.values())
        if total_episodes == 0:
            print("ERROR: No episodes found")
            sys.exit(1)

        generate_addon_files(episodes_by_series)
        print(f"\nBuild complete! Total episodes: {total_episodes}")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
