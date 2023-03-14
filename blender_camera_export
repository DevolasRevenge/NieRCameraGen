import bpy

def print_list():
    
    # Get the selected object
    obj = bpy.context.object

    # Get the selected action
    action = obj.animation_data.action

    # Create an empty set to store the unique keyframe times
    keyframe_times = set()
    
    keyframe_data = {}
    basic_dict = {}

    # Loop through all the fcurves in the action
    for fcurve in action.fcurves:
        # Loop through all the keyframes in the fcurve
        for keyframe in fcurve.keyframe_points:
            # Add the keyframe time to the set of unique keyframe times
            keyframe_times.add(round(keyframe.co[0]))

    # Sort the set of unique keyframe times
    sorted_keyframe_times = sorted(keyframe_times)

    # Loop through the sorted keyframe times
    for time in sorted_keyframe_times:
        # Set the current frame to the keyframe time
        bpy.context.scene.frame_set(time)
        # Print the location and rotation of the object
        print("Time:", time)
        print("Location:", obj.location)
        print("Rotation in YXZ:", obj.rotation_euler)
        
        #store the location and rotation in a dictionary
        keyframe_data[time] = new_value = {
        "location": (obj.location),
        "rotation": (obj.rotation_euler)
        }
    
        
        basic_dict[time] = {
        "location": (keyframe_data[time]["location"].x, keyframe_data[time]["location"].y, keyframe_data[time]["location"].z),
        "rotation": (keyframe_data[time]["rotation"].x, keyframe_data[time]["rotation"].y, keyframe_data[time]["rotation"].z)
        }
        
        
        
        print(basic_dict)
        
        print("\n\n")
        
print_list()
