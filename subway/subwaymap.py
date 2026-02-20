import gtfs_realtime_pb2
import gtfs_realtime_NYCT_pb2
import datetime
from zoneinfo import ZoneInfo
from displaytext import display_static_message
from displaytext import clear_lcd
from displaytext import init_lcd
from gpiozero import LED
from displayled import init_leds
from displayled import turn_on_led
from displayled import clear_leds


led1 = LED(17)
led2 = LED(27)
led3 = LED(22)

allLeds = [led1.pin.number, led2.pin.number, led3.pin.number]

stop_42nd_S = "631S"
stop_59th_S = "629S"
stop_88th_S = "626S"

stop_5Av_N = "R13N"
stop_59th_N = "R11N"
stop_queensboro_N = "R09N"

all_stops = [stop_42nd_S, stop_59th_S, stop_88th_S, stop_5Av_N, stop_59th_N, stop_queensboro_N]
my_stops = [stop_59th_S, stop_59th_N]

stop_to_led_map = {
    stop_42nd_S: led3.pin.number,
    stop_59th_S: led2.pin.number,
    stop_88th_S: led1.pin.number
}

direction_text_map = {'S': "Downtown", 'N': "Queens"}

subway_endpoint_1234567S = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"
subway_endpoint_NRWQ = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"

import requests
import time

def get_subway_data(endpoint):
    """Fetch data from the subway endpoint."""
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise error for bad status
        return response.content  # For GTFS feeds, use .content (not .json())
    except Exception as e:
        print(f"Failed to fetch subway data: {e}")
        return None

def parse_gtfs(data):
    """Parse GTFS-realtime protobuf data and print sorted list of (route id, direction, minutes until arrival) for each trip update at Lexington Av/59 St (629S)."""
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)
    
    arrivals = []
    current_stops = []

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip = entity.trip_update.trip
            route_id = trip.route_id
            for stu in entity.trip_update.stop_time_update:
                arrival = stu.arrival.time if stu.HasField('arrival') else None
                direction = stu.stop_id[-1]
               
                if arrival:
                    now = datetime.datetime.now(datetime.timezone.utc)
                    arrival_dt = datetime.datetime.fromtimestamp(arrival, tz=datetime.timezone.utc)
                    minutes_until_arrival = int((arrival_dt - now).total_seconds() // 60)
                   
                    if stu.stop_id in my_stops and minutes_until_arrival > 0:
                        arrivals.append((route_id, direction, stu.stop_id, minutes_until_arrival))
                    
                    elif minutes_until_arrival == 0 and stu.stop_id in all_stops:
                        current_stops.append(stu.stop_id)
                
    print("currentStops", current_stops)

    clear_leds(allLeds)
    for stop in current_stops:
        if stop == stop_42nd_S:
            turn_on_led(led3.pin.number)
        elif stop == stop_59th_S:
            turn_on_led(led2.pin.number)
        elif stop == stop_88th_S:
            turn_on_led(led1.pin.number)

    arrivals.sort(key=lambda x: x[3])
    for idx, (route_id, direction, stop_id, minutes) in enumerate(arrivals[:4]):
        clear_lcd()
        direction = direction_text_map.get(direction, 'N/A')
        message1 = f"{idx + 1}. ({route_id}) {direction}"
        message2 = f"{minutes} min"
        display_static_message(message1, message2)
        print(message1, message2)
        time.sleep(5)


def main():    
  
    init_leds(allLeds)
    init_lcd()

    try:
        while True:
            data = get_subway_data(subway_endpoint_1234567S)
            if data:
                parse_gtfs(data)
                time.sleep(5)
            data2 = get_subway_data(subway_endpoint_NRWQ)
            if data2:
                parse_gtfs(data2)
                time.sleep(5)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        clear_lcd()
        clear_leds(allLeds)

        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        clear_lcd()
        clear_leds(allLeds)

        return 1

if __name__ == "__main__":
    main()