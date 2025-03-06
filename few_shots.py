import pandas as pd
import json


def load_posts(file_path="data/processed_posts.json"):
    """Load posts from a JSON file and preprocess them."""
    with open(file_path, encoding="utf-8") as f:
        posts = json.load(f)

    df = pd.json_normalize(posts)
    df['length'] = df['line_count'].apply(categorize_length)

    # Collect unique tags
    all_tags = df['tags'].explode().unique().tolist()

    return df, all_tags


def categorize_length(line_count):
    """Categorize post length based on line count."""
    if line_count < 5:
        return "Short"
    elif 5 <= line_count <= 10:
        return "Medium"
    else:
        return "Long"


def get_filtered_posts(df, length, language, tag):
    """Filter posts based on length, language, and tag."""
    df_filtered = df[
        (df['tags'].apply(lambda tags: tag in tags)) &
        (df['language'] == language) &
        (df['length'] == length)
    ]
    return df_filtered.to_dict(orient='records')


if __name__ == "__main__":
    df_posts, unique_tags = load_posts()
    print(df_posts.head())
    filtered_posts = get_filtered_posts(df_posts, "Medium", "English", "Influencer")

    print(f"Available tags: {unique_tags}")

    # print(f"Filtered Posts: {filtered_posts}")
    for i in filtered_posts:
        print(i)
        print("\n")
