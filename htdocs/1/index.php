<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('image.jpg'); /* Replace 'your-image-url.jpg' with the actual URL or path to your image */
            background-size: cover; /* This will cover the entire background */
            background-repeat: no-repeat; /* Prevent image from repeating */
            background-attachment: fixed;
        }
        form {
            width: 350px;
            margin: 0 auto;
            padding: 30px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 3px;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <form action="add.php" method="post">
        <input type="text" name="n1" placeholder="Enter number 1" />
        <br>
        <input type="text" name="n2" placeholder="Enter number 2" />
        <br>
        <input type="submit" name="submit" value="Submit">
    </form>
</body>
</html>
