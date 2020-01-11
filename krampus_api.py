#!/usr/bin/env python3
# Fridosleigh.com CAPTEHA API - Made by Krampus Hollyfeld
import requests
import json
import sys
import base64
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import numpy as np
import threading
import queue
import time



def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

def predict_image(q, sess, graph, image_bytes, img_full_path, labels, input_operation, output_operation):
    image = read_tensor_from_image_bytes(image_bytes)
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: image
    })
    results = np.squeeze(results)
    prediction = results.argsort()[-5:][::-1][0]
    q.put( {'img_full_path':img_full_path, 'prediction':labels[prediction].title(), 'percent':results[prediction]} )

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    return graph

def read_tensor_from_image_bytes(imagebytes, input_height=299, input_width=299, input_mean=0, input_std=255):
    image_reader = tf.image.decode_png( imagebytes, channels=3, name="png_reader")
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.compat.v1.Session()
    result = sess.run(normalized)
    return result

def main():
    yourREALemailAddress = "email@email.com"

    # Creating a session to handle cookies
    
    s = requests.Session()
    
    url = "https://fridosleigh.com/"
    
    
    json_resp = json.loads(s.get("{}api/capteha/request".format(url)).text)
    print(json_resp['select_type'])
    b64_images = json_resp['images']                    # A list of dictionaries eaching containing the keys 'base64' and 'uuid'
    challenge_image_type = json_resp['select_type'].split(',')     # The Image types the CAPTEHA Challenge is looking for.
    #print(challenge_image_type)
    if "Candy" in challenge_image_type[0]:
        typefolder0='Candy'
    elif "Christmas" in challenge_image_type[0]:
        typefolder0='Christmas'
    elif "Santa" in challenge_image_type[0]:
        typefolder0='Santahats'
    else:
        typefolder0=challenge_image_type[0]
    
    if "Candy" in challenge_image_type[1]:
        typefolder1='Candy'
    elif "Christmas" in challenge_image_type[1]:
        typefolder1='Christmas'
    elif "Santa" in challenge_image_type[1]:
        typefolder1='Santahats'
    else:
        typefolder1=challenge_image_type[1]
    
    if "Candy" in challenge_image_type[2].replace(' and ','').strip():
        typefolder2='Candy'
    elif "Christmas" in challenge_image_type[2].replace(' and ','').strip():
        typefolder2='Christmas'
    elif "Santa" in challenge_image_type[2].replace(' and ','').strip():
        typefolder2='Santahats'
    else:
        typefolder2=challenge_image_type[2].replace(' and ','').strip()
    challenge_image_types = [challenge_image_type[0].strip(), challenge_image_type[1].strip(), challenge_image_type[2].replace(' and ','').strip()] # cleaning and formatting
    print(json_resp['select_type'])
    print(f'{typefolder0} {typefolder1} {typefolder2}')
    
    # IMAGE PROCESSING AND ML IMAGE PREDICTION CODE GOES HERE
    #**************************************************************************************************
    
    # Loading the Trained Machine Learning Model created from running retrain.py on the training_images directory
    graph = load_graph('/tmp/retrain_tmp/output_graph.pb')
    labels = load_labels("/tmp/retrain_tmp/output_labels.txt")

    # Load up our session
    input_operation = graph.get_operation_by_name("import/Placeholder")
    output_operation = graph.get_operation_by_name("import/final_result")
    sess = tf.compat.v1.Session(graph=graph)


    #convert base64 image to imahe .png in file unk..imagx
    #---------------------SAVE IMAGE FROM REQUEST RESPONSE -----------------------
    os.system("rm -r unknown_imagesx/*")
    os.system("ls unknown_imagesx/")
    print("removed files")
    for image in b64_images:
        base64_img_bytes = image['base64'].encode('utf-8')
        name_image="unknown_imagesx/"+str(image['uuid'])+""
        with open(name_image, 'wb') as file_to_save:
            decode_image_data = base64.decodebytes(base64_img_bytes)
            file_to_save.write(decode_image_data)

    #--------------------------------------------
    # Can use queues and threading to spead up the processing
    
    q = queue.Queue()
    unknown_images_dir = 'unknown_imagesx'
    unknown_images = os.listdir(unknown_images_dir)
    
    
    #Going to interate over each of our images.
    for image in unknown_images:
        img_full_path = '{}/{}'.format(unknown_images_dir, image)
        print('Processing Image {}'.format(img_full_path))
        # We don't want to process too many images at once. 10 threads max
        while len(threading.enumerate()) > 10:
            #time.sleep(0.0001)
            pass
            

        #predict_image function is expecting png image bytes so we read image as 'rb' to get a bytes object
        image_bytes = open(img_full_path,'rb').read()
        threading.Thread(target=predict_image, args=(q, sess, graph, image_bytes, img_full_path, labels, input_operation, output_operation)).start()
    print('Waiting For Threads to Finish...')
    while q.qsize() < len(unknown_images):
        pass
        #time.sleep(0.001)
        
    
    #getting a list of all threads returned results
    prediction_results = [q.get() for x in range(q.qsize())]
    img_uuid_listt=[]
    #do something with our results... Like print them to the screen.
    
    #print(prediction_results)
    time.sleep(23)
    for prediction in prediction_results:
        
        
        percent=prediction['percent']*100
        
        print('TensorFlow Predicted {img_full_path} is a {prediction} with {percent:.2%} Accuracy'.format(**prediction))
        #print(str(prediction['img_full_path']).split("/")[1] )
        #print(f"{prediction['prediction']} ")
        if (typefolder0 in prediction['prediction'] or typefolder1 in prediction['prediction'] or typefolder2 in prediction['prediction']) and percent>95:
           #print(str(img_full_path).split("/")[1])
           #print("its in selection type and morethan 95")
           img_uuid_listt.append(str(prediction['img_full_path']).split("/")[1])
           #print(img_uuid_listt)
           
           if typefolder0 in prediction['prediction']:
               #print(f'in if witch will add name to txt file {typefolder0}')
               #print(f"adding to {prediction['prediction']} txt file")
               os.system("echo '"+ str(prediction['img_full_path']).split("/")[1]+ "' >> " +typefolder0 +".txt")
           elif typefolder1 in prediction['prediction']:
               print(f'in if witch will add name to txt file {typefolder1}')
               print(f"adding to {prediction['prediction']} txt file")
               os.system("echo '"+ str(prediction['img_full_path']).split("/")[1]+ "' >> " +typefolder1 +".txt")
           elif typefolder2 in prediction['prediction']:
               print(f'in if witch will add name to txt file {typefolder2}')
               print(f"adding to {prediction['prediction']} txt file")
               os.system("echo '"+ str(prediction['img_full_path']).split("/")[1]+ "' >> " +typefolder2 +".txt")
           else:
               print("not in this type print type is not asked in this sesion::")
               print(prediction['prediction'])
            
    ##**************************************************************************************************
    
    # This should be JUST a csv list image uuids ML predicted to match the challenge_image_type .
    #final_answer = ','.join( [ img['uuid'] for img in b64_images ] )
    print(json_resp['select_type'])
    final_answer=''
    for i in img_uuid_listt:
        final_answer=final_answer+i+','
    final_answer=final_answer[:-1]
    print(final_answer)       
    json_resp = json.loads(s.post("{}api/capteha/submit".format(url), data={'answer':final_answer}).text)
    
    if not json_resp['request']:
        # If it fails just run again. ML might get one wrong occasionally
        print('FAILED MACHINE LEARNING GUESS')
        print('--------------------\nOur ML Guess:\n--------------------\n{}'.format(final_answer))
        print('--------------------\nServer Response:\n--------------------\n{}'.format(json_resp['data']))
        #if 'Timed Out' in str(json_resp['data']):
        sys.exit(1)
            
            


    print('CAPTEHA Solved!')
    # If we get to here, we are successful and can submit a bunch of entries till we win
    userinfo = {
        'name':'Krampus Hollyfeld',
        'email':'email@email.com',
        'age':180,
        'about':"Cause they're so flippin yummy!",
        'favorites':'thickmints'
    }
    # If we win the once-per minute drawing, it will tell us we were emailed. 
    # Should be no more than 200 times before we win. If more, somethings wrong.
    entry_response = ''
    entry_count = 1
    while yourREALemailAddress not in entry_response and entry_count < 200:
        print('Submitting lots of entries until we win the contest! Entry #{}'.format(entry_count))
        entry_response = s.post("{}api/entry".format(url), data=userinfo).text
        entry_count += 1
    print(entry_response)


if __name__ == "__main__":
    main()