import bge

def main():
    
    scene = bge.logic.getCurrentScene()
    objects = scene.objects
    print("Pisteesi: "+str(objects["PinsRoof"]["points"]))
    
main()