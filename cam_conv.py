import random
from keyframe_list import k_list
from target_keyframe_list import target_k_list

bind_var = ""
action_var = ""
ruby_var = ""

def hex_gen():
    hex_code = ''.join(random.choice('0123456789ABCDEF') for _ in range(8))
    hex_code = "0x" + hex_code
    return(hex_code)

def bind_generator(id, instance, type):
    global bind_var
    id_value = str(hex_gen())
    cam_name =  ("track" + str(instance) + "_" + type)   # ex. track1_init
    cam_id =  id    # ex. 0xcf856a5

    action = (f'''
    <value>
        <id>{id_value}</id>
        <name>{cam_name}</name>
        <value>
            <code str="hap::Action">0xa6aaf7a4</code>
            <value>{cam_id}</value>
        </value>
    </value>''')

    bind_var = bind_var + action

    return(cam_name)

def ruby_generator(cam_name, timeF, type):
    global ruby_var    

    if type == "init":
        action = (f'''
        self.enable(self.{cam_name}())
		self.wait(1)
		self.disable(self.{cam_name}())
        ''')
    elif type == "target":
        action = (f'''
		self.enable(self.{cam_name}())
		self.wait({timeF-1})
		self.disable(self.{cam_name}())
        ''')
    
    ruby_var = ruby_var + action

def camera_action_generator(cam_id, x_rotation, y_rotation_automata, x_location, y_location_automata, z_location_automata, z_rotation_automata, timeF,  x_location_tar, y_location_target, z_location_target, cam_name):
    global action_var

    cam_action = (f'''
    <action>
        <code str="CameraAction">0xad895807</code>
        <name eng="Camera parameter specification area {cam_name}">カメラパラメータ指定エリア</name>
        <id>{cam_id}</id>
        <attribute>0x2</attribute>
        <area>
            <size>0</size>
        </area>
        <upVecForce>0 1 0</upVecForce>
        <Rotation_X>{x_rotation}</Rotation_X>
        <Rotation_Y>{y_rotation_automata}</Rotation_Y>
        <Fovy>20</Fovy>
        <Distance>4</Distance>
        <pos>
            <position>{x_location} {y_location_automata} {z_location_automata}</position>
        </pos>
        <tar>
            <position>{x_location_tar} {y_location_target} {z_location_target}</position>
        </tar>
        <usePos>1</usePos>
        <useTarget>1</useTarget>
        <interRate>0.1</interRate>
        <overwrite>0</overwrite>
        <offset>0 0 0</offset>
        <disableBattle>0</disableBattle>
        <useLimit>0</useLimit>
        <limitTime>20</limitTime>
        <accType>0</accType>
        <playerStop>0</playerStop>
        <actionCamStop>0</actionCamStop>
        <rotateOnly>1</rotateOnly>
        <distanceOnly>1</distanceOnly>
        <disableCameraHit>1</disableCameraHit>
        <newInter>0</newInter>
        <endInter>-1</endInter>
        <endAccType>0</endAccType>
        <Rotation_Z>0</Rotation_Z>
        <noControlTarget>0</noControlTarget>
        <overwriteNormalInterRate>0</overwriteNormalInterRate>
        <normalInterRate>0.05</normalInterRate>
        <useMoveOffset_>0</useMoveOffset_>
        <moveOffsetScale_>10</moveOffsetScale_>
        <moveOffsetInterp_>0.05</moveOffsetInterp_>
        <moveOffsetInterpStop_>0.001</moveOffsetInterpStop_>
        <useHold>0</useHold>
        <holdDistanceX_>9.9</holdDistanceX_>
        <holdDistanceZ_>4</holdDistanceZ_>
        <useHandOffInterp_>0</useHandOffInterp_>
        <handOffInterpRate_>0.001</handOffInterpRate_>
        <fixHeightUse_>0</fixHeightUse_>
        <fixHeight_>0</fixHeight_>
        <playerForceIn_>0</playerForceIn_>
        <leavePlayer_>0</leavePlayer_>
        <playerTargetForceInUp_>0</playerTargetForceInUp_>
        <playerTargetForceInUpDist_>0</playerTargetForceInUpDist_>
        <interpTimeDistance_>-1</interpTimeDistance_>
        <interpTimeAngle_>-1</interpTimeAngle_>
        <interpTimeFov_>-1</interpTimeFov_>
        <interpTimePosition_>{timeF}</interpTimePosition_>
        <interpTimeTarget_>{timeF}</interpTimeTarget_>
        <interpTimeAccTypeDistance_>0</interpTimeAccTypeDistance_>
        <interpTimeAccTypeAngle_>0</interpTimeAccTypeAngle_>
        <interpTimeAccTypeFov_>0</interpTimeAccTypeFov_>
        <interpTimeAccTypePosition_>0</interpTimeAccTypePosition_>
        <interpTimeAccTypeTarget_>0</interpTimeAccTypeTarget_>
        <endInterpTimeDistance_>-1</endInterpTimeDistance_>
        <endInterpTimeAngle_>-1</endInterpTimeAngle_>
        <endInterpTimeFov_>-1</endInterpTimeFov_>
        <endInterpTimePosition_>-1</endInterpTimePosition_>
        <endInterpTimeTarget_>-1</endInterpTimeTarget_>
        <endInterpTimeAccTypeDistance_>0</endInterpTimeAccTypeDistance_>
        <endInterpTimeAccTypeAngle_>0</endInterpTimeAccTypeAngle_>
        <endInterpTimeAccTypeFov_>0</endInterpTimeAccTypeFov_>
        <endInterpTimeAccTypePosition_>0</endInterpTimeAccTypePosition_>
        <endInterpTimeAccTypeTarget_>0</endInterpTimeAccTypeTarget_>
        <forceInterTimer>0</forceInterTimer>
        <forceInterRate>0.1</forceInterRate>
    </action>''')

    action_var = action_var + cam_action

    


def file_writer():
    bind_file = open("name_binding.xml", "w")         
    bind_file.write(bind_var)
    bind_file.close()

    ruby_file = open("ruby_function.rb", "w")         
    ruby_file.write(ruby_var)
    ruby_file.close()

    # action_file = open("camera_actions.xml", "w")         
    # action_file.write(action_var)
    # action_file.close()

    with open('camera_actions.xml', 'w', encoding='utf-8') as f:
        f.write(action_var)
    f.close


def camera_action_iteration():
    type = "init"
    prevFrame = 0
    cam_id = 0

    instance = 1
    init_instance = 0
    target_instance = 0
    
    #iterates through the main_keyframes and the target keyframes
    for frame, target_frame in zip(k_list, target_k_list):

        cam_id = str(hex_gen())

        #print(k_list[frame])
        #print(round(k_list[frame]["location"][0], 3))

        #extract location from dic
        x_location = round(k_list[frame]["location"][0], 3)
        y_location = round(k_list[frame]["location"][1], 3)
        z_location = round(k_list[frame]["location"][2], 3)

        #extract rotation from dic
        x_rotation = round(k_list[frame]["rotation"][0], 3)
        y_rotation = round(k_list[frame]["rotation"][1], 3)
        z_rotation = round(k_list[frame]["rotation"][2], 3)

        #flip // invert values for automata's system
        y_rotation_automata = z_rotation
        z_rotation_automata = y_rotation

        #flip // invert values for automata's system
        y_location_automata = z_location
        z_location_automata = (y_location*-1)

        ##

        #extract TARGET location from dic
        x_location_tar = round(target_k_list[frame]["location"][0], 3)
        y_location_tar = round(target_k_list[frame]["location"][1], 3)
        z_location_tar = round(target_k_list[frame]["location"][2], 3)

        #flip // invert TARGET values for automata's system
        y_location_target = z_location_tar
        z_location_target = (y_location_tar*-1)

        if type == "init" or prevFrame == 0:
            timeF = 0
        elif type == "target":
            timeF = frame - prevFrame

        #change current frame to previous for next interation
        prevFrame = frame

        if init_instance == 1 and target_instance == 1:
            instance = instance + 1
            init_instance = 0
            target_instance = 0

        print(frame)

        #runs the bind generator and appends each action to it, as well as returning the generated cam_action name
        cam_name = bind_generator(cam_id, instance, type)

        ruby_generator(cam_name, timeF, type)

        camera_action_generator(cam_id, x_rotation, y_rotation_automata, x_location, y_location_automata, z_location_automata, z_rotation_automata, timeF, x_location_tar, y_location_target, z_location_target, cam_name)

        #switch type to the other
        if type == "target":
            target_instance = 1
            type = "init"
        elif type == "init":
            init_instance = 1
            type = "target"
    
    file_writer()





camera_action_iteration()

