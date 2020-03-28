def total_sec(minutes):
    return minutes * 60

def step(time, num):
    return round(time/num, 0)

def time_format(sec, date, start_time):
    start_seconds = int(start_time[6:8])
    start_minutes = int(start_time[3:5])
    start_hours = int(start_time[0:2])
    time = start_seconds + start_minutes * 60 + start_hours * 3600 + sec
    seconds = time % 60
    minutes = time % 3600 // 60 
    hours = time // 3600
    time = "%(date)sT%(hours)02d:%(minutes)02d:%(seconds)02dZ" % {'date': date,'hours': hours, 'minutes': minutes, 'seconds': seconds}
    return "    <time>"+time+"</time>"
    
def count(request):
    track = open("track.gpx", "r")
    counter = 0
    for line in track:
        if request in line:
            counter += 1
    track.close()
    return counter

settings = open("settings.txt", "r")
res = open("res.gpx", "w")

params = [line for line in settings]

DATE = params[0][6:16]
START_TIME = params[1][12:20]
RUN_TIME = int(params[2][10:12])

res.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
res.write("<gpx creator=\"StravaGPX Android\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\" version=\"1.1\" xmlns=\"http://www.topografix.com/GPX/1/1\">\n")
res.write(" <metadata>\n")
res.write("  <time>" + DATE + "T" + START_TIME + "Z" + "</time>\n") #to done
res.write(" </metadata>\n")


time_step = step(total_sec(RUN_TIME), count('</trkpt>'))
time = 0

track = open("track.gpx", "r")

flag = False
for line in track:
    if "<trk>" in line:
        flag = True
    if flag == True:
        if "<ele>" in line:
            line = line + time_format(time, DATE, START_TIME) + "\n"
            time += time_step
        if "link href" in line:
            line = ""
        res.write(line)

settings.close()    
track.close()
res.close()
