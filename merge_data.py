import pandas as pd
from textblob import TextBlob
from datetime import date

#test
yahoo = pd.read_csv(r'data\yahoo_data.csv')
print(yahoo.head(5))

cnbc = pd.read_csv(r'data\cnbc_data.csv')
print(cnbc.head(5))

world_gov = pd.read_csv(r'data\world_gov_data.csv')
print(world_gov.head(5))


# ── Add scrape date to world_gov and yahoo ────────────────────────────
today = str(date.today())
world_gov['Scrape_Date'] = today
yahoo['Scrape_Date'] = today

# ── Clean the Yield column — remove % sign for analysis ──────────
world_gov['Yield'] = world_gov['Yield'].str.replace('%', '').str.strip()

# ── Clean percentage change — remove % sign ───────────────────────
yahoo['Percentage_Change'] = yahoo['Percentage_Change'].str.replace('%', '').str.strip()

# ── Add sentiment column to CNBC headlines ────────────────────────
def get_sentiment(headline):
    polarity = TextBlob(headline).sentiment.polarity
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

cnbc['Sentiment'] = cnbc['Headline'].apply(get_sentiment)

# ── Preview cleaned datasets ──────────────────────────────────────
print("CNBC with sentiment:")
print(cnbc[['Headline', 'Sentiment']].head(5))
print()

print("world_gov cleaned:")
print(world_gov.head(3))
print()

print("Yahoo cleaned:")
print(yahoo.head(3))

# ── Save all three cleaned datasets ──────────────────────────────
cnbc.to_csv('data/cnbc_clean.csv', index=False)
world_gov.to_csv('data/world_gov_clean.csv', index=False)
yahoo.to_csv('data/yahoo_clean.csv', index=False)

print("\nAll three cleaned datasets saved.")