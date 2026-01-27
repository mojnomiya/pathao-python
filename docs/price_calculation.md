# Price Calculation

## Overview

Calculate delivery prices before creating orders to show customers accurate pricing.

## Basic Price Calculation

```python
from pathao import PathaoClient

client = PathaoClient(environment="sandbox")

# Calculate delivery price
price = client.prices.calculate(
    store_id=123,
    delivery_type=48,      # Normal delivery
    item_type=2,           # Parcel
    item_weight=1.0,       # kg
    recipient_city=1,      # Dhaka
    recipient_zone=1       # Dhanmondi
)

print(f"Base price: ৳{price.price}")
print(f"Discount: ৳{price.discount}")
print(f"Final price: ৳{price.final_price}")
print(f"COD available: {price.cod_enabled}")
if price.cod_enabled:
    print(f"COD fee: {price.cod_percentage}%")
```

## Price Comparison

```python
def compare_delivery_options(client, store_id, weight, city_id, zone_id):
    """Compare normal vs on-demand delivery pricing."""
    
    # Normal delivery (48 hours)
    normal_price = client.prices.calculate(
        store_id=store_id,
        delivery_type=48,
        item_type=2,
        item_weight=weight,
        recipient_city=city_id,
        recipient_zone=zone_id
    )
    
    # On-demand delivery (same day)
    ondemand_price = client.prices.calculate(
        store_id=store_id,
        delivery_type=12,
        item_type=2,
        item_weight=weight,
        recipient_city=city_id,
        recipient_zone=zone_id
    )
    
    print("📦 Delivery Options:")
    print(f"Normal (48h):   ৳{normal_price.final_price}")
    print(f"On-demand:      ৳{ondemand_price.final_price}")
    print(f"Difference:     ৳{ondemand_price.final_price - normal_price.final_price}")
    
    return normal_price, ondemand_price

# Usage
stores = client.stores.list()
store_id = stores.data[0].store_id

normal, ondemand = compare_delivery_options(
    client, store_id, 1.5, 1, 1
)
```

## Weight-Based Pricing

```python
def calculate_weight_pricing(client, store_id, city_id, zone_id):
    """Show how weight affects pricing."""
    
    weights = [0.5, 1.0, 2.0, 5.0, 10.0]
    
    print("📊 Weight-based pricing:")
    for weight in weights:
        try:
            price = client.prices.calculate(
                store_id=store_id,
                delivery_type=48,
                item_type=2,
                item_weight=weight,
                recipient_city=city_id,
                recipient_zone=zone_id
            )
            print(f"{weight:4.1f}kg: ৳{price.final_price}")
        except Exception as e:
            print(f"{weight:4.1f}kg: Error - {e}")

# Usage
calculate_weight_pricing(client, store_id, 1, 1)
```

## Price Model

```python
@dataclass
class PriceDetails:
    price: float                # Base delivery price
    discount: float             # Applied discount
    promo_discount: float       # Promotional discount
    plan_id: int               # Pricing plan ID
    cod_enabled: bool          # COD availability
    cod_percentage: float      # COD fee percentage
    additional_charge: float   # Extra charges
    final_price: float         # Total price after discounts
```

## Parameters

### Delivery Types
- **12**: On-demand delivery (same day, premium)
- **48**: Normal delivery (within 48 hours, standard)

### Item Types
- **1**: Document (lighter items, lower price)
- **2**: Parcel (general items, standard price)

### Weight Limits
- **Minimum**: 0.5 kg
- **Maximum**: 10.0 kg

## Error Handling

```python
from pathao import ValidationError

try:
    price = client.prices.calculate(
        store_id=123,
        delivery_type=99,  # Invalid delivery type
        item_type=2,
        item_weight=1.0,
        recipient_city=1,
        recipient_zone=1
    )
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    price = client.prices.calculate(
        store_id=123,
        delivery_type=48,
        item_type=2,
        item_weight=15.0,  # Too heavy
        recipient_city=1,
        recipient_zone=1
    )
except ValidationError as e:
    print(f"Weight error: {e}")
```

## Complete Pricing Example

```python
from pathao import PathaoClient, ValidationError

def get_delivery_quote(client, store_id, weight, city_id, zone_id):
    """Get comprehensive delivery quote."""
    try:
        # Calculate for both delivery types
        options = {}
        
        for delivery_type, name in [(48, "Normal"), (12, "Express")]:
            try:
                price = client.prices.calculate(
                    store_id=store_id,
                    delivery_type=delivery_type,
                    item_type=2,  # Parcel
                    item_weight=weight,
                    recipient_city=city_id,
                    recipient_zone=zone_id
                )
                
                options[name] = {
                    "base_price": price.price,
                    "discount": price.discount,
                    "final_price": price.final_price,
                    "cod_available": price.cod_enabled,
                    "cod_fee": price.cod_percentage if price.cod_enabled else 0
                }
                
            except ValidationError as e:
                options[name] = {"error": str(e)}
        
        return options
        
    except Exception as e:
        return {"error": f"Failed to get quote: {e}"}

def display_quote(quote):
    """Display pricing quote in user-friendly format."""
    print("💰 Delivery Quote")
    print("=" * 40)
    
    for option, details in quote.items():
        if "error" in details:
            print(f"{option}: ❌ {details['error']}")
            continue
            
        print(f"\n📦 {option} Delivery:")
        print(f"   Base price: ৳{details['base_price']}")
        if details['discount'] > 0:
            print(f"   Discount:   -৳{details['discount']}")
        print(f"   Final price: ৳{details['final_price']}")
        
        if details['cod_available']:
            print(f"   💳 COD available ({details['cod_fee']}% fee)")
        else:
            print(f"   ❌ COD not available")

# Usage
client = PathaoClient(environment="sandbox")

# Get store and location data
stores = client.stores.list()
cities = client.locations.get_cities()
dhaka = next(c for c in cities.data if "dhaka" in c.city_name.lower())
zones = client.locations.get_zones(dhaka.city_id)

if stores.data and zones.data:
    quote = get_delivery_quote(
        client,
        store_id=stores.data[0].store_id,
        weight=2.0,
        city_id=dhaka.city_id,
        zone_id=zones.data[0].zone_id
    )
    
    display_quote(quote)
```

## Best Practices

1. **Show Multiple Options**: Always show both normal and express pricing
2. **Include COD Info**: Display COD availability and fees clearly
3. **Handle Weight Limits**: Validate weight before calculation
4. **Cache Pricing**: Consider caching prices for common routes
5. **Error Handling**: Always handle validation errors gracefully