
### Code for the problem
Importing `datetime` library to work with times


```python
import datetime as dt
```

Class *RoomInfo* stores information about each room like *floor number*, *room number*, *room capacity* and *available time slots*


```python
class RoomInfo:
  def __init__(self, roomFloor, roomNumber, roomCapacity, roomAvailability):
    self.floor = roomFloor
    self.number = int(roomNumber)
    self.capacity = int(roomCapacity)
    self.availability = roomAvailability
```

Opened the `rooms.txt` file and parsed to be able to be able to work on


```python
rooms = []
file = open("rooms.txt","r")
for line in file: 
    line = line.rstrip()
    roomDetails = line.split(",")
    roomsAvailabilities = roomDetails[2:]
    i = 0
    roomsAvailabilitiesSets=[]
    while i < len(roomsAvailabilities):
        roomsAvailabilitiesSets.append( [dt.datetime.strptime(roomsAvailabilities[i],'%H:%M'), dt.datetime.strptime(roomsAvailabilities[i+1],'%H:%M')])
        i = i+2
    room = RoomInfo(roomDetails[0].split(".")[0], roomDetails[0].split(".")[1],roomDetails[1],roomsAvailabilitiesSets)
    rooms.append(room)
```

Defined a function `CheckAvailability` that takes in *floor*, *number*, *start time*, *end time* as inputs. This function checks for the available rooms that can host the required number of people at the specified meeting time range. If the conditions are satisfied, it calls the function `getBestFloorAvailability` which checks for the best room available based on the floor the team is located. If the conditions are not met, it calls the function `getBestMeetingAvailability` which returns the most suitable rooms matching the team size and the meeting time ranges.


```python
def checkAvailability(floor,numberOfPeople,startTime,endTime):
    PossibleRooms = []
    startTime = dt.datetime.strptime(startTime,'%H:%M')
    endTime = dt.datetime.strptime(endTime,'%H:%M')
    for eachRoom in rooms:
        if eachRoom.capacity >= numberOfPeople:
            for eachRoomAvailability in eachRoom.availability:
                if startTime >=  eachRoomAvailability[0] and endTime <= eachRoomAvailability[1]:
                    PossibleRooms.append ([int(eachRoom.floor), eachRoom.number])
    if len(PossibleRooms) == 0:
        getBestMeetingAvailability(floor,numberOfPeople,startTime,endTime)
    else:
        return getBestFloorAvailability (PossibleRooms, floor)
```

Defined a function `getBestMeetingAvailability` that takes in *floor*, *number*, *start time*, *end time* as inputs from `checkAvailability` function and returns best available floor, room number and time slots 


```python
def getBestMeetingAvailability(floor,numberOfPeople,startTime,endTime):
    meetingDuration = endTime-startTime
    remainingDuration = dt.timedelta(seconds=0)
    availableSlots = []
    for eachRoom in rooms:
        if eachRoom.capacity >= numberOfPeople:
            for eachRoomAvailability in eachRoom.availability:
                    roomFloor = float('{}.{}'.format(eachRoom.floor, eachRoom.number))
                    availableSlots.append({'floor_room':roomFloor, 'time_slots':eachRoomAvailability})
    availableSlots.sort(key = lambda i: (i['time_slots'][0]))
    meetingSlot= startTime
    print('Best Possible Meeting room and time slots available: ')
    for slots in availableSlots:
        slotStart = slots['time_slots'][0]
        slotEnd = slots['time_slots'][1]
        availableTime = slotEnd - slotStart
        if slotStart >= meetingSlot and slotEnd <= endTime:
            if remainingDuration < meetingDuration and availableTime > dt.timedelta(minutes=30):
                remainingDuration += availableTime
                meetingSlot = slotEnd
                print('{}, Slot start: {}, Slot end: {}'.format(slots['floor_room'],slotStart.strftime('%I:%M'),slotEnd.strftime('%I:%M')))
```

Defined a function `getBestFloorAvailability` that takes in *floor*, *PossibleRooms* as inputs from `checkAvailability` function to determine the best room available at the chosen time on the floor that is closest to where the team works.


```python
def getBestFloorAvailability(PossibleRooms, floor):
    matchedDiff = []
    for matchedRoom in PossibleRooms:
        matchedDiff.append({"diff" : abs(matchedRoom[0] - floor), "fn":str(matchedRoom[0]) +"."+ str(matchedRoom[1])})
    leastAbsDifference = [matchedDiff[0]["diff"], matchedDiff[0]["fn"]]
    for matchedDif in matchedDiff:
        if matchedDif["diff"] <= leastAbsDifference[0]:
            leastAbsDifference = [matchedDif["diff"], matchedDif["fn"]]
    print(leastAbsDifference[1])

```

### Test cases



```python
checkAvailability(5,8,'10:30','11:30')
```

    9.547
    


```python
checkAvailability(8,4,'10:30','11:00')
```

    8.23
    


```python
checkAvailability(9,8,'10:30','11:00')
```

    9.547
    


```python
checkAvailability(8,4,'9:30','15:00')
```

    Best Possible Meeting room and time slots available: 
    9.511, Slot start: 09:30, Slot end: 10:30
    9.547, Slot start: 10:30, Slot end: 11:30
    8.43, Slot start: 11:30, Slot end: 12:30
    8.23, Slot start: 02:00, Slot end: 03:00
    


```python
checkAvailability(8,8,'10:00','12:00')
```

    Best Possible Meeting room and time slots available: 
    9.547, Slot start: 10:30, Slot end: 11:30
    
