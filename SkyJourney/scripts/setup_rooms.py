# scripts/setup_rooms.py
# Run inside PowerShell:
# python manage.py shell -c "exec(open('scripts/setup_rooms.py', encoding='utf-8').read())"

from hotels.models import Hotel, RoomType, Pricing, Room
from django.db import transaction
import random

print("🧹 Deleting all existing Room records...")
Room.objects.all().delete()

with transaction.atomic():
    # --- Room Types ---
    room_types_data = [
        ("Single", "A single room suitable for one person."),
        ("Double", "A room suitable for two people."),
        ("Deluxe", "A larger room with additional amenities."),
        ("Suite", "A luxurious suite with living area."),
    ]

    room_types = {}
    for name, desc in room_types_data:
        obj, created = RoomType.objects.get_or_create(name=name, defaults={"description": desc})
        room_types[name] = obj
        print(f"{'Created' if created else 'Exists'} RoomType: {name}")

    # --- Pricing per type/capacity ---
    pricing_config = {
        "Single": [(1, 1000)],
        "Double": [(2, 1800)],
        "Deluxe": [(2, 2500), (3, 3000)],
        "Suite": [(4, 4000)],
    }

    for rt_name, configs in pricing_config.items():
        for capacity, price in configs:
            rt = room_types[rt_name]
            obj, created = Pricing.objects.get_or_create(
                room_type=rt, capacity=capacity,
                defaults={"base_price": price}
            )
            print(f"{'Created' if created else 'Exists'} Pricing: {rt_name} (cap={capacity}) ₹{price}")

    # --- Generate 80 Rooms per Hotel ---
    hotels = Hotel.objects.all()
    if not hotels.exists():
        print("⚠️ No hotels found. Please create hotels first.")
    else:
        print(f"🏨 Found {hotels.count()} hotels. Creating 80 rooms per hotel...")

        for hotel in hotels:
            for i in range(1, 81):
                rt = random.choice(list(room_types.values()))
                # Choose a valid capacity that exists for this room type
                valid_pricing = Pricing.objects.filter(room_type=rt)
                if not valid_pricing.exists():
                    continue
                pricing = random.choice(valid_pricing)
                capacity = pricing.capacity

                room_number = f"{hotel.id}{i:03d}"  # e.g., 1001–1080

                Room.objects.create(
                    hotel=hotel,
                    room_type=rt,
                    room_number=room_number,
                    capacity=capacity,
                    status=random.choice(["available", "out_of_service"]),
                )
            print(f"✅ Created 80 rooms for {hotel.name}")

print("🎉 Room setup complete!")
