import pandas as pd
from datetime import datetime

class NotinoTransformation:
    def __init__(self, country: str, retailer: str):
        self.country = country
        self.retailer = retailer

    def transform_data(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        transformed_df = raw_df.copy()

        # Add new columns
        transformed_df['country'] = self.country
        transformed_df['currency'] = 'CZK'  # Assuming Czech Koruna
        transformed_df['scraped_at'] = datetime.now()  # Current date and time

        # Convert columns to strings for cleaning
        transformed_df['price'] = transformed_df['price'].astype(str)
        transformed_df['price_after_sale'] = transformed_df['price_after_sale'].astype(str)

        # Clean and convert price columns to float
        transformed_df['price'] = transformed_df['price'].str.replace(' Kč', '').str.replace('\xa0', '').str.replace(',', '.').astype(float)
        transformed_df['price_after_sale'] = transformed_df['price_after_sale'].str.replace(' Kč', '').str.replace('\xa0', '').str.replace(',', '.').astype(float)

        # Calculate discount amount
        transformed_df['discount_amount'] = transformed_df['price'] - transformed_df['price_after_sale']

        return transformed_df

def main(raw_df: pd.DataFrame, country: str, retailer: str):
    transformation = NotinoTransformation(country=country, retailer=retailer)
    transformed_df = transformation.transform_data(raw_df)
    return transformed_df

if __name__ == "__main__":
    raw_df = pd.read_csv("notino_raw.csv")
    transformed_df = main(raw_df, country="cz", retailer="notino")
    transformed_df.to_csv("notino_transformed.csv", index=False)
