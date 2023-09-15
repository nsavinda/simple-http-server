# simple-http-server-python
Simple HTTP server with PHP support

# Start Server


- DEFAULT_HOST = "127.0.0.1"
- DEFAULT_PORT = 2728


```python
python server.py
```

Put your files to htdocs folder


# About 

- Support for POST and GET requests 
- Supported POST request Content-Type:application/x-www-form-urlencoded
- Supported response Content-Types: text/plain, jpeg, png, mp4



# File Structure

```
├── htdocs/                        # Web site content
│   ├── index.php                  # Form
│   ├── add.php                    # Php code to add numbers
│   ├── image.jpg                  # Image
|   ├── form.html
|   ├── favicon.ico
|   ├── 1/
|   |   ├── add.php
|   |   ├── image.png
|   |   ├── index.php
|
├── server.py                      # Main File 
```


# Tested on

- Operating System: Arch Linux x86_64
- Python Version: 3.11.5
- PHP Version: 8.2.10
- Other Tools:Postman, Brave-Browser, Mozilla Firefox
