from .sample_data import generate_crop_yield, generate_soil_health, generate_pest_records, generate_market_prices

def generate_all():
    return {
        "crop": generate_crop_yield(),
        "soil": generate_soil_health(),
        "pest": generate_pest_records(),
        "price": generate_market_prices(),
    }

