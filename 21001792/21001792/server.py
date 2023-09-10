import os
import socket
import subprocess
import argparse
import uuid


# Constants
VERSION = "5.2"
ROOT_DIR = "htdocs"
TEMP_FILE_PATH = False

# Colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
WHITEONRED = "\033[41m\033[37m"
RESET = "\033[0m"

# Print log with status code 
def print_log(method,path,status):
    if 200 <= status < 300:
        status = GREEN + str(status) + RESET
    elif 300 <= status < 400:
        status = YELLOW + str(status) + RESET
    elif 400 <= status < 500:
        status = RED + str(status) + RESET
    elif 500 <= status < 600:
        status = WHITEONRED + str(status) + RESET

    print(method + "\t" + str(status) + "\t" + path)


# Create a PHP Array from request data
def create_php_array(data):
    php_string = " array(\n"
    for item in data:
        php_string += f"    '{item[0]}' => '{item[1]}',\n"
    php_string += ");"
    return php_string


def send_response(connection, response):
    try:
        if isinstance(response, str):
            data = response.encode("utf-8")
        else:
            data = response
        sent = 0
        while sent < len(data):
            remaining_data = data[sent:]
            sent_bytes = connection.send(remaining_data)
            if sent_bytes == 0:
                raise RuntimeError("Connection closed unexpectedly")
            sent += sent_bytes
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        connection.close()

# Generate a unique identifier
def generate_unique_id():
    uuid_value = uuid.uuid4()
    random_string = str(uuid_value).replace("-", "")[:4] + str(uuid_value).replace("-", "")[-8:-4]
    return random_string

# Start the web server
def start_web_server(host, port):
    try:
        server_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
        server_socket.bind((host, port))
        server_socket.listen(20) # 20 connections 
        print(f"Server is running on http://{host}:{port}")

    
        while True:
            try:
                TEMP_FILE_PATH = False
                params = False
                content_type = "text/html"

                connection, address = server_socket.accept()
                request_lines = connection.recv(4096).decode("utf-8").split("\r\n") # get request lines
                # split GET request parameters
                path = request_lines[0].split(" ")[1]
                if 2 == len(path.split("?")):
                    path,params = path.split("?")


                request_method = request_lines[0].split(" ")[0]
                file_path = os.path.join(ROOT_DIR, path.lstrip("/"))  # get file path form url path 
                if os.path.exists(file_path) and os.path.commonpath([ROOT_DIR, file_path]) == ROOT_DIR:
                    if os.path.isdir(file_path):
                        if os.path.exists(os.path.join(file_path, "index.php")): # check php file available or not 
                            file_path = os.path.join(file_path, "index.php")  # chnage file path 
                        elif os.path.exists(os.path.join(file_path, "index.html")): # check html file available or not 
                            file_path = os.path.join(file_path, "index.html") # change file path 

                    if not os.path.isdir(file_path): # check path is still directory or not
                        if file_path.endswith(".php"): # check file path

                            # Handle PHP files
                            
                            # Handle POST data
                            if request_method == "POST": 
                                post_data = list(map(lambda x: [ it for it in x.split("=")], request_lines[request_lines.index('') + 1].split("&"))) # convert to list [['n1', '5'], ['n2', '8']]
                                php_text = f"<?php \n $_SERVER['REQUEST_METHOD'] = 'POST'; \n $_POST =  {create_php_array(post_data)}  ?> \n\n"

                                with open(file_path, 'r') as php_file: # read php file
                                    php_code = php_file.read()

                                dir_path = os.path.dirname(file_path)
                                file_name = "." + generate_unique_id() + "_" + os.path.basename(file_path)  # get name for temporary php file
                                file_path = os.path.join(dir_path, file_name)       # get path for temporary php file
                                TEMP_FILE_PATH = file_path

                                with open(file_path, 'w') as php_file:  # save new temporary file with request data
                                    php_file.write(php_text + php_code)

                            # Handle GET data
                            if request_method == "GET" and params: # work only if request has URL parameters
                                get_data = list(map(lambda x: [ it for it in x.split("=")], params.split("&")))  ## Work same as above code

                                php_text = f"<?php \n $_SERVER['REQUEST_METHOD'] = 'GET'; \n $_GET =  {create_php_array(get_data)}  ?> \n\n"

                                with open(file_path, 'r') as php_file:
                                    php_code = php_file.read()

                                dir_path = os.path.dirname(file_path)
                                file_name = "." + generate_unique_id() + "_" + os.path.basename(file_path)
                                file_path = os.path.join(dir_path, file_name)
                                TEMP_FILE_PATH = file_path

                                with open(file_path, 'w') as php_file:
                                    php_file.write(php_text + php_code)

                            try:
                                output = subprocess.run(['php', file_path], capture_output=True, text=True, check=True)  # Create subprocess to run php file and get output
                                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html \r\n\r\n" + output.stdout
                                print_log(request_method, path, 200)

                            except subprocess.CalledProcessError as e:
                                response = "HTTP/1.1 500 Internal Server Error\r\n\r\nInternal Server Error\n" + e.stderr
                                print_log(request_method, path, 500)

                            if TEMP_FILE_PATH:   # Delete temporary file 
                                try:
                                    os.remove(TEMP_FILE_PATH)
                                    # print(f"File '{TEMP_FILE_PATH}' has been deleted.")
                                except OSError as e:
                                    print(f"Error deleting file: {e}")

                        else:
                            # Handle HTML files
                            try:
                                with open(file_path, "rb") as file:
                                    file_content = file.read()
                                    content_type = "text/html"  # Plain text


                                    file_extension = file_path.split(".")[-1].lower()

                                    if file_extension == "jpg" or file_extension == "jpeg":
                                        content_type = "image/jpeg"
                                    elif file_extension == "png":
                                        content_type = "image/png"
                                    elif file_extension == "mp4":
                                        content_type = "video/mp4"
                                    elif file_extension == "pdf":
                                        content_type = "application/pdf"
                                    elif file_extension == "html":
                                        content_type = "text/html"
                                    elif file_extension == "js":
                                        content_type = "text/javascript"
                                    elif file_extension == "css":
                                        content_type = "text/css"

                                    response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8") + file_content
                                    print_log(request_method, path, 200)
                            except FileNotFoundError:
                                response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
                                print_log(request_method, path, 404)
                            except PermissionError:
                                response = "HTTP/1.1 403 Forbidden\r\n\r\nPermission Denied"
                                print_log(request_method, path, 403)
                            except Exception as e:
                                response = "HTTP/1.1 500 Internal Server Error\r\n\r\n" + str(e)
                                print_log(request_method, path, 500)
                    else:
                        # Handle directories
                        content = "<html><body><h1>Directory Contents</h1><ul>"
                        for item in os.listdir(file_path):
                            item_path = os.path.join(file_path, item)
                            if os.path.isdir(item_path):
                                content += f"<li><b><a href='{path.rstrip('/')}/{item}/'>{item}</a></b></li>"
                            else:
                                content += f"<li><a href='{path.rstrip('/')}/{item}'>{item}</a></li>"
                        content += "</ul></body></html>"
                        response = "HTTP/1.1 200 OK\r\n\r\n" + content
                        print_log(request_method, path, 200)
                else:
                    response = "HTTP/1.1 403 Forbidden\r\n\r\nForbidden"
                    print_log(request_method, path, 403)
                
                send_response(connection,response)  # send response
            except KeyboardInterrupt:
                server_socket.close()
                exit()     
            except:
                continue

    except KeyboardInterrupt:
        server_socket.close()
        exit()
    except OSError as e:
        if e.errno == 98:
            print("Address already in use. Waiting for the port to free up")
        else:
            print(f"Error: {e}")
    
        


# Default server host and port
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 2728

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-S", "--server", type=str, default=f"{DEFAULT_HOST}:{DEFAULT_PORT}", help="Server address in the format 'host:port' (default: 127.0.0.1:4000)")
parser.add_argument("-v", "--version", action="store_true", help="Print version number")
args = parser.parse_args()

# Check for version flag
if args.version:
    print(f"Simple HTTP Server\nAuthor: Nirmal Savinda\nVersion: {VERSION}")
    exit(0)

# Parse host and port from the server argument
server_host, server_port = args.server.split(":")
server_port = int(server_port)

# Start the web server

start_web_server(server_host, server_port)


