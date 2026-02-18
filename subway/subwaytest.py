import gtfs_realtime_pb2
import gtfs_realtime_NYCT_pb2
import datetime
from zoneinfo import ZoneInfo
from displaytext import display_static_message
from displaytext import destroy

subway_endpoint = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"

import requests
import time

def get_subway_data():
    """Fetch data from the subway endpoint."""
    try:
        response = requests.get(subway_endpoint)
        response.raise_for_status()  # Raise error for bad status
        return response.content  # For GTFS feeds, use .content (not .json())
    except Exception as e:
        print(f"Failed to fetch subway data: {e}")
        return None

def parse_gtfs(data):
    """Parse GTFS-realtime protobuf data and print sorted list of (route id, direction, minutes until arrival) for each trip update at Lexington Av/59 St (629S)."""
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)
    direction_map = {1: 'N', 2: 'E', 3: 'S', 4: 'W'}
    arrivals = []
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip = entity.trip_update.trip
            route_id = trip.route_id
            nyct_trip = trip.Extensions[gtfs_realtime_NYCT_pb2.nyct_trip_descriptor]
            direction_val = nyct_trip.direction if nyct_trip.HasField('direction') else None
            direction = direction_map.get(direction_val, 'N/A')
            for stu in entity.trip_update.stop_time_update:
                if "629" in stu.stop_id:
                    arrival = stu.arrival.time if stu.HasField('arrival') else None
                    if arrival:
                        now = datetime.datetime.now(datetime.timezone.utc)
                        arrival_dt = datetime.datetime.fromtimestamp(arrival, tz=datetime.timezone.utc)
                        minutes_until_arrival = int((arrival_dt - now).total_seconds() // 60)
                        if minutes_until_arrival > 0:
                            arrivals.append((route_id, direction, stu.stop_id, minutes_until_arrival))
    arrivals.sort(key=lambda x: x[3])
    for route_id, direction, stop_id, minutes in arrivals[:6]:
        message1 = f"Line: {route_id}, Dir: {stop_id[-1]}"
        message2 = f"{minutes} min"
        display_static_message(message1, message2)
        print(message1, message2)
        time.sleep(1)
        destroy()


def main():    
    destroy()
    try:
        while True:
            data = get_subway_data()
            if data:
                parse_gtfs(data)
        return 0
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        destroy()
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        destroy()
        return 1

if __name__ == "__main__":
    main()