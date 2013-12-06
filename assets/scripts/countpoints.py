import bge

def main():
    
    scene = bge.logic.getCurrentScene()
    objects = scene.objects
    points = 0
    
    for i in range (0, 10):
        if objects["Pin.00"+str(i)]["fallen"] and not objects["Pin.00"+str(i)]["hasbeencount"]:
            objects["Pin.00"+str(i)]["hasbeencount"] = True
            points += 1
        
    objects["PinsRoof"]["points"] += points
    
main()