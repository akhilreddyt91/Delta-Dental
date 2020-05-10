import datetime as dt

class RoomInfo:
  def __init__(self, roomFloor, roomNumber, roomCapacity, roomAvailability):
    self.floor = roomFloor
    self.number = int(roomNumber)
    self.capacity = int(roomCapacity)
    self.availability = roomAvailability



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
    print('Best Possible Meeting room and timing available: ')
    for slots in availableSlots:
        slotStart = slots['time_slots'][0]
        slotEnd = slots['time_slots'][1]
        availableTime = slotEnd - slotStart
        if slotStart >= meetingSlot and slotEnd <= endTime:
            if remainingDuration < meetingDuration and availableTime > dt.timedelta(minutes=30):
                remainingDuration += availableTime
                meetingSlot = slotEnd
                print('{}, Slot start: {}, Slot end: {}'.format(slots['floor_room'],slotStart.strftime('%I:%M'),slotEnd.strftime('%I:%M')))


def getBestFloorAvailability(PossibleRooms, floor):
    matchedDiff = []
    for matchedRoom in PossibleRooms:
        matchedDiff.append({"diff" : abs(matchedRoom[0] - floor), "fn":str(matchedRoom[0]) +"."+ str(matchedRoom[1])})
    leastAbsDifference = [matchedDiff[0]["diff"], matchedDiff[0]["fn"]]
    for matchedDif in matchedDiff:
        if matchedDif["diff"] <= leastAbsDifference[0]:
            leastAbsDifference = [matchedDif["diff"], matchedDif["fn"]]
    print(leastAbsDifference[1])


checkAvailability(5,8,'10:30','11:30')