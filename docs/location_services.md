# Location Services

## Overview

Location services provide city, zone, and area information needed for store creation and order delivery.

## Get Cities

```python
from pathao import PathaoClient

client = PathaoClient(environment="sandbox")

# Get all cities
cities = client.locations.get_cities()

print(f"Available cities: {len(cities.data)}")
for city in cities.data:
    print(f"- {city.city_name} (ID: {city.city_id})")
```

## Get Zones

```python
# Get zones for a specific city
dhaka_city_id = 1
zones = client.locations.get_zones(dhaka_city_id)

print(f"Zones in Dhaka: {len(zones.data)}")
for zone in zones.data:
    print(f"- {zone.zone_name} (ID: {zone.zone_id})")
```

## Get Areas

```python
# Get areas for a specific zone
dhanmondi_zone_id = 1
areas = client.locations.get_areas(dhanmondi_zone_id)

print(f"Areas in Dhanmondi: {len(areas.data)}")
for area in areas.data:
    print(f"- {area.area_name} (ID: {area.area_id})")
    print(f"  Home delivery: {area.home_delivery_available}")
    print(f"  Pickup: {area.pickup_available}")
```

## Find City by Name

```python
# Search for city by name (case-insensitive)
city = client.locations.get_city_by_name("dhaka")
if city:
    print(f"Found: {city.city_name} (ID: {city.city_id})")
else:
    print("City not found")
```

## Location Models

```python
@dataclass
class City:
    city_id: int
    city_name: str

@dataclass
class Zone:
    zone_id: int
    zone_name: str

@dataclass
class Area:
    area_id: int
    area_name: str
    home_delivery_available: bool
    pickup_available: bool
```

## Location Hierarchy

The location system follows this hierarchy:
1. **City** (e.g., Dhaka, Chittagong)
2. **Zone** (e.g., Dhanmondi, Gulshan)
3. **Area** (e.g., Dhanmondi 27, Gulshan 1)

## Error Handling

```python
from pathao import NotFoundError

try:
    zones = client.locations.get_zones(999999)  # Invalid city ID
except NotFoundError as e:
    print(f"City not found: {e}")

try:
    areas = client.locations.get_areas(999999)  # Invalid zone ID
except NotFoundError as e:
    print(f"Zone not found: {e}")
```

## Complete Location Workflow

```python
from pathao import PathaoClient, NotFoundError

def explore_locations(client):
    """Explore the complete location hierarchy."""
    try:
        # Get all cities
        cities = client.locations.get_cities()
        print(f"📍 Found {len(cities.data)} cities")

        # Focus on Dhaka
        dhaka = client.locations.get_city_by_name("dhaka")
        if not dhaka:
            print("❌ Dhaka not found")
            return

        print(f"\n🏙️  Exploring {dhaka.city_name}")

        # Get zones in Dhaka
        zones = client.locations.get_zones(dhaka.city_id)
        print(f"📍 Found {len(zones.data)} zones in Dhaka")

        # Explore first few zones
        for zone in zones.data[:3]:
            print(f"\n🏘️  Zone: {zone.zone_name}")

            try:
                areas = client.locations.get_areas(zone.zone_id)
                print(f"   📍 {len(areas.data)} areas")

                # Show first few areas
                for area in areas.data[:3]:
                    delivery_info = []
                    if area.home_delivery_available:
                        delivery_info.append("Home Delivery")
                    if area.pickup_available:
                        delivery_info.append("Pickup")

                    services = ", ".join(delivery_info) if delivery_info else "No services"
                    print(f"     - {area.area_name} ({services})")

            except NotFoundError:
                print(f"     ❌ No areas found for {zone.zone_name}")

    except Exception as e:
        print(f"❌ Error exploring locations: {e}")

def get_location_ids(client, city_name="dhaka"):
    """Get location IDs for store/order creation."""
    try:
        # Find city
        city = client.locations.get_city_by_name(city_name)
        if not city:
            return None, None, None

        # Get first zone
        zones = client.locations.get_zones(city.city_id)
        if not zones.data:
            return city.city_id, None, None

        zone = zones.data[0]

        # Get first area
        areas = client.locations.get_areas(zone.zone_id)
        if not areas.data:
            return city.city_id, zone.zone_id, None

        area = areas.data[0]

        return city.city_id, zone.zone_id, area.area_id

    except Exception as e:
        print(f"❌ Error getting location IDs: {e}")
        return None, None, None

# Usage
client = PathaoClient(environment="sandbox")

# Explore locations
explore_locations(client)

# Get IDs for store creation
city_id, zone_id, area_id = get_location_ids(client)
if all([city_id, zone_id, area_id]):
    print(f"\n Location IDs - City: {city_id}, Zone: {zone_id}, Area: {area_id}")
```

## Best Practices

1. **Cache Location Data**: Location data doesn't change frequently, consider caching
2. **Validate Service Availability**: Check `home_delivery_available` and `pickup_available`
3. **Handle Missing Areas**: Some zones might not have areas defined
4. **Use City Search**: Use `get_city_by_name()` for user-friendly city selection
5. **Error Handling**: Always handle `NotFoundError` for invalid IDs
