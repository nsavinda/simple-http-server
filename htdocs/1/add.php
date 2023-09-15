<html>
    <body>
<?php

if (isset($_POST['n1']) && isset($_POST['n2']))
    echo $_POST['n1'] + $_POST['n2'];
else
    echo "empty";


    if (isset($_GET['n1']) && isset($_GET['n2']))
    echo $_GET['n1'] + $_GET['n2'];
?>

</body>
</html>