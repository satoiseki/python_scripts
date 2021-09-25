import os

source_dir = "E:/temp_music/"
destination_dir = "E:/music/"

def simple_renamer(src_dir, dst_dir, name):
    # example input: "E:/folder/", "E:/another_folder/", "img"
    for count, filename in enumerate(os.listdir(src_dir)):
        file_type = os.path.splitext(filename)[1][1:]
        src = src_dir + filename
        dst = dst_dir + name + str(count) + "." + file_type
        
        os.rename(src, dst)

def adv_renamer(src_dir, dst_dir):
    adv_renamer(src_dir, dst_dir, ["amv", "gmv", "lmfao", "unknown", "visualization"])

def adv_renamer(src_dir, dst_dir, words):
    for count, filename in enumerate(os.listdir(src_dir)):
        file_name = os.path.splitext(filename)[0]
        file_type = os.path.splitext(filename)[1][1:]

        # all to lower case
        file_name = file_name.casefold()

        # delete consecutive words such as given as parameter
        for word in words:
            file_name = file_name.replace(word, "")

        # string into a list because string is ummutable
        file_name_list = list(file_name)
        
        # replace special chars, numbers, spaces etc. with _
        for i in range(len(file_name_list)):
            unicode = ord(file_name_list[i])
            if (unicode < 97 or unicode > 122):
                file_name_list[i] = '_'

        # reduce multiple _ to one
        curr_index = 0
        for i in range(len(file_name_list)-1):
            if file_name_list[curr_index] == '_' and file_name_list[curr_index+1] == '_':
                file_name_list.pop(curr_index+1)
                continue
            curr_index += 1

        # delete _ at beginning
        if file_name_list[0] == '_':
            file_name_list.pop(0)
            
        # delete _ in front of file type
        x = len(file_name_list)-1
        while (x > 1 and file_name_list[x] == '_'):
            file_name_list.pop(x)
            x -= 1

        temp = "".join(file_name_list)
        src = src_dir + filename
        dst = dst_dir + temp + "." + file_type
        try: 
            os.rename(src, dst)
        except:
            print("Error: \nSource: " + src + "\nDestination: " + dst)


adv_renamer(source_dir, destination_dir)