# ###################################################
# This Script will hide and unhide the spawner cones
# Chris Sprance
# Entrada Interactive
# Miscreated
# ##################################################
import re
import os

import general


# function to get the list of current spawners
def get_spawners():
    # find out where were runing the editor from
    rundir = os.getcwd()
    # get a list of all the current spawners
    spawners = "\\GameSDK\\Objects\\spawners"
    spawnlist = os.listdir(rundir + spawners)
    spawnerlist = list()
    for x in spawnlist:
        if x.endswith(".cgf"):
            spawnerlist.append(x.replace(".cgf", ""))
    return spawnerlist


# clean objects list and returns a list of a list with name and model geometry used
def clean_objects(obj):
    # return list
    retList = list()
    for x in obj:
        # run through our objects and only return the brushes
        if general.get_object_type(x) == "Brush":
            objlist = list()
            # split the list by / and grab the last then split that by . and grab the first
            model = general.get_entity_param(x, "Geometry").split("/")[-1].split(".")[0]
            # add those to the retlist as a dictionary ('Name of Object': 'ModelGeo')
            objlist.append(model)
            objlist.append(x)
            retList.append(objlist)
            # send it all back
    return retList


# function to get selected objects in the layer
def get_selected_objects(selection):
    sel = selection
    objects = list()
    objects.extend(sel)
    for x in sel:
        # Go find it's children objects and add that to the return list
        objects.extend(find_child(x))
    return clean_objects(objects)


# This function goes through an objects and finds if it has child objects and return them in a list
def find_child(parent):
    # get the children object from the parent
    children = general.get_object_children(parent)
    # return our list of children
    return children


# function to get all the objects in the level into one list
def get_all_objects():
    # define our list of objects to search through
    objects = list()
    # get all the layers
    layers = general.get_all_layers()
    # for every layer get all the objects in it
    for x in layers:
        objects.extend(general.get_all_objects_of_layer(x))
        # send the compiled list back
    return clean_objects(objects)


# function to find out what selection to do
def get_objects():
    selection = general.get_names_of_selected_objects()
    # test if we have anything selected and warn the user about each operation
    if len(selection) == 1:
        return get_selected_objects(selection)
    elif len(selection) == 0:
        sure = general.message_box(
            "You have no objects selected which means you will be will hiding all. This will probably crash on islands. Are you sure?"
        )
        if sure:
            return get_all_objects()
    elif len(selection) > 15:
        sure = general.message_box(
            "You have a large number of items selected. This may crash, make sure you save first."
        )
        if sure:
            return get_selected_objects(selection)
    else:
        return get_selected_objects(selection)


# function to hide an object
def hide_object(obj):
    for x in obj:
        general.hide_object(x)
        # print "Hiding: "+x


# function to unhide an object
def unhide_object(obj):
    for x in obj:
        general.unhide_object(x)


if __name__ == "__main__":
    # get our spawners
    spawners = get_spawners()
    # get our objects
    objects = get_objects()
    # print objects
    # create our list to store the hide items in
    hidelist = list()
    # generate our hide lists by iterating through our objects and spawners
    for spawner in spawners:
        # create our regex string
        regex = re.escape(spawner)
        # loop through each object
        for obj in objects:
            # test and see if our regex matches
            if re.search(regex, obj[0]):
                hidelist.append(obj[1])
    # hide the objects
    hide_object(hidelist)
