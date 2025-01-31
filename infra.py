from docker import DockerClient
from docker.errors import NotFound
import time,requests

client = DockerClient.from_env()

network_name = "job_id_scapper_network"
volume_name = "job_id_scapper_volume"
image_name_master = "master"
container_name_master = "master_container"
dockerfile_path_master = "master/." 
image_name_slave="slave"
container_name_slave="slave"
dockerfile_path_slave="slave/."




def build_images_and_network():

    # create network if not exits
    try:
        network = client.networks.get(network_name)
        print(f"Network '{network_name}' already exists.")
    except NotFound:
        network = client.networks.create(network_name, driver="bridge")
        print(f"Network '{network_name}' created.")
    # create volume if not exits

    try:
        volume = client.volumes.get(volume_name)
        print(f"Volume '{volume_name}' already exists.")
    except NotFound:
        volume = client.volumes.create(name=volume_name)
        print(f"Volume '{volume_name}' created.")

    #Build master image
    print(f"Building image '{image_name_master}' from '{dockerfile_path_master}'...")
    try:
        image, logs = client.images.build(path=dockerfile_path_master, tag=image_name_master)
        for log in logs:
            if 'stream' in log:
                print(log['stream'].strip())
        print(f"Image '{image_name_master}' built successfully.")
    except Exception as e:
        print(f"Error building image: {e}")
        exit(1)

    #build slave image
    print(f"Building image '{image_name_slave}' from '{dockerfile_path_slave}'...")
    try:
        image, logs = client.images.build(path=dockerfile_path_slave, tag=image_name_slave)
        for log in logs:
            if 'stream' in log:
                print(log['stream'].strip())
        print(f"Image '{image_name_slave}' built successfully.")
    except Exception as e:
        print(f"Error building image: {e}")
        exit(1)







def wait_for_selenium():
    url = "http://localhost:4444/wd/hub/status"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Selenium container is ready!")
                break
        except requests.exceptions.RequestException:
            print("Waiting for Selenium container to be ready...")
            time.sleep(3)


def run_slave(chunk_id):
    try:
        container_slave = client.containers.run(
            image_name_slave,  
            detach=True,  
            network=network_name,  
            name=container_name_slave+str(chunk_id),  
            volumes={volume_name: {"bind": "/data", "mode": "rw"}},  
            environment={
                "CHUNK_ID": chunk_id,
                }
                )
        print(f"Container {container_name_slave} {str(chunk_id)} started successfully.")
    except Exception as e:
        print(f"Error running container: {e}")
        exit(1)
    

    return container_slave

    # print(container_slave.logs())

if __name__ == "__main__":
    #sets up base infra volumes & network & build images
    build_images_and_network()

    #runs selenium container
    selenium_container = client.containers.run(
    "selenium/standalone-chromium",  
    detach=True,  
    network=network_name,  
    ports={"4444/tcp": 4444},  
    name="selenium_chromium_container",  
    environment={
        'SE_NODE_MAX_SESSIONS': 7,
        "SE_NODE_SESSION_TIMEOUT":30

        }
        )
    print("Selenium container started.")


    wait_for_selenium()


    #runs master container
    master_container = client.containers.run(
        image_name_master,  
        detach=True,  
        network=network_name,  
        name=container_name_master,  
        volumes={volume_name: {"bind": "/data", "mode": "rw"}},  
        environment={
        "CITY_NAME": "Toronto",   
        "PROVINCE_CODE": "ON",
        "CHUNK_NO": 6
    }
    )
    print(f"Container '{container_name_master}' started successfully.")

    master_container.wait()



    slave_0=run_slave(0)
    slave_1=run_slave(1)
    slave_2=run_slave(2)
    slave_3=run_slave(3)
    slave_4=run_slave(4)
    slave_5=run_slave(5)

    slave_0.wait()
    slave_1.wait()
    slave_2.wait()
    slave_3.wait()
    slave_4.wait()
    slave_5.wait()

    selenium_container.stop()
    selenium_container.remove()